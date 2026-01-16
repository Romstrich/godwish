# forms.py
from email.policy import default

from django import forms
from django.forms import ClearableFileInput

from .models import Picture, Document, Component


# -----------Заготовка под мультизагрузку
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    '''
    Реализация выбора нескольких файлов
    '''
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


# END--------Заготовка под мультизагрузку

class UpPicture(forms.ModelForm):
    '''
    Выбор Картинок
    '''
    picture = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Picture
        fields = ['name', 'comment', 'picture']


class UpDocument(forms.ModelForm):
    '''
    Выбор документов
    '''
    document = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Document
        fields = ['name', 'comment', 'document']


class UpComponent(forms.ModelForm):
    '''
    Создание компонента
    '''
    docs=MultipleFileField(label='Загрузить документы', required=False)
    images = MultipleFileField(label='Загрузить изображения', required=False)
    class Meta:
        model = Component
        fields = ['name','comment','images','docs','contract']

class OrderAdd(forms.ModelForm):
    '''
    Форма создания непосредственно заказа
    ( ПУНКТ contract по-умолчанию True)
    '''
    docs = MultipleFileField(label='Загрузить документы', required=False)
    images = MultipleFileField(label='Загрузить изображения', required=False)
    class Meta:
        model = Component
        fields = ['name','comment','images','docs','contract']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['contract'].empty_label=None
        self.fields['contract'].initial=True