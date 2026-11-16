from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    # Profile Photo Upload
    path(
        'upload-profile-photo/',
        views.upload_profile_photo,
        name='upload_profile_photo'
    ),

    # Remove Profile Photo
    path(
        'remove-profile-photo/',
        views.remove_profile_photo,
        name='remove_profile_photo'
    ),

    # Forgot Password
    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url='/accounts/forgot-password/done/'
        ),
        name='password_reset'
    ),

    # Password Reset Email Sent
    path(
        'forgot-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Reset Password
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # Password Reset Complete
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # Change Password
    path(
        'change-password/',
        views.change_password_view,
        name='change_password'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),
]