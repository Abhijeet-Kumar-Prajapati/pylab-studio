from flask import Flask, render_template_string, request, jsonify
import stripe
from twilio.rest import Client

app = Flask(__name__)

# Set your Stripe secret key and Twilio credentials here
stripe.api_key = 'your_stripe_secret_key'  # Replace with your Stripe secret key
TWILIO_SID = 'your_twilio_account_sid'     # Replace with your Twilio Account SID
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'  # Replace with your Twilio Auth Token
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'  # Replace with your Twilio phone number

# Twilio client setup
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Function to get the country code
def get_country_code(country):
    country_codes = {
        'US': '1',
        'IN': '91',
        'UK': '44',
        # Add more countries as needed
    }
    return country_codes.get(country, '1')  # Default to US if country is not found

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Real-Time Calling with Country Selection</title>
    </head>
    <body>
      <h1>Dial a Mobile Number</h1>
      
      <label for="country">Select Country:</label>
      <select id="country">
        <option value="US">United States (+1)</option>
        <option value="IN">India (+91)</option>
        <option value="UK">United Kingdom (+44)</option>
        <!-- Add more countries as needed -->
      </select>
      
      <label for="phoneNumber">Enter Phone Number:</label>
      <input type="text" id="phoneNumber" placeholder="Enter phone number" />
      
      <button onclick="initiateCall()">Make a Call</button>

      <script src="https://js.stripe.com/v3/"></script>
      <script>
        const stripe = Stripe('your_stripe_publishable_key');  // Replace with your Stripe public key

        async function initiateCall() {
          const country = document.getElementById('country').value;
          const phoneNumber = document.getElementById('phoneNumber').value;
          
          if (!phoneNumber) {
            alert('Please enter a phone number');
            return;
          }

          // Prepend country code to the phone number
          const fullPhoneNumber = `+${getCountryCode(country)}${phoneNumber}`;
          
          try {
            // Step 1: Create Payment Intent
            const response = await fetch('/start-payment', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ phoneNumber: fullPhoneNumber })
            });

            const data = await response.json();
            if (data.paymentIntentClientSecret) {
              const { error, paymentIntent } = await stripe.confirmCardPayment(data.paymentIntentClientSecret);

              if (error) {
                alert(error.message);
              } else if (paymentIntent.status === 'succeeded') {
                // Step 2: Payment successful, make the call
                const callResponse = await fetch('/start-call', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ phoneNumber: fullPhoneNumber })
                });

                const callData = await callResponse.json();
                if (callData.success) {
                  alert('Call initiated!');
                } else {
                  alert('Failed to initiate call');
                }
              }
            }
          } catch (error) {
            console.error('Error:', error);
            alert('An error occurred.');
          }
        }

        // Helper function to get the country code
        function getCountryCode(country) {
          const countryCodes = {
            'US': '1',
            'IN': '91',
            'UK': '44',
            // Add more countries as needed
          };
          return countryCodes[country] || '1'; // Default to US if not found
        }
      </script>
    </body>
    </html>
    """)

@app.route('/start-payment', methods=['POST'])
def start_payment():
    data = request.get_json()
    phone_number = data['phoneNumber']
    
    try:
        # Create a payment intent (charge $10)
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,  # Amount in cents
            currency='usd',
            metadata={'phoneNumber': phone_number}
        )
        return jsonify({'paymentIntentClientSecret': payment_intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start-call', methods=['POST'])
def start_call():
    data = request.get_json()
    phone_number = data['phoneNumber']
    
    try:
        # Initiate the call via Twilio
        call = twilio_client.calls.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            url='http://demo.twilio.com/docs/voice.xml'  # Twilio call script URL (this is a simple example)
        )
        return jsonify({'success': True, 'callSid': call.sid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
