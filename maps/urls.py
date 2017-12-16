from django.conf.urls import url
from django.urls import path

from maps import views
from .views import index, ReverseGeocode

urlpatterns = [
    path('', views.index, name='index'),
    url('^reverseGeocode/(?P<lat>[-]*\w+[.]*\w+)/(?P<lng>[-]*\w+[.]*\w+)$', ReverseGeocode.as_view(), name='reverse_geocode')
]
