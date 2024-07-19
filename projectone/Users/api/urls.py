# Users/urls.py
"""""
 
from django.db import router
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import CategorySiteViewSet, ClientSignupView, AgencySignupView, GuideOnlyView, GuideProfilePictureUpdateView, GuideSignupView, ItemViewSet, LogoutView, ClientOnlyView, AgencyOnlyView, RegionViewSet , UserLoginView ,UpdateProfilePictureView, WilayatViewSet, items_by_category, wilayat_by_category

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'wilayat', WilayatViewSet)
router.register(r'categories', CategorySiteViewSet)
 
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
    path('', include(router.urls)),
    path('items/category/<str:category>/', items_by_category, name='items_by_category'),
    path('wilayat/category/<str:category>/', wilayat_by_category, name='wilayat_by_category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urls.py
"""
from django import views
from django.urls import path, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import          ActivityDetail, ActivityListAPIView, AgencyBookingsView, BookingCreateView, BookingListView, DailyActivityDetail, DailyActivityList, ItemViewSet   ,ActivityViewSet, OneDayActivityDetail, PublisherActivitiesView  , RegionViewSet, SpecificDurationActivityDetail, UploadPhotosView, WeeklyActivityCreateView, WeeklyActivityDetail, WeeklyActivityListAPIView ,  WilayatViewSet, CategorySiteViewSet, ReviewViewSet, items_by_category, wilayat_by_category
from .views import ClientSignupView, AgencySignupView, GuideOnlyView, GuideProfilePictureUpdateView, GuideSignupView, LogoutView, ClientOnlyView, AgencyOnlyView , UserLoginView 
from .views import DailyActivityCreateView, OneDayActivityCreateView, SpecificDurationActivityCreateView

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'wilayat', WilayatViewSet)
router.register(r'categories', CategorySiteViewSet)
router.register(r'reviews',  ReviewViewSet)
#router.register(r'activities', ActivityViewSet)  # Add the new ActivityViewSet

 
#router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('signup/client/', ClientSignupView.as_view(), name='client_signup'),
  path('signup/agency/', AgencySignupView.as_view(), name='agency_signup'),
   # path('verify-signup/', VerifySignupView.as_view(), name='verify_signup'),
    path('signup/guide/', GuideSignupView.as_view(), name='guide_signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('client/', ClientOnlyView.as_view(), name='client_only'),
    path('agency/', AgencyOnlyView.as_view(), name='agency_only'),
    path('guide/', GuideOnlyView.as_view(), name='guide_only'),
     path('weekly-activities/', WeeklyActivityListAPIView.as_view(), name='weekly-activity-list'),
   # path('activities/', ActivityViewSet.as_view(), name='activities'),
    path('daily-activity/', DailyActivityCreateView.as_view(), name='daily-activity-create'),
    path('weekly-activity/', WeeklyActivityCreateView.as_view(), name='weekly-activity-create'),
    path('one-day-activity/', OneDayActivityCreateView.as_view(), name='one-day-activity-create'),
    path('specific-duration-activity/', SpecificDurationActivityCreateView.as_view(), name='specific-duration-activity-create'),
    path('upload-photos/<int:activity_id>/', UploadPhotosView.as_view(), name='upload-photos'),
    path('update-profile-picture/<int:userid>/', GuideProfilePictureUpdateView.as_view(), name='update_profile_picture'),
      path('activities/', ActivityListAPIView.as_view(), name='activity-list'),
   #  path('activity/<int:activity_id>/', get_activity_detail, name='activity-detail'),
      path('activity/<int:pk>/', ActivityDetail.as_view(), name='activity-detail'),
    path('daily_activity/<int:pk>/', DailyActivityDetail.as_view(), name='daily-activity-detail'),
    path('weekly_activity/<int:activity_id>/', WeeklyActivityDetail.as_view(), name='weekly-activity-detail'),
    path('specific_duration_activity/<int:pk>/', SpecificDurationActivityDetail.as_view(), name='specific-duration-activity-detail'),
    path('one_day_activity/<int:pk>/', OneDayActivityDetail.as_view(), name='one-day-activity-detail'),
    path('', include(router.urls)),
    path('items/category/<str:category>/', items_by_category, name='items_by_category'),
    path('wilayat/category/<str:category>/', wilayat_by_category, name='wilayat_by_category'),
       path('api/dailyactivities/', DailyActivityList.as_view(), name='daily-activities-list'),
         path('create-booking/', BookingCreateView.as_view(), name='create-booking'),
        # path('user-bookings/<int:user_id>/', UserBookingsView.as_view(), name='user-bookings'),
    path('agency-bookings/<int:agency_id>/', AgencyBookingsView.as_view(), name='agency-bookings'),
     path('api/publisher/<int:agency_id>/activities/', PublisherActivitiesView.as_view(), name='publisher-activities'),
     path('api/bookings/publisher/<int:publisher_id>/', BookingListView.as_view(), name='booking-list-by-publisher'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
