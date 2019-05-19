from django.urls import re_path
from .views import DeviceListView, DeviceDetailView

urlpatterns = [
    re_path(r'devices/(?P<emp_pk>[a-z0-9-]+)/(?P<device_pk>[a-z0-9-]+)/$',DeviceDetailView.as_view() ),
    re_path(r'devices/(?P<pk>[a-z0-9-]+)/$', DeviceListView.as_view(),name="device-detail"),
]
