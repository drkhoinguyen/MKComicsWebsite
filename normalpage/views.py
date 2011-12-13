# Create your views here.
from mkcomics.normalpage.models import * 
from mkcomics.normalpage.forms import *
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError

def home(request):
	return render_to_response('normalpage/home.html',
	{},
	context_instance = RequestContext(request))
		
def newcomic(request):
	comic = []
	issue = None
	count = Comic.objects.all().count()
	if count > 5: count = 5
	for i in range(0, count):
		temp = Comic.objects.all().order_by('-id')[i].id
		comic.append(Comic.objects.get(id = temp))
	if request.method =='POST':
		issue = Issue.objects.filter(comic = request.POST.get('comic'))
		
	return render_to_response('normalpage/library.html',
	{'display': 1,'comics':comic, 'issues': issue},
	context_instance = RequestContext(request))
	
def newissue(request):
	issue = []
	count = Issue.objects.all().count()
	if count > 5: count = 5
	for i in range(0, count):
		temp = Issue.objects.all().order_by('-id')[i].id
		issue.append(Issue.objects.get(id = temp))
		
	return render_to_response('normalpage/library.html',
	{'display':2, 'issues': issue},
	context_instance = RequestContext(request))
	
def humor(request):
	comic = Comic.objects.filter(category = 'humor')
	issue = None
	if request.method == 'POST':
		issue = Issue.objects.filter(comic = request.POST.get('comic'))
	return render_to_response('normalpage/library.html',
	{'comics': comic, 'issues': issue, 'display': 4, },
	context_instance = RequestContext(request))

def action(request):
	comic= Comic.objects.filter(category = 'action')
	issue = None
	if request.method == 'POST':
		issue = Issue.objects.filter(comic = request.POST.get('comic'))
	return render_to_response('normalpage/library.html',
	{'comics': comic, 'issues': issue, 'display':3},
	context_instance = RequestContext(request))
	
def romantic(request):
	comic = Comic.objects.filter(category = 'romantic')
	issue = None
	if request.method == 'POST':
		issue = Issue.objects.filter(comic = request.POST.get('comic'))
	return render_to_response('normalpage/library.html',
	{'comics': comic, 'issues': issue, 'display': 5},
	context_instance = RequestContext(request))
	
def login_site(request):
	error = ""
	if request.method == 'POST':	
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/mkcomics/customer/home')
			else:
				error = "you are currently disabled"
		else:
			error = "Your username and password didn't match. Please try again"
	return render_to_response('normalpage/login.html',
	{'errornotice':error},
	context_instance = RequestContext(request))
	
def register(request):
	error = ""
	form = UserForm()
	if request.method == 'POST':	
		username = request.POST.get('username')
		try:
			u = User.objects.get(username = username)
		except User.DoesNotExist, e:	
			password = request.POST.get('password')
			confirmpassword = request.POST.get('confirmpassword')
			if password != confirmpassword:
				error = "password and confirmpassword is not the same"
			else: 
				email = request.POST.get('email')			
				try:
					u = User.objects.get(email = email)
				except User.DoesNotExist, e:							
					form = UserForm(request.POST)					
					if form.is_valid():
						user = User.objects.create_user(username, email,  password)	
						user.save()
						name = form.cleaned_data['name']				
						mobile = form.cleaned_data['mobile']
						SSN = form.cleaned_data['SSN']
						bankcode = form.cleaned_data['bankcode']
						userprofile = UserProfile(user = User.objects.get(username = username),
													name = name, mobile = mobile, SSN = SSN, bankcode = bankcode)
						userprofile.save()
						return HttpResponseRedirect('/mkcomics/normal/success')	
				else:		
					error = "This email had been used by another user. Please try another."
		else:
			error = "This user name is exist. Please try another one"
	return render_to_response('normalpage/register.html',
	{'errornotice': error, 'form':form},
	context_instance = RequestContext(request))
	
def success(request):
	return render_to_response('normalpage/success.html',
	{},
	context_instance = RequestContext(request))
