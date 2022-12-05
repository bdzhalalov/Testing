from django.urls import include, path

from .views import Registration

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', Registration.as_view(), name='registration'),
]