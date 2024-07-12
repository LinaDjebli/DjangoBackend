import re
from django.forms import DateField
from rest_framework import serializers 
from Users.models import  Transport,Food,Price,SuitableFor, CustomUser, Client, Agency, Guide, OneDayActivity, Photos, SpecificDurationActivity, WeeklyActivity, validate_pdf  ,LANGUAGE_CHOICES , Language
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.serializers import Serializer, FileField

class UserSerialier(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_client', 'is_agency', 'is_guide']
        
       
        
         
class AgencySignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)  # Added username field
    agency_name = serializers.CharField(required=True)
    agency_email = serializers.EmailField(required=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    agency_phone_number = serializers.CharField(required=True)
    agency_website = serializers.CharField(required=True)
    number_of_employees = serializers.CharField(required=True)
    agency_location = serializers.CharField(required=True)
    agency_licenses = serializers.FileField(required=False)
    agency_profile_picture = serializers.FileField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'agency_name', 'agency_email', 'password' , 'agency_phone_number', 'agency_website', 'number_of_employees', 'agency_location', 'agency_licenses', 'agency_profile_picture']

    def save(self, **kwargs):
        email = self.validated_data['agency_email']
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        user = CustomUser(
            username=self.validated_data['username'],
            email=email,
            is_active=False  # User will be inactive until approved
        )
        password = self.validated_data['password']
        
        

        user.set_password(password)
        user.is_agency = True
        user.save()

        # Create related Agency object
        Agency.objects.create(
            user=user,
            agency_name=self.validated_data['agency_name'],
            agency_email=email,
            password=password,
            agency_phone_number=self.validated_data['agency_phone_number'],
            agency_website=self.validated_data['agency_website'],
            number_of_employees=self.validated_data['number_of_employees'],
            agency_location=self.validated_data['agency_location'],
            agency_licenses=self.validated_data.get('agency_licenses'),
            agency_profile_picture=self.validated_data.get('agency_profile_picture', 'defaults/default_profile_picture.png')
        )

        # Send pending approval email
        send_mail(
            
            'Registration Pending Approval',
            'Your registration request has been received and is pending approval.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return user

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.core import exceptions as django_exceptions
 
from django.core.mail import send_mail
from django.conf import settings

class GuideSignupSerializer(serializers.ModelSerializer):
    guide_first_name = serializers.CharField(required=True)
    guide_last_name = serializers.CharField(required=True)
    guide_email = serializers.EmailField(required=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)
    guide_phone_number = serializers.CharField(required=True)
    guide_website = serializers.CharField(required=False)
    guide_location = serializers.CharField(required=False)
    guide_licenses = serializers.FileField(required=False)
    guide_dateofbirth = serializers.DateField(input_formats=["%Y/%m/%d"], required=True)
    guide_profile_picture = serializers.FileField(required=False)
    guide_gender = serializers.ChoiceField(choices=Guide.GENDER_CHOICES, required=True)
    guide_languages = serializers.ListField(
 child=serializers.IntegerField(), write_only=True)
    guide_description = serializers.CharField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'guide_email', 'guide_first_name', 'guide_last_name', 'password', 'guide_phone_number', 'guide_website', 'guide_location', 'guide_licenses', 'guide_profile_picture', 'guide_gender', 'guide_languages', 'guide_dateofbirth', 'guide_description']

    def create(self, validated_data):
        email = validated_data['guide_email']
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        username = validated_data.get('username', '')
        guide_first_name = validated_data.get('guide_first_name')
        guide_last_name = validated_data.get('guide_last_name')
        password = validated_data.get('password')
        languages = validated_data.pop('guide_languages')

        user = CustomUser.objects.create_user(
            username=username if username else email.split('@')[0],
            email=email,
            password=password,
            is_active=False  # User will be inactive until approved
        )
        user.set_password(password)
        user.is_guide = True
        user.save()
        
        guide = Guide.objects.create(
            user=user,
            guide_email=email,
            guide_phone_number=validated_data.get('guide_phone_number'),
            guide_first_name=guide_first_name,
            guide_last_name=guide_last_name,
            guide_website=validated_data.get('guide_website', ''),
            guide_location=validated_data.get('guide_location'),
            guide_licenses=validated_data.get('guide_licenses',),
            guide_profile_picture=validated_data.get('guide_profile_picture', 'defaults/default_profile_picture.png'),
            guide_gender=validated_data.get('guide_gender'),
            guide_dateofbirth=validated_data.get('guide_dateofbirth'),
            guide_description=validated_data.get('guide_description')
        )
        guide.guide_languages.set(languages)
        guide.save()

        # Send pending approval email
        send_mail(
            'Registration Pending Approval',
            'Your registration request has been received and is pending approval.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return user
     
from rest_framework import serializers
from Users.models import CustomUser, Client
from django.core.mail import send_mail
from django.conf import settings
"""""
class ClientSignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)
    phone_number = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'profile_picture']

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        if not email:
            raise serializers.ValidationError({"email": "This field is required."})

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        username = self.validated_data.get('username', '')
        first_name = self.validated_data.get('first_name')
        last_name = self.validated_data.get('last_name')
        password = self.validated_data.get('password')

         
        user = CustomUser(
            username=username if username else email.split('@')[0],  # Default to email's local part if username not provided
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_client=True,
            is_active=True  # Activate the client directly
        )
        user.set_password(password)
        user.save()

        Client.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone_number=self.validated_data.get('phone_number', ''),
            email_user=email,
            password=password,
            profile_picture=self.validated_data.get('profile_picture', 'defaults/default_profile_picture.png')
        )

        # Send approval email to client
         

        return user
# serializers.py
"""


class ClientSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)
    phone_number = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone_number', 'profile_picture']

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        if not email:
            raise serializers.ValidationError({"email": "This field is required."})

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        username = self.validated_data.get('username', '')
        password = self.validated_data.get('password')

        user = CustomUser(
            username=username if username else email.split('@')[0],  # Default to email's local part if username not provided
            email=email,
            is_client=True,
            is_active=True  # Activate the client directly
        )
        user.set_password(password)
        user.save()

        Client.objects.create(
            user=user,
            phone_number=self.validated_data.get('phone_number', ''),
            profile_picture=self.validated_data.get('profile_picture', 'defaults/default_profile_picture.png')
        )

        # Optionally send approval email to client here

        return user
from rest_framework import serializers
 

class ProfilePictureUpdateSerializer(serializers.ModelSerializer):
    agency_profile_picture = serializers.ImageField(required=True)

    class Meta:
        model = Agency
        fields = ['agency_profile_picture']



class GuideProfilePictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ['guide_profile_picture']



from rest_framework import serializers
from Users.models import Item, Region, Wilayat , CategorySite ,Review

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'item', 'timestamp']
        extra_kwargs = {
            'text': {'required': False, 'allow_blank': True},
            'rating': {'required': False}
        }

       

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class WilayatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilayat
        fields = '__all__'
       

class CategorySiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySite
        fields = '__all__'       






from Users.models import (
    Activity, DailyActivity, Price, Food, Transport, SuitableFor, Allowed, NotAllowed, 
    Includes, NotIncludes, Highlights, ActivityCategory, CustomUser
)

 
from rest_framework import serializers
from Users.models import DailyActivity, Activity, Price, Allowed, NotAllowed, Includes, NotIncludes, Highlights
from Users.models import CustomUser

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['price_type', 'number_of_clients', 'price']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Photos
        fields = ['image_path']

class AllowedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowed
        fields = ['description']

class SuitableforSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SuitableFor
        fields = ['description']


class NotAllowedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotAllowed
        fields = ['description']


class IncludesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Includes
        fields = ['description']


class NotIncludesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotIncludes
        fields = ['description']


class HighlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlights
        fields = ['description']


class ActivitySerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, required=False)
    food = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    transport = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    suitable_for = SuitableforSerializer(many=True , required = False)
    allowed = AllowedSerializer(many= True , required = False) 
    not_allowed = NotAllowedSerializer(many=True,required = False)
    includes = IncludesSerializer(many=True,required=False)
    not_includes = NotIncludesSerializer(many=True, required = False)
    highlights = HighlightsSerializer(many=True , required=False)
    photos = PhotoSerializer(many=True , required= False)
    published_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Activity
        fields = [
            'activity_name', 'guide_name', 'guide_phone', 'activity_category',
            'activity_type', 'activity_description', 'activity_location', 'food', 'transport',
            'emergency_phone_number', 'cut_off_time', 'meeting_point',
            'suitable_for', 'allowed', 'not_allowed', 'includes', 'not_includes', 'highlights',
            'prices', 'published_by','photos'
        ]

    def create(self, validated_data):
        prices_data = validated_data.pop('prices', [])
        food_data = validated_data.pop('food', [])
        transport_data = validated_data.pop('transport', [])
        suitable_for_data = validated_data.pop('suitable_for', [])
        allowed_data = validated_data.pop('allowed', [])
        not_allowed_data = validated_data.pop('not_allowed', [])
        includes_data = validated_data.pop('includes', [])
        not_includes_data = validated_data.pop('not_includes', [])
        highlights_data = validated_data.pop('highlights', [])

        activity = Activity.objects.create(**validated_data)

        for price_data in prices_data:
            Price.objects.create(activity=activity, **price_data)

        activity.food.set(food_data)
        activity.transport.set(transport_data)
         
        for allowed_item in allowed_data:
            Allowed.objects.create(activity=activity, **allowed_item)

        for not_allowed_item in not_allowed_data:
            NotAllowed.objects.create(activity=activity, **not_allowed_item)

        for includes_item in includes_data:
            Includes.objects.create(activity=activity, **includes_item)

        for not_includes_item in not_includes_data:
            NotIncludes.objects.create(activity=activity, **not_includes_item)

        for highlight_item in highlights_data:
            Highlights.objects.create(activity=activity, **highlight_item)

        return activity

    def update(self, instance, validated_data):
        instance.activity_name = validated_data.get('activity_name', instance.activity_name)
        instance.guide_name = validated_data.get('guide_name', instance.guide_name)
        instance.guide_phone = validated_data.get('guide_phone', instance.guide_phone)
        # Update other fields similarly

        # Handle related fields updates
         
        # Update related fields as needed

        instance.save()
        return instance


class DailyActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    activity_date = serializers.DateField()
    start_hour = serializers.TimeField()
    end_hour = serializers.TimeField()

    class Meta:
        model = DailyActivity
        fields = ['activity', 'activity_date', 'start_hour', 'end_hour']

    def create(self, validated_data):
        activity_data = validated_data.pop('activity')
        prices_data = activity_data.pop('prices', [])
        food_data = activity_data.pop('food', [])
        transport_data = activity_data.pop('transport', [])
        suitable_for_data = activity_data.pop('suitable_for', [])
        allowed_data = activity_data.pop('allowed', [])
        not_allowed_data = activity_data.pop('not_allowed', [])
        includes_data = activity_data.pop('includes', [])
        not_includes_data = activity_data.pop('not_includes', [])
        highlights_data = activity_data.pop('highlights', [])

        activity = Activity.objects.create(**activity_data)

        for price_data in prices_data:
            Price.objects.create(activity=activity, **price_data)

        activity.food.set(food_data)
        activity.transport.set(transport_data)
        for allowed_item in allowed_data:
            Allowed.objects.create(activity=activity, **allowed_item)

        for not_allowed_item in not_allowed_data:
            NotAllowed.objects.create(activity=activity, **not_allowed_item)

        for includes_item in includes_data:
            Includes.objects.create(activity=activity, **includes_item)

        for not_includes_item in not_includes_data:
            NotIncludes.objects.create(activity=activity, **not_includes_item)

        for highlight_item in highlights_data:
            Highlights.objects.create(activity=activity, **highlight_item)
       
        return DailyActivity.objects.create(activity=activity, **validated_data)
   
    def update(self, instance, validated_data):
        instance.activity = validated_data.get('activity', instance.activity)
        instance.activity_date = validated_data.get('activity_date', instance.activity_date)
        instance.start_hour = validated_data.get('start_hour', instance.start_hour)
        instance.end_hour = validated_data.get('end_hour', instance.end_hour)
        # Update other fields similarly
 
        instance.save()
        return instance
