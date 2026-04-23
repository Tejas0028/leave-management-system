# 🏢 Leave Management System (Django REST Framework + JWT)

A role-based Leave Management System built using **Django REST Framework (DRF)** with **JWT Authentication**, supporting Employee and Manager workflows.

---

## 🚀 Features

### 👨‍💼 Employee Module
- User registration and login (JWT authentication)
- Apply for leave (Casual / Sick)
- View own leave status
- Track approval status (Pending / Approved / Rejected)

### 🧑‍💼 Manager Module
- View all pending leave requests
- Approve or reject leave applications
- Add remarks for each decision
- Role-based access control

---

## 🔐 Authentication
- JWT-based authentication using SimpleJWT
- Access & Refresh token system
- Secure API endpoints with role-based permissions

---

## 🛠 Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SimpleJWT (Authentication)
- PostgreSQL (Recommended DB)
- Git & GitHub

---

## 📁 Project Structure

leave_management/
│
├── accounts/ # User & Authentication system
├── leaves/ # Leave management module
├── leave_management/# Project settings
├── manage.py



---

## ⚙️ Installation Setup

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/leave-management-system.git
cd leave-management-system

2. Create Virtual Environment
python -m venv venv

Activate:
Windows
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Environment Variables (.env)

Create .env file in root directory:

SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

5. Run Migrations
python manage.py makemigrations
python manage.py migrate

6. Create Superuser
python manage.py createsuperuser

7. Run Server
python manage.py runserver


🔑 API Endpoints
🔐 Authentication
Method	Endpoint	Description
POST	/api/accounts/register/	Register user
POST	/api/accounts/login/	Login & get JWT
POST	/api/token/refresh/	Refresh token

👨‍💼 Employee APIs
Method	Endpoint	Description
POST	/api/leaves/apply/	Apply leave
GET	/api/leaves/my/	View own leaves

🧑‍💼 Manager APIs
Method	Endpoint	Description
GET	/api/leaves/pending/	View pending leaves
POST	/api/leaves/action/<id>/	Approve/Reject leave

🔐 Sample Login Request
{
  "username": "test@gmail.com",
  "password": "123456"
}

📌 Sample Apply Leave Request
{
  "leave_type": 1,
  "start_date": "2026-04-25",
  "end_date": "2026-04-26",
  "reason": "Medical emergency"
}

⚡ Status Workflow
PENDING → APPROVED → REJECTED

