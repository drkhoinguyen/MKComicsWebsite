from django.contrib import admin
from django.db import models
from mkcomics.normalpage.models import *
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django import forms

class UserProfileAdmin(admin.ModelAdmin):
	exclude = ('comic', 'issue',)
	
class IssueAdmin(admin.ModelAdmin):
	exclude = ('filename',)
	
admin.site.register(Comic)
admin.site.register(Issue, IssueAdmin)
admin.site.register(UserProfile, UserProfileAdmin)