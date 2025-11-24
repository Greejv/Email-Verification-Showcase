from django.urls import path
from .views import send_email, verify_token


urlpatterns = [
    path('verification/send/', send_email, name='send_email'),
    path('verification/verify/', verify_token, name='verify_token')
]