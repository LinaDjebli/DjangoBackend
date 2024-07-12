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
from .views import        ItemViewSet   ,ActivityViewSet  , RegionViewSet,  WilayatViewSet, CategorySiteViewSet, ReviewViewSet, items_by_category, wilayat_by_category
from .views import ClientSignupView, AgencySignupView, GuideOnlyView, GuideProfilePictureUpdateView, GuideSignupView, LogoutView, ClientOnlyView, AgencyOnlyView , UserLoginView 
router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'wilayat', WilayatViewSet)
router.register(r'categories', CategorySiteViewSet)
router.register(r'reviews', ReviewViewSet)
 
router.register(r'activities', ActivityViewSet)
 
#router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('signup/client/', ClientSignupView.as_view(), name='client_signup'),
    path('signup/agency/', AgencySignupView.as_view(), name='agency_signup'),
    path('signup/guide/', GuideSignupView.as_view(), name='guide_signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('client/', ClientOnlyView.as_view(), name='client_only'),
    path('agency/', AgencyOnlyView.as_view(), name='agency_only'),
    path('guide/', GuideOnlyView.as_view(), name='guide_only'),
    path('update-profile-picture/<int:userid>/', GuideProfilePictureUpdateView.as_view(), name='update_profile_picture'),
    path('', include(router.urls)),
    path('items/category/<str:category>/', items_by_category, name='items_by_category'),
    path('wilayat/category/<str:category>/', wilayat_by_category, name='wilayat_by_category'),
   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
