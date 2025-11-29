from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.forms import CustomProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from appointments.models import Appointment
from users.models import CustomUser
from django.utils import timezone


# ---------------------------------------------
# DOCTOR DASHBOARD VIEW
# ---------------------------------------------
@login_required
def dashboard(request):
    # Only doctors should access this page
    if request.user.role != "doctor":
        return render(request, "403.html", status=403)

    # Get today's date
    today = timezone.now().date()

    # Count total appointments scheduled for today
    todays_appointments = Appointment.objects.filter(
        doctor=request.user, date=today
    ).count()

    # Count upcoming future appointments
    upcoming_appointments = Appointment.objects.filter(
        doctor=request.user, date__gt=today
    ).count()

    # Count unique patients the doctor has appointments with
    total_patients = Appointment.objects.filter(
        doctor=request.user
    ).values('patient').distinct().count()

    # Send data to the dashboard template
    context = {
        "todays_appointments": todays_appointments,
        "upcoming_appointments": upcoming_appointments,
        "total_patients": total_patients
    }

    return render(request, "doctors/dashboard.html", context)


# ---------------------------------------------
# DOCTOR PROFILE UPDATE + PASSWORD CHANGE VIEW
# ---------------------------------------------
@login_required
def profile(request):
    # Restrict access to doctors only
    if request.user.role != "doctor":
        return render(request, "403.html", status=403)

    # Initialize profile form and password form
    profile_form = CustomProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    # List of fields doctors are allowed to update
    allowed_fields = [
        "username", "email", "first_name", "last_name",
        "specialization", "hospital_contact"
    ]

    # Handle POST actions (profile update or password change)
    if request.method == "POST":

        # --------------------------
        # UPDATE PROFILE DATA
        # --------------------------
        if "update_profile" in request.POST:
            profile_form = CustomProfileForm(
                request.POST,
                request.FILES,
                instance=request.user
            )

            if profile_form.is_valid():
                # Save updated info
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("doctors:profile")
            else:
                messages.error(request, "Please correct the errors below.")

        # --------------------------
        # CHANGE PASSWORD
        # --------------------------
        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(
                user=request.user,
                data=request.POST
            )

            if password_form.is_valid():
                user = password_form.save()

                # Keep user logged in after password change
                update_session_auth_hash(request, user)

                messages.success(request, "Password changed successfully!")
                return redirect("doctors:profile")
            else:
                messages.error(request, "Please correct the errors below.")

    # Send forms + allowed fields to template
    context = {
        "form": profile_form,
        "pwd_form": password_form,
        "allowed_fields": allowed_fields
    }

    return render(request, "doctors/profile.html", context)
