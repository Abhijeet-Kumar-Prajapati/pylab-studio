# PayPal Clone

A simple PayPal clone application built with Flask that allows users to send and receive money, view transaction history, and manage their wallet.

## Features

- User registration and authentication
- Send money to other users
- View transaction history
- Real-time balance updates
- Secure password hashing
- Modern and responsive UI

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd paypal-clone
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Register a new account using your email and password
2. Login with your credentials
3. View your dashboard to see your balance and transaction history
4. Use the "Send Money" feature to transfer funds to other users
5. Logout when you're done

## Technologies Used

- Backend: Python Flask
- Database: SQLite with SQLAlchemy
- Frontend: HTML, CSS
- Authentication: Flask-Login
- Password Hashing: Werkzeug Security

## Security Features

- Secure password hashing
- User session management
- CSRF protection
- Input validation
- Secure database queries

## File Structure

```
paypal-clone/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── static/
│   └── css/
│       └── style.css     # CSS styles
└── templates/
    ├── index.html        # Landing page
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # User dashboard
    └── send_money.html   # Send money page
```

## Contributing

Feel free to submit issues and enhancement requests.
