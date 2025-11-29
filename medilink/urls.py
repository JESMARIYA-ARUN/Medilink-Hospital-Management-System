from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    # -------------------------
    # Admin Panel
    # -------------------------
    path('admin/', admin.site.urls),

    # -------------------------
    # Root URL → Redirect to Login Page
    # This ensures users always start at the login screen
    # instead of accidentally landing on someone’s dashboard.
    # -------------------------
    path('', RedirectView.as_view(pattern_name='users:login', permanent=False), name='home'),

    # -------------------------
    # App URL Routing
    # Each app manages its own URLs through include()
    # -------------------------
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('patients/', include(('patients.urls', 'patients'), namespace='patients')),
    path('doctors/', include(('doctors.urls', 'doctors'), namespace='doctors')),
    path('appointments/', include(('appointments.urls', 'appointments'), namespace='appointments')),

    # -------------------------
    # Authentication: Password Reset Workflow
    # Django’s built-in password reset views with custom templates
    # -------------------------

    # Step 1: User submits email for reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'
    ), name='password_reset'),

    # Step 2: Email sent confirmation
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    # Step 3: User clicks the link in email and sets a new password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # Step 4: Password reset complete page
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]

