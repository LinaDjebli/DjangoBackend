from django import forms
from .models import Guide 

class ProfilePictureUpdateForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['guide_profile_picture']


from django import forms
from .models import Upload

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['name', 'description', 'title', 'image', 'file']


"""""
class ActivityImageForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }
"""