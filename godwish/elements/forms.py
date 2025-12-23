# forms.py
from django import forms
from django.forms import ClearableFileInput

from .models import Picture

#-----------Заготовка под мультизагрузку
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
#END--------Заготовка под мультизагрузку

class UpPicture(forms.ModelForm):

    picture = MultipleFileField(label='Select files', required=False)
    class Meta:

        model = Picture
        fields=['name','comment','picture']




# class ImageForm(forms.ModelForm):
#     photo = MultipleFileField(label='Select files', required=False)
#
#     class Meta:
#         model = Image
#         fields = ['photo', ]