from django.conf.urls import url
from Crypto import views

urlpatterns = [
    url(r'^$', views.say_hello, name='home'),
    url(r'^blog/(?P<mycurr>[\w]+)/$', views.blog, name='blog')
]