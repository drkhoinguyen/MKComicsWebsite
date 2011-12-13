from django import forms
from django.db import models
from django.contrib.auth.models import User
from photologue.models import ImageModel, GalleryUpload
from Image import *
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
import zipfile

class ZipUploadField(models.FileField):
	def __init__(self, *args, ** kwargs):
		self.content_types = kwargs.pop("content_type")
		self.max_upload_size = kwargs.pop("max_upload_size")
		super(ZipUploadField,self).__init__(*args, **kwargs)
	
	def clean(self, *args, **kwargs):
		data = super(ZipUploadField, self).clean(*args, **kwargs)
		file = data.file
		try:
			content_type = file.content_type
			if content_type in self.content_types:
				if file._size > self.max_upload_size:
					raise forms.ValidationError(_('Please keep filesize der %s. Current filesize %s') 
						% (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
			else:
				raise forms.ValidationError(_('Filetype not supported. input: %s.Require: %s') % (content_type, self.content_type[0]))
		except AttributeError:
			pass			
		return data		
			
# Create your models here.
class Comic(models.Model):
	CATEGORY_CHOICES = (('humor', 'Humor'), ('action', 'Action'), ('romantic', 'Romantic'))
	title = models.CharField(max_length = 30)
	author = models.CharField(max_length = 30)
	publisher = models.CharField(max_length = 30)
	description = models.TextField()
	image = models.ImageField(upload_to = 'image/comic/')
	category = models.CharField(max_length = 8, choices = CATEGORY_CHOICES)
	
	def __unicode__(self):
		return self.title
	
class Issue(models.Model):
	comic = models.ForeignKey('Comic')
	episode = models.IntegerField()
	title = models.CharField(max_length = 50)
	ISBN = models.CharField(max_length = 20)
	publishdate = models.DateField(auto_now = True)
	description = models.TextField()
	image = models.ImageField(upload_to = 'image/issue/frontpage')
	file = ZipUploadField(upload_to='image/issue/zipupload/', content_type=['application/zip',], max_upload_size=5242880)
	filename = models.CharField(max_length = 1000, null = True)	
	
	def __unicode__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		super(Issue, self).save(*args, ** kwargs)
		filepath = self.file
		myzipfile = zipfile.ZipFile(filepath, 'r')
		myzipfile.extractall('media/image/issue/extractfile/issue%s' % self.id)
		filenamelist = myzipfile.namelist()
		filelist = ""
		for filename in filenamelist:
			filelist += str(filename) + " "
		
		self.filename = filelist
		myzipfile.close()
		super(Issue, self).save(*args, ** kwargs)
	
class UserProfile(models.Model):
	user = models.ForeignKey(User, unique = True)
	name = models.CharField(max_length = 30)
	mobile = models.CharField(max_length = 13)
	SSN = models.CharField(max_length = 9)
	bankcode = models.CharField(max_length = 15)
	comic = models.ManyToManyField('Comic')
	issue = models.ManyToManyField('Issue')
	
	def __unicode__(self):
		return self.name

User.profile = property(lambda u: PubProfile.objects.get_or_create(user=u)[0])