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
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # Ensure settings import
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings 
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.db import models
from django import forms 
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
    first_name = None  # Remove first_name field from CustomUser
    last_name = None

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
    #email_user = models.EmailField(unique=True,null = True)
    #password = models.CharField(max_length=100,null = True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',default='projectone/Users/defaults/default-avatar-icon-of-social-media-user-vector.jpg')

    def __str__(self):
        return self.user.username

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
import re

class Region(models.Model):
    REGION_CHOICES = [
        ('Mountainous', 'Mountainous Region'),
        ('Coastal', 'Coastal Region'),
        ('Desert', 'Desert Region'),
        ('Forest', 'Forest Region')
    ]
    region_type = models.CharField(max_length=20, choices=REGION_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    
    description = models.TextField()

    def __str__(self):
        return self.name

class CategorySite(models.Model):
    CATEGORY_CHOICES = [
        ('for_you', 'For You'),
        ('culture', 'Culture'),
        ('nature', 'Nature'),
        ('hotel', 'Hotel'),
        ('food', 'Food')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.category
    
class Wilayat(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='images/')
    category = models.ForeignKey(CategorySite, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
def validate_phone_number(value):
    phone_regex = re.compile(r'^(0|\+213)(5|6|7)\d{8}$')
    if not phone_regex.match(value):
        raise ValidationError("The phone number entered is not valid. It should start with 0 or +213 followed by 9 digits.")

    
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    phone_number = PhoneNumberField(blank=True, null=True, region='DZ', help_text='Enter phone number in international format, starting with +213 or 0 followed by 9 digits.')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    item_type = models.CharField(max_length=100)
    full_description = models.TextField()
    highlight = models.TextField()
    url = models.URLField(max_length=500)
    time_string = models.TextField()
    picture = models.ImageField(upload_to='images/')
    picture1 = models.ImageField(upload_to='images/', blank=True, null=True)
    picture2 = models.ImageField(upload_to='images/', blank=True, null=True)
    picture3 = models.ImageField(upload_to='images/', blank=True, null=True)
    picture4 = models.ImageField(upload_to='images/', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    wilayat = models.ForeignKey(Wilayat, on_delete=models.CASCADE)
    category = models.ForeignKey(CategorySite, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
 

from .models import Item  # Assuming Item is the related model

from django.db import models

class Review(models.Model):
    text = models.TextField(blank=True, null=True,)
    rating = models.IntegerField(blank=True, null=True,)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically sets the timestamp on creation

    def __str__(self):
        return f"Review for {self.item}: {self.text}"
  



class Upload(models.Model):
    name = models.CharField(max_length=100, default='Default Name')
    id = models.AutoField(primary_key=True)
    description = models.TextField(default='Default description')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.name

from django.db import models

from django.db import models

from django.db import models


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ActivityCategory(models.Model):
    name = models.CharField(max_length=255)

class Food(models.Model):
    name = models.CharField(max_length=255)

class Transport(models.Model):
    name = models.CharField(max_length=255)

class SuitableFor(models.Model):
    description = models.TextField()
    activity = models.ForeignKey('Activity', related_name='suitable_for', on_delete=models.CASCADE)

class Allowed(models.Model):
    description = models.TextField()
    activity = models.ForeignKey('Activity', related_name='allowed', on_delete=models.CASCADE)

class NotAllowed(models.Model):
    description = models.TextField()
    activity = models.ForeignKey('Activity', related_name='not_allowed', on_delete=models.CASCADE)

class Includes(models.Model):
    description = models.TextField()
    activity = models.ForeignKey('Activity', related_name='includes', on_delete=models.CASCADE)

class NotIncludes(models.Model):
    description = models.TextField()
    activity = models.ForeignKey('Activity', related_name='not_includes', on_delete=models.CASCADE)

class Highlights(models.Model):
    description = models.TextField()
    activity = models.ForeignKey('Activity', related_name='highlights', on_delete=models.CASCADE)

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activity_name = models.CharField(max_length=255)
    guide_name = models.CharField(max_length=255)
    guide_phone = models.CharField(max_length=20)
    activity_category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    activity_description = models.TextField()
    activity_location = models.URLField()
    food = models.ManyToManyField(Food)
    transport = models.ManyToManyField(Transport)
    emergency_phone_number = models.CharField(max_length=20)
    cut_off_time = models.CharField(max_length=20)
    meeting_point = models.URLField()
    published_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='published_activities' , null = True , blank = True)
    class Meta:
         
        constraints = [
            models.CheckConstraint(
                check=~models.Q(activity_location=models.F('meeting_point')),
                name='meeting_point_different_from_location'
            ),
        ]
        
def __str__(self):
        return  self.activity_id



class DailyActivity(models.Model):
    
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE,primary_key=True,related_name='daily_activity')
    activity_date = models.DateField(null = True , blank = True)
    start_hour = models.TimeField(null = True , blank = True)
    end_hour = models.TimeField(null = True , blank = True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_hour__lt=models.F('end_hour')),
                name='start_date_before_end_date'
            ),
        ]
        

class WeeklyActivity(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE,primary_key=True,related_name='weekly_activity')
    day = models.CharField(max_length=255)
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_hour__lt=models.F('end_hour')),
                name='start_date_before_end_date_weekly'
            ),
        ]
        
class SpecificDurationActivity(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE,primary_key=True,related_name='specific_duration_activity')
    start_date = models.DateField()
    activity_start_hour = models.TimeField()
    activity_end_date = models.DateField()
    end_hour = models.TimeField()
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F('activity_end_date')),
                name='start_date_before_end_date_specific'
            ),
        ]
        

class OneDayActivity(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE, primary_key=True,related_name='one_day_activity')
    activity_start_hour = models.TimeField()
    activity_end_hour = models.TimeField()
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(activity_start_hour__lt=models.F('activity_end_hour')),
                name='start_date_before_end_date_oneday'
            ),
        ]
        
    def __str__(self):
        return f"{self.activity.activity_name} - One Day Activity"
class Price(models.Model):
    PRICE_TYPE_CHOICES = [
        ('ADULT', 'Adult'),
        ('CHILD', 'Child'),
        ('GROUP', 'Group'),
        ('INDIVIDUAL', 'Individual'),
    ]
    price_type = models.CharField(max_length=50, choices=PRICE_TYPE_CHOICES)
    number_of_clients = models.IntegerField()
    price = models.FloatField()
    activity = models.ForeignKey('Activity', related_name='prices', on_delete=models.CASCADE )



class Photos(models.Model):

  image_path = models.ImageField(upload_to='Activities_Photos/',default='projectone/Users/defaults/default-avatar-icon-of-social-media-user-vector.jpg')

  activity = models.ForeignKey('Activity', related_name='photos', on_delete=models.CASCADE , null = True , blank = True )