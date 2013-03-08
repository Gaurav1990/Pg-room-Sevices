from django.forms import ModelForm
from app.models import Ad , UserProfile , Rating

from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.forms.fields import ChoiceField
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

TYPE = ( ('owner', 'owner'),
         ('seeker','seeker'))



class article(ModelForm):
    class Meta:
        model = Ad
        exclude = ('posted_by')

class rate(ModelForm):
    class Meta:
        model = Rating
        exclude = ('posted_by')
        
class reg(forms.Form):
    username = forms.CharField(max_length = 30)
    first_name = forms.CharField(max_length = 30)
    last_name = forms.CharField(max_length = 30)
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput(render_value = True))
    re_password = forms.CharField(widget = forms.PasswordInput(render_value = True))
    address = forms.CharField()
    user_type = forms.ChoiceField(choices = TYPE)


    

