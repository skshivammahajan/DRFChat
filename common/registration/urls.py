from django.conf.urls import url

from registration import views

urlpatterns = [
    url(r'^register/$', views.UserRegistrationView.as_view(), name='user-registration'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^change-password/$', views.PasswordChangeView.as_view(), name='password-change'),
    url(r'^password/reset/$', views.PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^resend/$', views.ResendVerifyEmailView.as_view(), name='resend_email'),
]
