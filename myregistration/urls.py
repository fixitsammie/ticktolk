from django.conf.urls import patterns, url

from django.contrib.auth import views as auth_views
urlpatterns=patterns('myregistration.views',
    url(r'^register/$','register_page',{"template_name":"registration/register.html"},name="register" ),
    url(r'^login/$','login_request',{"template_name":"registration/login.html"}, name="login"),
    url(r'^logout/$','logout_request' ,name="logout"),
    
                  
)



urlpatterns += patterns('',
                       
                       url(r'^password/change/$',
                           auth_views.password_change,name='auth_password_change'),
                       url(r'^password/change/done/$',
                           auth_views.password_change_done,
                           name='auth_password_change_done'),
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           name='password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='auth_password_reset_confirm'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='auth_password_reset_complete'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='auth_password_reset_done'),
)
