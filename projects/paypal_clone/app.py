from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import logging
import secrets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# SECRET_KEY signs sessions and CSRF tokens, so it must never fall back to a
# value that is published in the repository. Use the SECRET_KEY environment
# variable in production; otherwise generate a random one for this process.
_secret = os.environ.get('SECRET_KEY')
if not _secret:
    _secret = secrets.token_hex(32)
    logger.warning(
        "SECRET_KEY is not set - generated a random one for this process. "
        "Sessions will be invalidated on restart. Set SECRET_KEY in production."
    )
app.config['SECRET_KEY'] = _secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paypal_clone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('COOKIE_SECURE', '0') == '1'
app.config['WTF_CSRF_ENABLED'] = True

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Form Classes
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class SendMoneyForm(FlaskForm):
    receiver_email = EmailField('Receiver Email', validators=[DataRequired(), Email()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.Float, default=0.0)
    transactions_sent = db.relationship('Transaction', backref='sender', lazy=True, foreign_keys='Transaction.sender_id')
    transactions_received = db.relationship('Transaction', backref='receiver', lazy=True, foreign_keys='Transaction.receiver_id')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))
            
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page or url_for('dashboard'))
            flash('Invalid email or password', 'danger')
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash('An error occurred during login. Please try again.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        transactions = Transaction.query.filter(
            (Transaction.sender_id == current_user.id) | 
            (Transaction.receiver_id == current_user.id)
        ).order_by(Transaction.timestamp.desc()).all()
        return render_template('dashboard.html', transactions=transactions)
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        flash('Error loading dashboard. Please try again.', 'danger')
        return redirect(url_for('index'))

@app.route('/send_money', methods=['GET', 'POST'])
@login_required
def send_money():
    form = SendMoneyForm()
    if form.validate_on_submit():
        try:
            amount = round(float(form.amount.data), 2)
            receiver = User.query.filter_by(email=form.receiver_email.data).first()

            if not receiver:
                flash('Recipient not found', 'danger')
                return redirect(url_for('send_money'))

            if receiver.id == current_user.id:
                flash('You cannot send money to yourself', 'danger')
                return redirect(url_for('send_money'))

            if current_user.balance < amount:
                flash('Insufficient balance', 'danger')
                return redirect(url_for('send_money'))

            current_user.balance -= amount
            receiver.balance += amount

            transaction = Transaction(
                amount=amount,
                sender_id=current_user.id,
                receiver_id=receiver.id,
                description=form.description.data
            )

            db.session.add(transaction)
            db.session.commit()
            flash('Money sent successfully!', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            logger.error(f"Send money error: {str(e)}")
            db.session.rollback()
            flash('An error occurred while sending money. Please try again.', 'danger')
            return redirect(url_for('send_money'))

    return render_template('send_money.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
    
    # Run the application.
    # Defaults are deliberately safe: bind to loopback only and keep the
    # debugger OFF. Werkzeug's debugger allows remote code execution, so it
    # must never be reachable from another machine.
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    if debug and host not in ('127.0.0.1', 'localhost', '::1'):
        logger.error("Refusing to start: FLASK_DEBUG=1 is only allowed on loopback.")
        raise SystemExit(1)

    logger.info(f"Starting on http://{host}:{port}  (debug={debug})")
    app.run(host=host, port=port, debug=debug)