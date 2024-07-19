 
import re
from django.forms import DateField
from rest_framework import serializers 
from Users.models import Booking, Transport,  Food, Highlights, Price,NotSuitableFor, CustomUser, Client, Agency, Guide, OneDayActivity, Photos, SpecificDurationActivity, WeeklyActivity, validate_pdf  ,LANGUAGE_CHOICES , Language
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
   # number_of_employees = serializers.CharField(required=True)
    agency_location = serializers.CharField(required=True)
    agency_licenses = serializers.FileField(required=False)
    agency_profile_picture = serializers.FileField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'agency_name', 'agency_email', 'password' , 'agency_phone_number', 'agency_website', 'agency_location', 'agency_licenses', 'agency_profile_picture']

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
            #number_of_employees=self.validated_data['number_of_employees'],
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
# serializers.py

from rest_framework import serializers
from Users.models import TemporaryAgencySignup

class TempAgencySignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryAgencySignup
        fields = ['username', 'agency_name', 'agency_email', 'password', 'agency_phone_number', 'agency_website', 'number_of_employees', 'agency_location', 'agency_licenses', 'agency_profile_picture']

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


""""
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
 """

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
    Activity, DailyActivity, Price   ,NotSuitableFor  , NotAllowed, 
    Includes, NotIncludes , ActivityCategory, CustomUser
)

 
from rest_framework import serializers
from Users.models import DailyActivity, Activity, Price  , NotAllowed, Includes, NotIncludes  #Highlights
from Users.models import CustomUser

from rest_framework import serializers

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['price_type', 'number_of_clients', 'price']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['food']

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ['transport']

class PhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
      
        model = Photos
        fields = ['File']

class NotSuitableForSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotSuitableFor
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
    notsuitable_for = NotSuitableForSerializer(many=True, required=False)
    guide_name = serializers.CharField(required=False)
    not_allowed = NotAllowedSerializer(many=True, required=False)
    food = FoodSerializer(many=True , required=False) 
    includes = IncludesSerializer(many=True, required=False)
    transport = TransportSerializer(many=True,required=False)
    not_includes = NotIncludesSerializer(many=True, required=False)
    photos = PhotoSerializer(many=True, required=False)
    published_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    highlights = HighlightsSerializer(many=True , required = False)
    

    class Meta:
        model = Activity
        fields = [
            'activity_id','activity_name', 'guide_name', 'activity_category', 'activity_type','food','transport' ,'activity_description',
            'activity_location', 'emergency_phone_number', 'cut_off_time', 'meeting_point', 'groupesize', 
            'dropoff', 'prices', 'notsuitable_for', 'not_allowed', 'includes', 'not_includes', 'highlights', 
            'photos', 'published_by', 'region',
        ]

    def create(self, validated_data):
        prices_data = validated_data.pop('prices', [])
        suitable_for_data = validated_data.pop('notsuitable_for', [])
        not_allowed_data = validated_data.pop('not_allowed', [])
        includes_data = validated_data.pop('includes', [])
        not_includes_data = validated_data.pop('not_includes', [])
        food_data = validated_data.pop('food', [])
        transport_data = validated_data.pop('transport', [])
        highlights_data = validated_data.pop('highlights', [])
        photo_data = validated_data.pop('photos',[])
        activity = Activity.objects.create(**validated_data)

        for price_data in prices_data:
            Price.objects.create(activity=activity, **price_data)
        for  item in photo_data:
            Photos.objects.create(activity=activity, **item)

        for food_datas in food_data:
            Food.objects.create(activity=activity, **food_datas) 

        for transport_datas in transport_data:
            Transport.objects.create(activity=activity, **transport_datas)
        for highlight_item in highlights_data:
           Highlights.objects.create(activity=activity, **highlight_item)

        for suitable_fors_data in suitable_for_data:
            NotSuitableFor.objects.create(activity=activity, **suitable_fors_data)
        for not_allowed_item in not_allowed_data:
            NotAllowed.objects.create(activity=activity, **not_allowed_item)
        for includes_item in includes_data:
            Includes.objects.create(activity=activity, **includes_item)
        for not_includes_item in not_includes_data:
            NotIncludes.objects.create(activity=activity, **not_includes_item)
         
        return activity

    def update(self, instance, validated_data):
        instance.activity_name = validated_data.get('activity_name', instance.activity_name)
        instance.guide_name = validated_data.get('guide_name', instance.guide_name)
        instance.activity_category = validated_data.get('activity_category', instance.activity_category)
        instance.activity_type = validated_data.get('activity_type', instance.activity_type)
        instance.activity_description = validated_data.get('activity_description', instance.activity_description)
        instance.activity_location = validated_data.get('activity_location', instance.activity_location)
        instance.emergency_phone_number = validated_data.get('emergency_phone_number', instance.emergency_phone_number)
        instance.cut_off_time = validated_data.get('cut_off_time', instance.cut_off_time)
        instance.meeting_point = validated_data.get('meeting_point', instance.meeting_point)
        instance.groupesize = validated_data.get('groupesize', instance.groupesize)
        instance.dropoff = validated_data.get('dropoff', instance.dropoff)
        instance.region = validated_data.get('region', instance.region)
        instance.wilaya = validated_data.get('wilaya', instance.wilaya)
        
        instance.save()

        prices_data = validated_data.get('prices', [])
        suitable_for_data = validated_data.get('notsuitable_for', [])
        not_allowed_data = validated_data.get('not_allowed', [])
        includes_data = validated_data.get('includes', [])
        not_includes_data = validated_data.get('not_includes', [])
        
        photo_data = validated_data.get('photos', [])

        for price_data in prices_data:
            Price.objects.update_or_create(activity=instance, **price_data)
        
        for photo in photo_data:
            Photos.objects.update_or_create(activity=instance, **photo)

        for suitable_fors_data in suitable_for_data:
            NotSuitableFor.objects.update_or_create(activity=instance, **suitable_fors_data)
        for not_allowed_item in not_allowed_data:
            NotAllowed.objects.update_or_create(activity=instance, **not_allowed_item)
        for includes_item in includes_data:
            Includes.objects.update_or_create(activity=instance, **includes_item)
        for not_includes_item in not_includes_data:
            NotIncludes.objects.update_or_create(activity=instance, **not_includes_item)
        return instance

class DailyActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = DailyActivity
        fields = ['activity', 'start_hour', 'end_hour']

    def create(self, validated_data):
        activity_data = validated_data.pop('activity')
        prices_data = activity_data.pop('prices', [])
        food_data = activity_data.pop('food', [])
        transport_data = activity_data.pop('transport', [])
        notsuitable_for_data = activity_data.pop('notsuitable_for', [])
        not_allowed_data = activity_data.pop('not_allowed', [])
        includes_data = activity_data.pop('includes', [])
        not_includes_data = activity_data.pop('not_includes', [])
        highlights_data = activity_data.pop('highlights', [])

        activity = Activity.objects.create(**activity_data)

        for price_data in prices_data:
            Price.objects.create(activity=activity, **price_data)
        for food_item in food_data:
            Food.objects.create(activity=activity, **food_item)
        for transport_item in transport_data:
            Transport.objects.create(activity=activity, **transport_item)
        for not_allowed_item in not_allowed_data:
            NotAllowed.objects.create(activity=activity, **not_allowed_item)
        for includes_item in includes_data:
            Includes.objects.create(activity=activity, **includes_item)
        for not_includes_item in not_includes_data:
            NotIncludes.objects.create(activity=activity, **not_includes_item)
        for highlight_item in highlights_data:
            Highlights.objects.create(activity=activity, **highlight_item)
        for suitable_item in notsuitable_for_data:
            NotSuitableFor.objects.create(activity=activity, **suitable_item)

        daily_activity = DailyActivity.objects.create(activity=activity, **validated_data)
        return daily_activity

    def update(self, instance, validated_data):
        # Update fields similarly to the create method
        instance.save()
        return instance


class OneDayActicitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = OneDayActivity
        fields = ['activity', 'activity_date', 'start_hour', 'end_hour']

    def create(self, validated_data):
        activity_data = validated_data.pop('activity')
        prices_data = activity_data.pop('prices', [])
        food_data = activity_data.pop('food', [])
        transport_data = activity_data.pop('transport', [])
        notsuitable_for_data = activity_data.pop('notsuitable_for', [])
        not_allowed_data = activity_data.pop('not_allowed', [])
        includes_data = activity_data.pop('includes', [])
        not_includes_data = activity_data.pop('not_includes', [])
        highlights_data = activity_data.pop('highlights', [])

        activity = Activity.objects.create(**activity_data)

        for price_data in prices_data:
            Price.objects.create(activity=activity, **price_data)
        for food_item in food_data:
            Food.objects.create(activity=activity, **food_item)
        for transport_item in transport_data:
            Transport.objects.create(activity=activity, **transport_item)
        for not_allowed_item in not_allowed_data:
            NotAllowed.objects.create(activity=activity, **not_allowed_item)
        for includes_item in includes_data:
            Includes.objects.create(activity=activity, **includes_item)
        for not_includes_item in not_includes_data:
            NotIncludes.objects.create(activity=activity, **not_includes_item)
        for highlight_item in highlights_data:
            Highlights.objects.create(activity=activity, **highlight_item)
        for suitable_item in notsuitable_for_data:
            NotSuitableFor.objects.create(activity=activity, **suitable_item)

        one_day_activity = OneDayActivity.objects.create(activity=activity, **validated_data)
        return one_day_activity

    def update(self, instance, validated_data):
        # Update fields similarly to the create method
        instance.save()
        return instance


class SpeceficDurationActicitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = SpecificDurationActivity
        fields = ['activity', 'activity_start_date', 'activity_end_date', 'start_hour', 'end_hour']

    def create(self, validated_data):
        activity_data = validated_data.pop('activity')
        prices_data = activity_data.pop('prices', [])
        food_data = activity_data.pop('food', [])
        transport_data = activity_data.pop('transport', [])
        notsuitable_for_data = activity_data.pop('notsuitable_for', [])
        not_allowed_data = activity_data.pop('not_allowed', [])
        includes_data = activity_data.pop('includes', [])
        not_includes_data = activity_data.pop('not_includes', [])
        highlights_data = activity_data.pop('highlights', [])

        activity = Activity.objects.create(**activity_data)

        for price_data in prices_data:
            Price.objects.create(activity=activity, **price_data)
        for food_item in food_data:
            Food.objects.create(activity=activity, **food_item)
        for transport_item in transport_data:
            Transport.objects.create(activity=activity, **transport_item)
        for not_allowed_item in not_allowed_data:
            NotAllowed.objects.create(activity=activity, **not_allowed_item)
        for includes_item in includes_data:
            Includes.objects.create(activity=activity, **includes_item)
        for not_includes_item in not_includes_data:
            NotIncludes.objects.create(activity=activity, **not_includes_item)
        for highlight_item in highlights_data:
            Highlights.objects.create(activity=activity, **highlight_item)
        for suitable_item in notsuitable_for_data:
            NotSuitableFor.objects.create(activity=activity, **suitable_item)

        specific_duration_activity = SpecificDurationActivity.objects.create(activity=activity, **validated_data)
        return specific_duration_activity

    def update(self, instance, validated_data):
        # Update fields similarly to the create method
        instance.save()
        return instance




class WeeklyActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    day = serializers.ListField(child=serializers.CharField())
    start_hour = serializers.TimeField()
    end_hour = serializers.TimeField()

    class Meta:
        model = WeeklyActivity
        fields = ['activity', 'day', 'start_hour', 'end_hour']

    def create(self, validated_data):
        activity_data = validated_data.pop('activity')
        prices_data = activity_data.pop('prices', [])
        food_data = activity_data.pop('food', [])
        transport_data = activity_data.pop('transport', [])
        notsuitable_for_data = activity_data.pop('notsuitable_for', [])
        not_allowed_data = activity_data.pop('not_allowed', [])
        includes_data = activity_data.pop('includes', [])
        not_includes_data = activity_data.pop('not_includes', [])
        highlights_data = activity_data.pop('highlights', [])

        activity = Activity.objects.create(**activity_data)

        for price_data in prices_data:
            Price.objects.create(activity=activity, **price_data)
        for food_item in food_data:
            Food.objects.create(activity=activity, **food_item)
        for transport_item in transport_data:
            Transport.objects.create(activity=activity, **transport_item)
        for not_allowed_item in not_allowed_data:
            NotAllowed.objects.create(activity=activity, **not_allowed_item)
        for includes_item in includes_data:
            Includes.objects.create(activity=activity, **includes_item)
        for not_includes_item in not_includes_data:
            NotIncludes.objects.create(activity=activity, **not_includes_item)
        for highlight_item in highlights_data:
            Highlights.objects.create(activity=activity, **highlight_item)
        for suitable_item in notsuitable_for_data:
            NotSuitableFor.objects.create(activity=activity, **suitable_item)

        weekly_activity = WeeklyActivity.objects.create(activity=activity, **validated_data)
        return weekly_activity

    def update(self, instance, validated_data):
        # Update fields similarly to the create method
        instance.save()
        return instance    
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'firstname', 
            'lastname', 
            'email', 
            'age', 
            'wilaya', 
            'phonenumber', 
            'number_of_tickets', 
            'total_price', 
            'activity', 
            'booking_date', 
            'state'
        ]
        read_only_fields = ['booking_date', 'state']
    def update(self, instance, validated_data):
        # Update fields similarly to the create method
        instance.save()
        return instance    
    