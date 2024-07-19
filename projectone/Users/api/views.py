# Users/api/views.py
import json
from urllib import request
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from Users.models import Activity, Booking, Client, CustomUser , Agency, OneDayActivity, Photos, SpecificDurationActivity, TemporaryAgencySignup, WeeklyActivity
from Users.forms import UploadForm
from Users.utils import send_verification_code
from .serializers import ActivitySerializer, BookingSerializer, ClientSignupSerializer, AgencySignupSerializer, GuideProfilePictureUpdateSerializer, GuideSignupSerializer, HighlightsSerializer, IncludesSerializer, NotAllowedSerializer, NotIncludesSerializer, NotSuitableForSerializer, OneDayActicitySerializer, PriceSerializer, SpeceficDurationActicitySerializer, UserSerialier, WeeklyActivitySerializer
from .permissions import IsClientUser, IsAgencyUser, IsGuideUser
from rest_framework.parsers import MultiPartParser, FormParser ,JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
import json
  


from rest_framework_simplejwt.tokens import RefreshToken

class ClientSignupView(APIView):
    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user_id": user.id  # Return user ID along with the response
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AgencySignupView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = AgencySignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Registration request submitted. Awaiting approval.",
                "user_id": user.id,  # Include the user ID in the response
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
"""
class AgencySignupView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = AgencySignupSerializer(data=request.data)
        if serializer.is_valid():
            temp_signup = serializer.save()
            verification_code = send_verification_code(temp_signup.agency_phone_number)
            temp_signup.verification_code = verification_code
            temp_signup.save()
            return Response({"message": "Verification code sent to your phone."}, status=status.HTTP_201_CREATED)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
class VerifySignupView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')

        try:
            temp_signup = TemporaryAgencySignup.objects.get(agency_phone_number=phone_number, verification_code=verification_code)
            user = CustomUser.objects.create(
                username=temp_signup.username,
                email=temp_signup.agency_email,
                is_active=True
            )
            user.set_password(temp_signup.password)
            user.is_agency = True
            user.save()

            agency = Agency.objects.create(
                user=user,
                agency_name=temp_signup.agency_name,
                agency_email=temp_signup.agency_email,
                password=temp_signup.password,
                agency_phone_number=temp_signup.agency_phone_number,
                agency_website=temp_signup.agency_website,
                number_of_employees=temp_signup.number_of_employees,
                agency_location=temp_signup.agency_location,
                agency_licenses=temp_signup.agency_licenses,
                agency_profile_picture=temp_signup.agency_profile_picture
            )

            temp_signup.delete()

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Registration successful.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except TemporaryAgencySignup.DoesNotExist:
            return Response({"message": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
 
 
"""""

class GuideSignupView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Retrieve guide_languages from form data
       

        serializer = GuideSignupSerializer(data=request.data)
        if serializer.is_valid():
            # Save serializer with guide_languages passed as keyword argument
            serializer.save()
            return Response({"message": "Registration request submitted. Awaiting approval."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# views.py

from .serializers import ProfilePictureUpdateSerializer

class UpdateProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            agency = Agency.objects.get(user=request.user)
        except Agency.DoesNotExist:
            return Response({"message": "Agency not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfilePictureUpdateSerializer(agency, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile picture updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

 
 
 

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)

                if not user.is_active:
                    return JsonResponse({'status': 'error', 'message': 'User not allowed yet'}, status=403)

                if user.check_password(password):
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)

                    # Include user role information in the response
                    response_data = {
                        'status': 'success',
                        'message': 'Login successful',
                        'user_id': user.id,
                        'is_guide': user.is_guide,
                        'is_agency': user.is_agency,
                        'is_client': user.is_client
                    }

                    return JsonResponse(response_data, status=201)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=406)
            except CustomUser.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Email not found'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Please provide both email and password'}, status=400)

        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

class ClientOnlyView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated & IsClientUser]
    serializer_class = UserSerialier
    def get_object(self):
        return self.request.user

class AgencyOnlyView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated & IsAgencyUser]
   
    serializer_class = UserSerialier
    def get_object(self):
        return self.request.user

class GuideOnlyView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated & IsGuideUser]
    serializer_class = UserSerialier
    def get_object(self):
        return self.request.user


#class FileUploadView(APIView):
 #   parser_classes = (MultiPartParser, FormParser)

  #  def post(self, request, *args, **kwargs):
   #     file_obj = request.FILES['file']
    #    description = request.data.get('description')
        # Save file or process it here
     #   with open(file_obj.name, 'wb+') as destination:
      #      for chunk in file_obj.chunks():
       #         destination.write(chunk)
        #return Response({'message': 'File uploaded successfully'}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
 

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from Users.models import Guide
from .serializers import GuideProfilePictureUpdateSerializer

class GuideProfilePictureUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, userid):
        try:
            guide = Guide.objects.get(user_id=userid)  # Assuming 'user_id' is the correct field name
        except Guide.DoesNotExist:
            return Response({"error": "Guide not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GuideProfilePictureUpdateSerializer(guide, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile picture updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





from rest_framework import viewsets
from rest_framework import serializers
from Users.models import Item, Region, Wilayat, CategorySite , Review
from .serializers import ItemSerializer, RegionSerializer, WilayatSerializer, CategorySiteSerializer
from django.shortcuts import redirect, render

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class WilayatViewSet(viewsets.ModelViewSet):
    queryset = Wilayat.objects.all()
    serializer_class = WilayatSerializer

class CategorySiteViewSet(viewsets.ModelViewSet):
    queryset = CategorySite.objects.all()
    serializer_class = CategorySiteSerializer
    

def items_by_category(request, category, wilaya=None):
    items = Item.objects.filter(category__category=category)
    if wilaya:
        items = items.filter(wilaya__name=wilaya)  # Adjust the field name accordingly
    return render(request, 'items_list.html', {'items': items})

from rest_framework import viewsets

from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
 


def wilayat_by_category(request, category):
    wilayat = Wilayat.objects.filter(category__category=category).distinct()
    return render(request, 'wilayat_list.html', {'wilayat': wilayat})





def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')
   
from rest_framework import generics
from rest_framework.response import Response
from Users.models import DailyActivity, OneDayActivity, SpecificDurationActivity
from .serializers import DailyActivitySerializer, OneDayActicitySerializer, SpeceficDurationActicitySerializer

from rest_framework import generics
from Users.models import DailyActivity
from .serializers import DailyActivitySerializer



class DailyActivityCreateView(APIView):
    def post(self, request):
        serializer = DailyActivitySerializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response({"activity_id": activity.activity_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OneDayActivityCreateView(APIView):
   def post(self, request):
        serializer = OneDayActicitySerializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response({"activity_id": activity.activity_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecificDurationActivityCreateView(APIView):
    def post(self, request):
        serializer = SpeceficDurationActicitySerializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response({"activity_id": activity.activity_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WeeklyActivityCreateView(APIView):
    def post(self, request):
        serializer = WeeklyActivitySerializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response({"activity_id": activity.activity_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

class ActivityViewSet(APIView):
    def post(self, request):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response({"activity_id": activity.activity_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadPhotosView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, activity_id):
        try:
            activity = Activity.objects.get(pk=activity_id)  # Ensure you use 'pk' for primary key lookup
        except Activity.DoesNotExist:
            return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
        
        file = request.FILES.get('File')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        Photos.objects.create(activity=activity, File=file)
        
        return Response({"message": "Photo uploaded successfully"}, status=status.HTTP_201_CREATED)

"""""
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = DailyActivity.objects.all()
    serializer_class = DailyActivitySerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)  # For handling file uploads and form data

    def perform_create(self, serializer):
        images_data = self.request.FILES.getlist('images')
        prices_data = self.request.data.get('prices')  # Ensure to retrieve as JSON object, assuming it's passed this way

        activity = serializer.save()

        # Save images
        for image_data in images_data:
            Photos.objects.create(activity=activity, image=image_data)

        # Save prices
        price_serializer = PriceSerializer(data=prices_data, many=True)
        if price_serializer.is_valid():
            price_serializer.save(activity=activity)
        else:
            # Handle serializer validation errors for prices_data
            pass

    def perform_update(self, serializer):
        images_data = self.request.FILES.getlist('images')
        prices_data = self.request.data.get('prices')  # Ensure to retrieve as JSON object, assuming it's passed this way

        instance = serializer.save()

        # Update images
        for image_data in images_data:
            Photos.objects.create(activity=instance, image=image_data)

        # Update prices
        price_serializer = PriceSerializer(instance.prices.all(), data=prices_data, many=True)
        if price_serializer.is_valid():
            price_serializer.save()
        else:
            # Handle serializer validation errors for prices_data
            pass

 
from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
 

 """
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Users.models import Activity, CustomUser, Price, NotSuitableFor, NotAllowed, Includes, NotIncludes, Highlights
from .serializers import ActivitySerializer
"""""
@api_view(['GET'])
def get_activity_detail(request, activity_id):
    try:
        activity = Activity.objects.get(activity_id=activity_id)
        activity_data = ActivitySerializer(activity).data

        # Fetch related data
        prices = Price.objects.filter(activity=activity)
        suitable_for = NotSuitableFor.objects.filter(activity=activity)
        not_allowed = NotAllowed.objects.filter(activity=activity)
        includes = Includes.objects.filter(activity=activity)
        not_includes = NotIncludes.objects.filter(activity=activity)
        highlights = Highlights.objects.filter(activity=activity)
        publisher = CustomUser.objects.get(id=activity.published_by.id)
        
        # Add related data to activity_data
        activity_data['prices'] = PriceSerializer(prices, many=True).data
        activity_data['suitable_for'] = NotSuitableForSerializer(suitable_for, many=True).data
        activity_data['not_allowed'] = NotAllowedSerializer(not_allowed, many=True).data
        activity_data['includes'] = IncludesSerializer(includes, many=True).data
        activity_data['not_includes'] = NotIncludesSerializer(not_includes, many=True).data
        activity_data['highlights'] = HighlightsSerializer(highlights, many=True).data
        activity_data['published_by'] = publisher.username

        # Fetch activity-specific details
        if hasattr(activity, 'weekly_activity'):
            activity_data['activity_detail'] = WeeklyActivitySerializer(activity.weekly_activity).data
        elif hasattr(activity, 'dailyactivity'):
            activity_data['activity_detail'] = DailyActivitySerializer(activity.dailyactivity).data
        elif hasattr(activity, 'specificdurationactivity'):
            activity_data['activity_detail'] = SpeceficDurationActicitySerializer(activity.specificdurationactivity).data
        elif hasattr(activity, 'onedayactivity'):
            activity_data['activity_detail'] = OneDayActicitySerializer(activity.onedayactivity).data

        return Response(activity_data, status=status.HTTP_200_OK)
    except Activity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"""
class ActivityDetail(generics.RetrieveAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class DailyActivityDetail(generics.RetrieveAPIView):
    queryset = DailyActivity.objects.all()
    serializer_class = DailyActivitySerializer
class WeeklyActivityDetail(generics.ListAPIView):
    serializer_class = WeeklyActivitySerializer

    def get_queryset(self):
        activity_id = self.kwargs['activity_id']  # Assuming 'activity_id' is passed in the URL
        return WeeklyActivity.objects.filter(activity_id=activity_id)
class SpecificDurationActivityDetail(generics.RetrieveAPIView):
    queryset = SpecificDurationActivity.objects.all()
    serializer_class = SpeceficDurationActicitySerializer

class OneDayActivityDetail(generics.RetrieveAPIView):
    queryset = OneDayActivity.objects.all()
    serializer_class = OneDayActicitySerializer



class ActivityListAPIView(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class WeeklyActivityListAPIView(generics.ListAPIView):
    queryset = WeeklyActivity.objects.all()
    serializer_class = WeeklyActivitySerializer


class DailyActivityList(APIView):
    def get(self, request):
        activities = DailyActivity.objects.all()
        serializer = DailyActivitySerializer(activities, many=True)
        return Response(serializer.data)
 
 
class BookingCreateView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return Response({
                "message": "Booking created successfully", 
                "booking_id": booking.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AgencyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
  #  permission_classes = [IsAuthenticated]

    def get_queryset(self):
        agency_id = self.kwargs['agency_id']
        return Booking.objects.filter(activity__published_by_id=agency_id)    

 
class PublisherActivitiesView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    #permission_classes = [IsAuthenticated]  # Adjust permissions as needed

    def get_queryset(self):
        # Get agency ID from URL parameter or request data
        agency_id = self.kwargs.get('agency_id')  # Adjust this based on your URL structure
        return Activity.objects.filter(published_by_id=agency_id)
    

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        publisher = self.kwargs['publisher_id']
        return Booking.objects.filter(activity__published_by_id=publisher)    