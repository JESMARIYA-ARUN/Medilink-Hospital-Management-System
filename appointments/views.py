from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm

@login_required
def appointments_list(request):
    #List appointments based on user role
    if request.user.role == "patient":
        appointments = Appointment.objects.filter(patient=request.user)
    elif request.user.role == "doctor":
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.all()  # Admin or staff

    return render(request, "appointments/list.html", {"appointments": appointments})

@login_required
def appointment_detail(request, id):
    #Show appointment details
    appointment = get_object_or_404(Appointment, id=id)

    # Security check
    if request.user.role == "patient" and appointment.patient != request.user:
        return render(request, "403.html", status=403)
    if request.user.role == "doctor" and appointment.doctor != request.user:
        return render(request, "403.html", status=403)

    return render(request, "appointments/detail.html", {"appointment": appointment})

@login_required
def create_appointment(request):
     #Allow patients to book an appointment"""
    if request.user.role != "patient":
        return redirect('appointments:list')

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('appointments:list')
    else:
        form = AppointmentForm()

    return render(request, "appointments/create.html", {"form": form})
