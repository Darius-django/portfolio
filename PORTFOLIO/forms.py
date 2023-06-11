from django import forms
from django.core.validators import EmailValidator
from .models import Contact, Comment
from .models import ScrapData

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['name','email','projectDetails']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
            }),
            'projectDetails': forms.Textarea(attrs={
                'placeholder': 'Enter your message',
                'cols':5,
                'rows':5,
            }),
        }

############coments bblock here#########
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body','post')
        widgets = {
            'post': forms.HiddenInput,
        }

#--------------scrap form here-------------
class ScrapDataForm(forms.ModelForm):
    class Meta:
        model = ScrapData
        fields = ['title', 'url']