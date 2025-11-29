# Medilink – Hospital Management System (Django + PostgreSQL)

**Medilink** is a modern **Hospital Management System** built using **Django**, providing **role-based dashboards** for **Patients** and **Doctors**, appointment management, secure authentication, and profile management.

---

##  Features

###  User Authentication
- User registration & login  
- Role-based access: **Patient** or **Doctor**  
- Secure password hashing  
- Password update from profile  

---

###  Patient Features
- **Dashboard** with: 
- Book appointments with doctors  
- View appointment list & details  
- Update profile (name, phone, address, DOB, gender, etc.)
- Change password

---

###  Doctor Features
- **Dashboard** with:
- View appointments with patients  
- Update  profile fields (name, specialization, hospital contact)
- Change password


---

###  Appointments
- Patients can book appointments  
- Doctors can view appointments (cannot book)  
- Appointment detail page  
- Role-based appointment list  
- Backend: PostgreSQL  

---

###  UI / Templates
- Responsive and professional design using **Bootstrap**  
- Dashboard cards for key stats  
- Modal password change form  
- Clean & intuitive layout  

---

##  Tech Stack
- **Backend:** Django (Python) 
- **Database:** PostgreSQL  
- **Frontend:** HTML, CSS, Bootstrap  
- **Deployment:** Render (Web Service + PostgreSQL Database)  

---

##  Project Structure

medilink/
│── appointments/
│── doctors/
│── patients/
│── users/
│── templates/
│── static/
│── medilink/ # settings, urls
│── manage.py


---

##  Installation (Local Setup)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/JESMARIYA-ARUN/Medilink-Hospital-Management-System
   cd Medilink-Hospital-Management-System
2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate     # Mac/Linux
   venv\Scripts\activate        # Windows
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
4. **Configure Database**
   ```bash
   CREATE DATABASE medilink_db;
Update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'medilink_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
5. **Run migrations**
   ```bash
   python manage.py makemigrations

6.  **Create superuser**
   ```bash
  python manage.py createsuperuser
7.  **Start development server**
   ```bash
  python manage.py runserver
   App will be live at: http://127.0.0.1:8000/
