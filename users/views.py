from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomRegisterForm, CustomPasswordChangeForm, CustomProfileForm
from django.contrib.auth import update_session_auth_hash


# ---------------------------------------------------------
# USER LOGIN VIEW
# Handles authentication and redirects users to dashboard
# ---------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user credentials
        user = authenticate(request, username=username, password=password)

        # If credentials are valid → login and redirect to dashboard
        if user is not None:
            login(request, user)
            return redirect("users:dashboard")
        else:
            messages.error(request, "Invalid username or password")

    # Render login page (GET request or failed login)
    return render(request, "users/login.html")



# ---------------------------------------------------------
# USER REGISTRATION VIEW
# Allows creation of new accounts using custom form
# ---------------------------------------------------------
def register_view(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)

        # Validate registration form
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("users:login")  # Redirect to login page after success
    else:
        form = CustomRegisterForm()

    return render(request, "users/register.html", {"form": form})



# ---------------------------------------------------------
# LOGOUT VIEW
# Logs out the current user and redirects to login page
# ---------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect("users:login")



# ---------------------------------------------------------
# DASHBOARD REDIRECT VIEW
# Checks user role and loads corresponding dashboard
# ---------------------------------------------------------
@login_required
def dashboard(request):
    # Redirect patient → patient dashboard
    if request.user.role == "patient":
        return render(request, "patients/dashboard.html")

    # Redirect doctor → doctor dashboard
    elif request.user.role == "doctor":
        return render(request, "doctors/dashboard.html")

    # Fallback for invalid roles
    else:
        messages.error(request, "Invalid user role. Please contact admin.")
        return redirect("users:login")



# ---------------------------------------------------------
# GLOBAL PROFILE VIEW (Not used for doctor/patient profiles)
# Loads and updates profile common to all users
# ---------------------------------------------------------
@login_required
def profile(request):
    user = request.user

    # Load forms with existing user data
    form = CustomProfileForm(instance=user)
    pwd_form = CustomPasswordChangeForm(user=user)

    if request.method == "POST":

        # ---------------------------
        # Handle Profile Update
        # ---------------------------
        if "update_profile" in request.POST:
            form = CustomProfileForm(request.POST, request.FILES, instance=user)

            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("users:profile")
            else:
                messages.error(request, "Please fix the errors below.")


        # ---------------------------
        # Handle Password Change
        # ---------------------------
        elif "change_password" in request.POST:
            pwd_form = CustomPasswordChangeForm(user, request.POST)

            if pwd_form.is_valid():
                user = pwd_form.save()

                # Prevent user from being logged out after password change
                update_session_auth_hash(request, user)

                messages.success(request, "Password changed successfully.")
                return redirect("users:profile")
            else:
                messages.error(request, "Please fix the errors below.")

    # Render profile template (currently loads patient profile template)
    context = {
        "form": form,
        "pwd_form": pwd_form,
    }
    
    return render(request, "patients/profile.html", context)
