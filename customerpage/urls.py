from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^home/?$', 'mkcomics.customerpage.views.home'),
	url(r'^/?$', 'mkcomics.customerpage.views.home'),
	url(r'^library/?$', 'mkcomics.customerpage.views.newcomic'),
	url(r'^library/newcomic/?$', 'mkcomics.customerpage.views.newcomic'),
	url(r'^library/newissue/?$', 'mkcomics.customerpage.views.newissue'),
	url(r'^library/humor/?$', 'mkcomics.customerpage.views.humor'),
	url(r'^library/action/?$', 'mkcomics.customerpage.views.action'),
	url(r'^library/romantic/?$', 'mkcomics.customerpage.views.romantic'),
	url(r'^logout/?$', 'mkcomics.customerpage.views.logout_site'),
	url(r'^mycomics/?$', 'mkcomics.customerpage.views.mycomics'),
	url(r'^success/?$', 'mkcomics.customerpage.views.success'),
	url(r'^read/?$', 'mkcomics.customerpage.views.read'),
	url(r'^purchasecomic/?$', 'mkcomics.customerpage.views.purchasecomic'),
	url(r'^purchaseissue/?$', 'mkcomics.customerpage.views.purchaseissue'),
)