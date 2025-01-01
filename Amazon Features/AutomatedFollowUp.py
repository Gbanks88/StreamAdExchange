import os
from twilio.rest import Client

# Load credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

def send_follow_up(customer_phone, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(body=message, from_='+1234567890', to=customer_phone)

# Example usage
send_follow_up('+0987654321', "Thank you for your purchase! Please leave a review.")