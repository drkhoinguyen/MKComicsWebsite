# Create your views here.
from mkcomics.normalpage.models import * 
from mkcomics.normalpage.forms import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
import datetime


LOGIN_URL = '/mkcomics/normal/login'
cartcomic = []
cartissue = []
@login_required(login_url = LOGIN_URL)	
def home(request):
	return render_to_response('customerpage/home.html',
	{'username': request.user.username},
	context_instance = RequestContext(request))

@login_required(login_url = LOGIN_URL)
def purchasecomic(request):
	if request.GET.get('ask') == 'no':
		return HttpResponseRedirect('/mkcomics/customer/library')
	elif request.GET.get('ask') == 'wait':
		cartcomic.append(request.GET.get('comicid'))
		return HttpResponseRedirect('/mkcomics/customer/library')
	elif request.GET.get('ask') == 'yes':
		cartcomic.append(request.GET.get('comicid'))
		userprofile = UserProfile.objects.get(user = request.user)
		for c in cartcomic:
			userprofile.comic.add(Comic.objects.get(id = c))	
			for i in Issue.objects.filter(comic = c):
				userprofile.issue.add(i)
		return email(request)
		
	return render_to_response('customerpage/purchasecomic.html',
	{'username': request.user.username, 'comicid': request.POST.get('comic')},
	context_instance = RequestContext(request)) 
	
@login_required(login_url = LOGIN_URL)
def purchaseissue(request):
	if request.GET.get('ask') == 'no':
		return HttpResponseRedirect('/mkcomics/customer/library')
	elif request.GET.get('ask') == 'wait':
		cartissue.append(request.GET.get('issueid'))
		return HttpResponseRedirect('/mkcomics/customer/library')
	elif request.GET.get('ask') == 'yes':
		cartissue.append(request.GET.get('issueid'))
		userprofile = UserProfile.objects.get(user = request.user)
		for i in cartissue:
			userprofile.issue.add(Issue.objects.get(id = i))
		return email(request)

	return render_to_response('customerpage/purchaseissue.html',
	{'username': request.user.username, 'issueid': request.POST.get('issue')},
	context_instance = RequestContext(request))

@login_required(login_url = LOGIN_URL)
def email(request):	
	subject = "Sending Bill of your account in MKCOMICS.com"
	message = "YOUR CART in MKCOMICS.COM\n"
	money = 0
	now = datetime.datetime.now()
	message += "Date:" + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "\n"
	message += "COMIC TITLE\tPRIZE\n"
	for c in cartcomic:
		money += 100
		comic = Comic.objects.get(id = c)
		message += comic.title + "\t"
		message += "$100\n"
		
	message += "\nISSUE TITLE\tPRIZE\n"
	for i in cartissue:
		money += 5
		issue = Issue.objects.get(id = i)
		message += issue.title + "\t"
		message += "$5\n"
	message += "Your Total bill: $" + str(money) + "\n"
	message += "Thanks for using MKCOMICS.COM. See you later!"		

	send_mail(subject, message, 'ducminhkhoi@gmail.com', [request.user.email])
	return HttpResponseRedirect('/mkcomics/customer/success')

@login_required(login_url = LOGIN_URL)	
def newcomic(request):
	comic = []
	issue = None
	purchase = False;
	purchaseIssue = False;
	comicchoose = None
	count = Comic.objects.all().count()
	if count > 5: count = 5
	for i in range(0, count):
		temp = Comic.objects.all().order_by('-id')[i].id
		comic.append(Comic.objects.get(id = temp))
		
	userprofile = UserProfile.objects.get(user = request.user)
	purchasedcomic = userprofile.comic.all()
	purchasedissue = userprofile.issue.all()
	
	if request.method == 'POST':
		if 'explore' in request.POST:
			issue = Issue.objects.filter(comic = request.POST.get('comic'))
			comicchoose = request.POST.get('comic')
		elif 'purchase' in request.POST:
			return purchasecomic(request)
		elif 'purchaseIssue' in request.POST:
			return purchaseissue(request)

	return render_to_response('customerpage/library.html',
	{'comics':comic, 'issues': issue, 'username': request.user.username, 'purchasedcomic': purchasedcomic, 'purchasedissue': purchasedissue},
	context_instance = RequestContext(request))
	
@login_required(login_url = LOGIN_URL)	
def newissue(request):
	purchaseIssue = False;
	issue = []
	count = Issue.objects.all().count()
	if count > 5: count = 5
	
	for i in range(0, count):
		temp = Issue.objects.all().order_by('-id')[i].id
		issue.append(Issue.objects.get(id = temp))
		
	userprofile = UserProfile.objects.get(user = request.user)
	purchasedcomic = userprofile.comic.all()
	purchasedissue = userprofile.issue.all()
		
	if request.method == 'POST':
		return purchaseissue(request)
		
	return render_to_response('customerpage/library.html',
	{'issues': issue, 'username': request.user.username, 'purchasedcomic': purchasedcomic, 'purchasedissue': purchasedissue},
	context_instance = RequestContext(request))
	
@login_required(login_url = LOGIN_URL)	
def humor(request):
	purchase = False;
	comic = Comic.objects.filter(category = 'humor')
	issue = None
	
	userprofile = UserProfile.objects.get(user = request.user)
	purchasedcomic = userprofile.comic.all()
	purchasedissue = userprofile.issue.all()
	
	if request.method == 'POST':
		if 'explore' in request.POST:
			issue = Issue.objects.filter(comic = request.POST.get('comic'))
		elif 'purchase' in request.POST:
			return purchasecomic(request)
		elif 'purchaseIssue' in request.POST:
			return purchaseissue(request)

	return render_to_response('customerpage/library.html',
	{'comics': comic, 'issues': issue,  'username': request.user.username, 'purchasedcomic': purchasedcomic, 'purchasedissue': purchasedissue},
	context_instance = RequestContext(request))

@login_required(login_url = LOGIN_URL)	
def action(request):
	purchase = False;
	comic= Comic.objects.filter(category = 'action')
	issue = None
	
	userprofile = UserProfile.objects.get(user = request.user)
	purchasedcomic = userprofile.comic.all()
	purchasedissue = userprofile.issue.all()

	if request.method == 'POST':
		if 'explore' in request.POST:
			issue = Issue.objects.filter(comic = request.POST.get('comic'))
		elif 'purchase' in request.POST:
			return purchasecomic(request)
		elif 'purchaseIssue' in request.POST:
			return purchaseissue(request)			
			
	return render_to_response('customerpage/library.html',
	{'comics': comic, 'issues': issue,'username': request.user.username, 'purchasedcomic': purchasedcomic, 'purchasedissue': purchasedissue},
	context_instance = RequestContext(request))
	
@login_required(login_url = LOGIN_URL)	
def romantic(request):
	purchase = False;
	comic = Comic.objects.filter(category = 'romantic')
	issue = None
	
	userprofile = UserProfile.objects.get(user = request.user)
	purchasedcomic = userprofile.comic.all()
	purchasedissue = userprofile.issue.all()

	if request.method == 'POST':
		if 'explore' in request.POST:
			issue = Issue.objects.filter(comic = request.POST.get('comic'))
		elif 'purchase' in request.POST:
			return purchasecomic(request)
		elif 'purchaseIssue' in request.POST:
			return purchaseissue(request)	
			
	return render_to_response('customerpage/library.html',
	{'comics': comic, 'issues': issue, 'username': request.user.username, 'purchasedcomic': purchasedcomic, 'purchasedissue': purchasedissue},
	context_instance = RequestContext(request))
	
@login_required(login_url = LOGIN_URL)
def logout_site(request):
	logout(request)
	return HttpResponseRedirect('/mkcomics/normal/home')
	
@login_required(login_url = LOGIN_URL)
def mycomics(request):
	userprofile = UserProfile.objects.get(user = request.user)
	comic = userprofile.comic.all()
	issue = []
	
	if request.method == 'POST':
		if 'explore' in request.POST:
			issueid = Issue.objects.filter(comic = request.POST.get('comic'))
			for i in userprofile.issue.all():
				if i in issueid:
					issue.append(i)
		elif 'read' in request.POST:
			return read(request)
					
	return render_to_response('customerpage/mycomics.html',
	{'username': request.user.username, 'comics': comic, 'issues': issue},
	context_instance = RequestContext(request))
	
@login_required(login_url = LOGIN_URL)
def read(request):				
	if request.method == 'GET':
		issueid = request.GET.get('issueid')		
		issue = Issue.objects.get(id = issueid)
		issuepage = issue.filename.split(' ')#name of the page
		totalpage = len(issuepage)- 1	
		page = request.GET.get('page')				
		width = request.GET.get('width')
		height = request.GET.get('height')
		
		if 'back' in request.GET:
			if int(page)  - 1< 1: 
				page = 1
			else:
				page = int(page) - 1
				
		elif 'forward' in request.GET:
			if int(page)  + 1> totalpage:
				page = totalpage
			else:
				page = int(page) + 1
				
		elif 'zoomin' in request.GET:
			if int(height) + 80 > 800: 
				height = 800
			else:
				height = int(height) + 80
			if int(width) + 100> 1000:
				width = 1000
			else:
				width = int(width) + 100	
				
		elif 'zoomout' in request.GET:
			if int(height) - 80< 80:
				height = 80
			else:
				height = int(height) - 80
			if int(width) - 100< 100:
				width = 100
			else:
				width = int(width) - 100		
				
		pageimage = "/media/image/issue/extractfile/issue" + str(issue.id) +"/"+ issuepage[int(page) -1]
			
	elif request.method == 'POST':
		issueid = request.POST.get('issue')
		page = 1
		width = 500
		height = 400
		
		issue = Issue.objects.get(id = issueid)
		issuepage = issue.filename.split(' ')#name of the page
		totalpage = len(issuepage) - 1
		pageimage = "/media/image/issue/extractfile/issue" + str(issue.id) + "/" +issuepage[int(page) - 1]
		
	return render_to_response('customerpage/read.html',
	{'username': request.user.username, 'issueid':issueid, 'width': width, 'height': height, 'page': page,
		'pageimage': pageimage, 'totalpage': totalpage},
	context_instance = RequestContext(request))

@login_required(login_url = LOGIN_URL)
def success(request):
	return render_to_response('customerpage/success.html',
	{'username': request.user.username},
	context_instance = RequestContext(request))

	
	
	