# Complaint Management System (CMS)

A web-based Complaint Management System built using Django that helps users register complaints, track complaint progress, send SOS alerts, and manage complaint workflows efficiently.

---

# Modules

## User
- [x] register
- [x] login
- [x] complaint_submission
- [x] sos (location)
- [x] feedback
- [x] notification

## SHO
- [x] receive_complaint
- [x] document_complaint
- [x] sos_alert
- [x] forward_to_complaint_manager
- [x] user_support

## Complaint Manager
- [x] case_assignment
- [x] report_generation
- [x] status_update_to_user

## System Manager
- [x] user_role_management
- [x] system_configuration
- [x] backup
- [x] dashboard

---

# Additional Features

- [x] sho, cm and sm does not need to sign up
- [x] cm and sho has different manage_complaint
- [x] user tracking graph
- [x] expandable architecture
- [x] sos alerts map
- [x] complaint district
- [x] user district
- [x] sos district detection
- [x] download complaint in pdf format
- [x] remove the about from index
- [x] remove others from index
- [x] forward complaint from sho to cm
- [x] password confirmation checking
- [x] cm complaint documenting
- [x] complaint manager can update complaint status of users
- [x] user tracking graph working state

---

# Technologies Used

- Django
- HTML
- CSS
- JavaScript
- SCSS
- MariaDB

---

# Project Structure

```text
shuhaibnc-complaint-management-system/
│
├── complaint_management_system/
├── complaint_manager/
├── home/
├── sho/
├── system_manager/
├── user/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/shuhaibnc/shuhaibnc-complaint-management-system.git
cd shuhaibnc-complaint-management-system
```

---

## Create Virtual Environment

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Database

Change database configuration in:

```text
complaint_management_system/settings.py
```

Replace the default database configuration with:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '', # Enter Database name here
        'USER': '', # Enter Database username here
        'PASSWORD': '', # Enter DB Password here
        'HOST': 'localhost', # Enter Host here
        'PORT': '3306', # Enter Port here
    }
}
```

Make sure MariaDB server is installed and running before applying migrations.

---

## Apply Migrations

```bash
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Run Server

```bash
python manage.py runserver
```

Open browser:

```text
http://127.0.0.1:8000/
```

---

# Homepage

The homepage provides:

- Complaint registration
- Complaint tracking
- Transparent complaint workflow
- Kerala Police themed interface
- SOS alert access

---

# Security Notes

- Use HTTPS in production
- Store secrets using environment variables
- Restrict admin access
- Configure proper authentication
- Secure database configuration

---

# Future Improvements

- Real-time notifications
- AI-based complaint categorization
- Mobile application
- SMS and Email integration
- Advanced analytics dashboard
- Multi-language support

---

# Authors

Developed by:

- Shuhaib N C
- Adnan

---

# License

This project is developed for academic and educational purposes.