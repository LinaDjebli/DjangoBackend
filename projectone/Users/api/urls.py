# Users/urls.py

 
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import ClientSignupView, AgencySignupView, GuideOnlyView, GuideProfilePictureUpdateView, GuideSignupView, LogoutView, ClientOnlyView, AgencyOnlyView , UserLoginView ,UpdateProfilePictureView

urlpatterns = [
    path('signup/client/', ClientSignupView.as_view(), name='client_signup'),
    path('signup/agency/', AgencySignupView.as_view(), name='agency_signup'),
    path('signup/guide/', GuideSignupView.as_view(), name='guide_signup'),
    path('login/',  UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('client/', ClientOnlyView.as_view(), name='client_only'),
    path('agency/', AgencyOnlyView.as_view(), name='agency_only'),
    path('guide/', GuideOnlyView.as_view(), name='guide_only'),
    path('update-profile-picture/<int:userid>/', GuideProfilePictureUpdateView.as_view(), name='update_profile_picture'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urls.py
