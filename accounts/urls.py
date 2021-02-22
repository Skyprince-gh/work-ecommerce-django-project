from django.urls import path
#from .views import *
from accounts.api.views import *
from knox import views as knox_views

app_name = 'accounts'





urlpatterns = [
    path('', ApiOverview.as_view()),
    path('validate_phone/', ValidatePhone.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
]
