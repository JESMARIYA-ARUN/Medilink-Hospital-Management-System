# patients/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.forms import CustomProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from appointments.models import Appointment
from users.models import CustomUser
from django.utils import timezone


# -----------------------------------
# Patient Dashboard View
# Shows appointment stats and doctor count
# -----------------------------------
@login_required
def dashboard(request):
    # Only patients are allowed to access the patient dashboard
    if request.user.role != "patient":
        return render(request, "403.html", status=403)

    today = timezone.now().date()

    # Count all upcoming appointments (today or later)
    upcoming_appointments = Appointment.objects.filter(
        patient=request.user, date__gte=today
    ).count()

    # Count all past appointments (before today)
    past_appointments = Appointment.objects.filter(
        patient=request.user, date__lt=today
    ).count()

    # Count total doctors available in the system
    total_doctors = CustomUser.objects.filter(role="doctor").count()

    context = {
        "upcoming_appointments": upcoming_appointments,
        "past_appointments": past_appointments,
        "total_doctors": total_doctors
    }

    # Render the patient dashboard with all stats
    return render(request, "patients/dashboard.html", context)



# -----------------------------------
# Patient Profile View
# Allows patients to edit profile and change password
# -----------------------------------
@login_required
def profile(request):
    # Only patients can access their own profile settings
    if request.user.role != "patient":
        return render(request, "403.html", status=403)

    # Pre-fill forms with current user data
    profile_form = CustomProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == "POST":
        
        # -------------------------------
        # Handle profile update
        # -------------------------------
        if "update_profile" in request.POST:
            profile_form = CustomProfileForm(
                request.POST, request.FILES, instance=request.user
            )

            # Validate and save updated profile information
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("patients:profile")
            else:
                messages.error(request, "Please correct the errors below.")


        # -------------------------------
        # Handle password change
        # -------------------------------
        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(
                user=request.user, data=request.POST
            )

            if password_form.is_valid():
                user = password_form.save()

                # Prevents logout after password change
                update_session_auth_hash(request, user)

                messages.success(request, "Password changed successfully!")
                return redirect("patients:profile")
            else:
                messages.error(request, "Please correct the errors below.")

    # Render both forms for user interaction
    context = {
        "form": profile_form,
        "pwd_form": password_form,
    }

    return render(request, "patients/profile.html", context)
