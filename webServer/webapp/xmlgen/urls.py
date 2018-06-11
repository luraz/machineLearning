from django.conf.urls import url

from . import views

urlpatterns = [
	url('getXml', views.index2, name='index2'),
	url('', views.index, name='index'),
	
]