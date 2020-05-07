from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update',  views.update_profile, name='update_profile'),
    path('login', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('change-password', auth_views.PasswordChangeView.as_view(
    	template_name='account/change-password.html', success_url='/'), name='change-password'
    ),
    path('password-reset/',
    	 auth_views.PasswordResetView.as_view(
    	 	template_name='account/password-reset.html',
    	 	subject_template_name='account/password-reset-subject.txt',
    	 	email_template_name='account/password-reset-email.html',
    	 ), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
    	template_name='account/password-reset-done.html'), name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    	 template_name='account/password-reset-confirm.html'), name='password-reset-confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
    	template_name='account/password-reset-complete.html'), name='password-reset-complete'),
]
