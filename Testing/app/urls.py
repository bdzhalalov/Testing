from django.urls import path

from .views import GroupView, GroupViewDetail, TestView, QuestionView

urlpatterns = [
    path('groups/', GroupView.as_view(), name='groups'),
    path('groups/<str:slug>', GroupViewDetail.as_view(), name='group_detail'),
    path('test/<str:slug>', TestView.as_view(), name='test_detail'),
    path('test/<str:slug>/<int:id>', QuestionView.as_view(), name='question')
]
