from django.urls import path, include
from .views import UserLoginView, UserLogoutView, UserRegistrationView, EmailVerificationView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify_email/<str:email>/', EmailVerificationView.as_view(), name='verify_email'),
]