from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings 
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.db import models
from django import forms 
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

 

LANGUAGE_CHOICES = [
        ("en", "English"),
        ("es", "Spanish"),
        ("fr", "French"),
        ("de", "German"),
        ("zh", "Chinese"),
        ("ja", "Japanese"),
        ("ar", "Arabic"),
        ("ru", "Russian"),
        ("pt", "Portuguese"),
        ("it", "Italian"),
        ("ko", "Korean"),
        ("nl", "Dutch"),
        ("sv", "Swedish"),
        ("tr", "Turkish"),
        ("pl", "Polish"),
        ("vi", "Vietnamese"),
        ("el", "Greek"),
        ("th", "Thai"),
    ] 
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    is_client = models.BooleanField(default=False)
    is_agency = models.BooleanField(default=False)
    is_guide = models.BooleanField(default=False)

    def __str__(self):
        return self.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        if instance.is_client:
            send_mail(
                'Welcome!',
                'Thank you for registering as a client. You can now log in to your account.',
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )

 
def validate_pdf(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")

class Agency(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agency')
    agency_name = models.CharField(max_length=255,null = True)
    agency_email = models.EmailField(unique=True,null = True)
    password = models.CharField(max_length=100,null = True)
    agency_phone_number = models.CharField(max_length=15,null = True)  
    agency_website = models.CharField(max_length=255,null = True)
    number_of_employees = models.CharField(max_length=15,null = True)
    agency_location = models.CharField(max_length=15,null = True)
    agency_licenses = models.FileField(upload_to='licenses/', null=True, blank=True,)
    agency_profile_picture = models.FileField(upload_to='profile_pictures/',default='projectone/Users/defaults/default-avatar-icon-of-social-media-user-vector.jpg')

    def __str__(self):
        return  self.agency_name
  
  
 
class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Guide(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='guide')
    guide_email = models.EmailField(unique=True, null=True)
    guide_phone_number = models.CharField(max_length=15, null=True)
    password = models.CharField(max_length=100, null=True)
    guide_first_name = models.CharField(max_length=30, null=True)
    guide_last_name = models.CharField(max_length=30, null=True)
    guide_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    guide_languages = models.ManyToManyField(Language, related_name='guides')
    guide_dateofbirth = models.DateField(_("mm/dd/yyyy"), auto_now=False, auto_now_add=False)
    guide_description = models.CharField(max_length=200)
    guide_website = models.CharField(max_length=100, null=True)
    guide_location = models.CharField(max_length=100, null=True)
    guide_licenses = models.FileField(upload_to='licenses/', null=True)
    guide_profile_picture = models.ImageField(upload_to='profile_pictures/', default='projectone/Users/defaults/default-avatar-icon-of-social-media-user-vector.jpg')

    def __str__(self):
        return f"{self.guide_first_name} {self.guide_last_name}"

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client', null = True)
    first_name = models.CharField(max_length=30,null = True)
    last_name = models.CharField(max_length=30,null = True)
    phone_number = PhoneNumberField(null = True, blank = True)
    email_user = models.EmailField(unique=True,null = True)
    password = models.CharField(max_length=100,null = True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',default='projectone/Users/defaults/default-avatar-icon-of-social-media-user-vector.jpg')

    def __str__(self):
        return self.user.username
