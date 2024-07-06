# myapp/utils.py
import random
from twilio.rest import Client
from django.conf import settings

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_code(phone_number, code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your verification code is {code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid
