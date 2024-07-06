# Users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from Users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, **kwargs):
    # Check if the user is active and it's the first time they are being activated
    if instance.is_active and instance._state.adding is False:
        # Determine if the user is a guide or agency and set the email message accordingly
        if instance.is_guide:
            subject = 'Your Guide Account is Now Active'
            message = 'Congratulations, your guide account is now active. You can now log in and start using our services.'
        elif instance.is_agency:
            subject = 'Your Agency Account is Now Active'
            message = 'Congratulations, your agency account is now active. You can now log in and start using our services.'
        else:
            return

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
