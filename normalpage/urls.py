from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^home/?$', 'mkcomics.normalpage.views.home'),
	url(r'^/?$', 'mkcomics.normalpage.views.home'),
	url(r'^library/?$', 'mkcomics.normalpage.views.newcomic'),
	url(r'^library/newcomic/?$', 'mkcomics.normalpage.views.newcomic'),
	url(r'^library/newissue/?$', 'mkcomics.normalpage.views.newissue'),
	url(r'^library/humor/?$', 'mkcomics.normalpage.views.humor'),
	url(r'^library/action/?$', 'mkcomics.normalpage.views.action'),
	url(r'^library/romantic/?$', 'mkcomics.normalpage.views.romantic'),
	url(r'^login/?$', 'mkcomics.normalpage.views.login_site'),
	url(r'^register/?$', 'mkcomics.normalpage.views.register'),
	url(r'^success/?$', 'mkcomics.normalpage.views.success'),
)