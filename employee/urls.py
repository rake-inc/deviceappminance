from django.urls import re_path
from .views import EmployeeListView, EmployeeDetailView

urlpatterns = [
    re_path(r'^employees/$', EmployeeListView.as_view()),
    re_path(r'^employees/(?P<pk>[a-z0-9-]+)/$', EmployeeDetailView.as_view(), {'type':'detail'}),
]
