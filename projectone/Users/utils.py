# myapp/utils.py
import random
from twilio.rest import Client
from django.conf import settings

 
# utils.py

import random
from django.conf import settings
from twilio.rest import Client
from .models import TemporaryAgencySignup

def send_verification_code(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification_code = str(random.randint(100000, 999999))
    message = client.messages.create(
        body=f'Your verification code is: {verification_code}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return verification_code

def verify_code(phone_number, code):
    try:
        temp_signup = TemporaryAgencySignup.objects.get(agency_phone_number=phone_number, verification_code=code)
        if not temp_signup.is_verified:
            temp_signup.is_verified = True
            temp_signup.save()
            return True
    except TemporaryAgencySignup.DoesNotExist:
        return False
    return False
