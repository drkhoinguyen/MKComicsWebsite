from django import forms
from mkcomics.normalpage.models import * 
from django.forms import ModelForm

class UserForm(forms.Form):
	name = forms.CharField(max_length = 30)
	mobile = forms.CharField(max_length = 13)
	SSN = forms.CharField(max_length = 9)
	bankcode = forms.CharField(max_length = 15)	
		