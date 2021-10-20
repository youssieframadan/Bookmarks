from urllib.request import Request, urlopen
from django import forms
from django.db import models
from django.core.files.base import ContentFile
from django.utils.text import slugify
from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','description','url')
        
    
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_exetentions = ['jpg','jpeg']
        exetention = url.rsplit('.',1)[1].lower()
        if exetention not in valid_exetentions:
            raise forms.ValidationError('the given url does not match valid image exetentions.')
        return url
    
    def save(self,force_insert=False,force_update=False,commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extention = image_url.rsplit('.',1)[1].lower()
        image_name = f'{name}.{extention}'
        req = Request(image_url,headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        image.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            image.save()
        return image