from django.forms import DateField
from rest_framework import serializers 
from Users.models import CustomUser, Client, Agency, Guide, validate_pdf  ,LANGUAGE_CHOICES , Language
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
