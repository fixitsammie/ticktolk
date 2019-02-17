from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ticktolk.views.home', name='home'),
                     url(r'^list/$', 'forum.views.list', name='list'),  
url(r'^$', 'forum.views.home', name='home'),
     url(r'^accounts/', include('password_reset.urls')),
	
     url(r'',include('myregistration.urls')),
url(r'^search/$','forum.views.search',name='search'),

url(r'^category/new/$','forum.views.new_category',name='new_category'),
url(r'^category/(?P<slug>[-\w]+)/$','forum.views.get_category',name='get_category'),

url(r'^category/(?P<pk>\d+)/new-topic/$','forum.views.new_thread',name='new_thread'),

url(r'^topics/(?P<slug>[-\w]+)/edit/$','forum.views.edit_thread',name='edit_thread'),
url(r'^topics/(?P<slug>[-\w]+)/$','forum.views.get_thread',name='get_thread'),

url(r'^topics/(\w*)/post/add/$','forum.views.add_post',name='add_post'),
url(r'^topics/(\w*)/quote/$','forum.views.quote_thread',name='quote_thread'),
url(r'^topics/(\w*)/delete/$','forum.views.delete_thread',name='delete_thread'),
    url(r'^admin/', include(admin.site.urls)),
                       
url(r'^(?P<username>\w+)/$','forum.views.user_page',name='user_page'),
                       url(r'^(?P<username>\w+)/edit/$','forum.views.edit_user_page',name='edit_user_page'),

             

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
                            url(r'^media/(?P<path>.*)$', 'serve'),
                            
    )
'''
