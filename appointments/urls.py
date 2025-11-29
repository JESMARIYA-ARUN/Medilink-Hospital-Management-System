from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointments_list, name='list'),
    path('create/', views.create_appointment, name='create'),
    path('<int:id>/', views.appointment_detail, name='detail'),
]
