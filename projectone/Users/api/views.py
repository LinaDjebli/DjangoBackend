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
from Users.models import CustomUser , Agency
from .serializers import ClientSignupSerializer, AgencySignupSerializer, GuideProfilePictureUpdateSerializer, GuideSignupSerializer, UserSerialier
from .permissions import IsClientUser, IsAgencyUser, IsGuideUser
from rest_framework.parsers import MultiPartParser, FormParser
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
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
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
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
 
 

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
        # Get the raw JSON data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        email = data.get('email')
        password = data.get('password')
        
        # Check if email and password are provided
        if email and password:
            try:
                # Get the user object from the database
                user = CustomUser.objects.get(email=email)
                
                if not user.is_active:
                    return JsonResponse({'status': 'error', 'message': 'User not allowed yet'}, status=403)
                
                if user.check_password(password):
                    # User is authenticated, specify the backend and log the user in
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                   
                    return JsonResponse({'status': 'success', 'message': 'Login successful', 'user_id': user.id}, status=201)
                else:
                    # Password verification failed
                    return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=406)
            except CustomUser.DoesNotExist:
                # User with the provided email does not exist
                return JsonResponse({'status': 'error', 'message': 'Email not found'}, status=404)
        else:
            # Email or password not provided
            return JsonResponse({'status': 'error', 'message': 'Please provide both email and password'}, status=400)

        # Return a bad request response if the request method is not POST
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