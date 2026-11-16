# ☁️ Cloud File Manager

A Django-based Cloud File Management System that allows users
to securely upload, manage, download, and delete their files
through a user-friendly web application.

## 🚀 Features

- User Registration and Login
- Secure User Authentication
- User Dashboard
- File Upload
- File Download
- File Deletion
- File Management
- User Profile Management
- Profile Picture Upload
- Change Password
- Forgot Password with Email Reset Link

## 🛠️ Technologies Used

**Backend:** Python, Django

**Frontend:** HTML, CSS, JavaScript

**Database:** SQLite

**Version Control:** Git and GitHub

## 📂 Project Structure

CloudFileManager/
├── accounts/
├── cloudmanager/
├── filemanager/
├── templates/
├── manage.py
├── requirements.txt
└── README.md

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/adhitya7-crypto/CloudFileManager.git
```

### 2. Navigate to the Project

```bash
cd CloudFileManager
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

Never commit the `.env` file to GitHub.

### 7. Apply Database Migrations

```bash
python manage.py migrate
```

### 8. Run the Application

```bash
python manage.py runserver
```

Open the local development server in your browser.

## 🔐 Security

- Django Authentication
- Password Hashing
- CSRF Protection
- Environment Variables for Credentials
- User Authentication for Protected Pages

## 👨‍💻 Developer

**Aadhitya**

Python Developer | Django | Cloud & DevOps Enthusiast

## 📌 Project Status

Development and deployment preparation in progress.