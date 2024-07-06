from django import forms
from .models import Guide

class ProfilePictureUpdateForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['guide_profile_picture']
