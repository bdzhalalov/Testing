from django.urls import path

from .views import GroupView, GroupViewDetail

urlpatterns = [
    path('groups/', GroupView.as_view(), name='groups'),
    path('groups/<str:slug>', GroupViewDetail.as_view(), name='group_detail')
]
