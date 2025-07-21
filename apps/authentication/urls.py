from django.urls import path
from . import views

urlpatterns = [
    path('send-email-otp/', views.send_email_otp_view, name='send-email-otp'),
    path('verify-email-otp/', views.verify_email_otp_view, name='verify-email-otp'),
    path('send-mobile-otp/', views.send_mobile_otp_view, name='send-mobile-otp'),
    path('verify-mobile-otp/', views.verify_mobile_otp_view, name='verify-mobile-otp'),
    path('bypass-mobile-verification/', views.bypass_mobile_verification_view, name='bypass-mobile-verification'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),  # Add profile endpoint
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset-password/', views.reset_password_view, name='reset-password'),
    path('change-password/', views.change_password_view, name='change-password'),
]
