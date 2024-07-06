from django.contrib import admin
from .models import CustomUser , Client , Agency, Guide 
from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.http import HttpResponse
from django.conf import settings
import os



# Register Client, Guide, and CustomUser Admin
admin.site.register(Client)
 
from django.contrib import admin
from .models import Guide

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('guide_first_name', 'guide_last_name', 'guide_email')
    search_fields = ('guide_first_name', 'guide_last_name', 'guide_email')
    list_filter = ('guide_gender', 'guide_languages')
    def download_license(self, obj):
        if obj.guide_licenses:
            return format_html('<a href="{}" download>Download</a>', obj.guide_licenses.url)
        return 'No file'
    download_license.allow_tags = True
    download_license.short_description = 'License'

    def view_folder(self, obj):
        url = reverse('admin:guide_folder', args=[obj.id])
        return format_html('<a href="{}">View Folder</a>', url)
    view_folder.short_description = 'Folder'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('folder/<int:agency_id>/', self.admin_site.admin_view(self.view_guide_folder), name='agency_folder'),
        ]
        return custom_urls + urls

    def view_guide_folder(self, request, guide_id):
        agency = self.get_object(request, guide_id)
        folder_path = os.path.join(settings.MEDIA_ROOT, 'licenses', str(guide_id))

        if os.path.exists(folder_path):
            folder_contents = os.listdir(folder_path)
            content_html = '<br>'.join(folder_contents)
        else:
            content_html = 'Folder is empty or does not exist.'

        return HttpResponse(f'<h2>{Guide.guide_first_name} Folder Contents</h2><p>{content_html}</p>')
    fieldsets = (
        (None, {
            'fields': ('user', 'guide_email', 'guide_first_name', 'guide_last_name', 'guide_gender', 'guide_languages', 'guide_dateofbirth', 'guide_phone_number', 'guide_website', 'guide_location', 'guide_licenses', 'guide_profile_picture', 'guide_description')
        }),
        
    )


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from .models import CustomUser

@admin.action(description='Approve selected users')
def approve_users(modeladmin, request, queryset):
    for user in queryset:
        user.is_active = True
        user.save()

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_client', 'is_agency', 'is_guide', 'is_active')
    list_filter = ('is_client', 'is_agency', 'is_guide', 'is_active')
    actions = [approve_users]


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['agency_name', 'agency_email', 'download_license', 'view_folder']

    def download_license(self, obj):
        if obj.agency_licenses:
            return format_html('<a href="{}" download>Download</a>', obj.agency_licenses.url)
        return 'No file'
    download_license.allow_tags = True
    download_license.short_description = 'License'

    def view_folder(self, obj):
        url = reverse('admin:agency_folder', args=[obj.id])
        return format_html('<a href="{}">View Folder</a>', url)
    view_folder.short_description = 'Folder'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('folder/<int:agency_id>/', self.admin_site.admin_view(self.view_agency_folder), name='agency_folder'),
        ]
        return custom_urls + urls

    def view_agency_folder(self, request, agency_id):
        agency = self.get_object(request, agency_id)
        folder_path = os.path.join(settings.MEDIA_ROOT, 'licenses', str(agency_id))

        if os.path.exists(folder_path):
            folder_contents = os.listdir(folder_path)
            content_html = '<br>'.join(folder_contents)
        else:
            content_html = 'Folder is empty or does not exist.'

        return HttpResponse(f'<h2>{agency.agency_name} Folder Contents</h2><p>{content_html}</p>')