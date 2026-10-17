import paypalrestsdk
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Use 'live' for production
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})

# Define the payment
payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"
    },
    "transactions": [{
        "amount": {
            "total": "10.00",
            "currency": "USD"
        },
        "description": "Payment for services"
    }],
    "redirect_urls": {
        "return_url": "http://localhost:8000/payment/execute",
        "cancel_url": "http://localhost:8000/payment/cancel"
    }
})

# Create the payment
if payment.create():
    print("Payment created successfully")
    for link in payment.links:
        if link.method == "REDIRECT":
            redirect_url = link.href
            print("Redirect for approval: %s" % redirect_url)
else:
    print("Error while creating payment: %s" % payment.error)
