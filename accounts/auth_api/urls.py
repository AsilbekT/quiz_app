from django.urls import path
from accounts.auth_api.views import (
    ObtainAuthToken,
    registration_view

)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('register/', registration_view, name="register"),
    path('login/', ObtainAuthToken.as_view(), name='login'),
]
