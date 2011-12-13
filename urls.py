from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mkcomics.views.home', name='home'),
    # url(r'^mkcomics/', include('mkcomics.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),	
	url(r'^mkcomics/?', include('mkcomics.normalpage.urls')),
	url(r'^mkcomics/normal/?', include('mkcomics.normalpage.urls')),
	url(r'^mkcomics/customer/?', include('mkcomics.customerpage.urls')),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': 'media'}),
)
urlpatterns += staticfiles_urlpatterns()