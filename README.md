# 🐾 Pawfolio

Pawfolio is a production-ready pet management application built with **Flask** and deployed on **AWS** using modern DevOps practices.

The application enables pet owners to securely manage pets, vaccination records, and health information through a clean, responsive web interface.

Beyond application development, Pawfolio demonstrates cloud deployment using **AWS EC2**, **Terraform**, **Docker**, **Nginx**, **Gunicorn**, **PostgreSQL**, **Flask-Migrate**, and **AWS Systems Manager Parameter Store** for secure secret management.

---

## ✨ Features

### 🐾 Application Features

- 🔐 User Registration & Login
- 🐶 Add Multiple Pets
- 📸 Upload Pet Photos
- 📝 Edit & Delete Pets
- 💉 Add Vaccination Records
- ✏️ Edit Vaccination Records
- 🗑️ Delete Vaccination Records
- 👤 User-specific Dashboard
- 🎨 Modern Responsive UI

### ☁️ Production Features

- 🗄️ PostgreSQL Database
- 🔄 Database Migrations using Flask-Migrate (Alembic)
- 🐳 Docker & Docker Compose
- ⚡ Gunicorn Production Server
- 🌐 Nginx Reverse Proxy
- ☁️ AWS EC2 Deployment
- 🏗️ Infrastructure as Code using Terraform
- 🔐 AWS Systems Manager (SSM) Parameter Store
- 📂 Persistent PostgreSQL Storage
- 🖼️ Persistent Image Uploads
---

## 🚀 Planned Features

- 📅 Vaccination Reminder System
- 📧 Email Notifications
- 📈 Dashboard Analytics
- 📊 Weight History Tracking
- 📋 Pet Health Records
- 🔍 Search & Filtering
- 🔔 In-App Notifications
---

## 🛠️ Technologies Used

### Backend

- Python
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Migrate (Alembic)

### Frontend

- HTML5
- CSS3
- Bootstrap 5

### Database

- PostgreSQL

### DevOps & Cloud

- Docker
- Docker Compose
- Gunicorn
- Nginx
- Terraform
- AWS EC2
- AWS Systems Manager Parameter Store

### Version Control

- Git
- GitHub

---
## 🏗️ Architecture

```text
                 Internet
                     │
                     ▼
             AWS Security Group
                     │
                     ▼
              Nginx Reverse Proxy
                     │
                     ▼
          Gunicorn + Flask Application
                     │
                     ▼
             PostgreSQL Database
```

# 📸 Application Screenshots

## Login Page

![Login](screenshots/login.png)

Secure login page for existing users.

---

## Register Page

![Register](screenshots/register.png)

Create a new Pawfolio account.

---

## Home Page - Overview

![Home Overview](screenshots/Home%20Page%20-%20Overview.png)

Dashboard overview displaying user information and quick navigation.

---

## Home Page - Pet Cards

![Home Pet Cards](screenshots/Home%20Page%20-%20Pet%20Cards.png)

Displays all pets belonging to the logged-in user.

---

## Home Page - Additional Content

![Home Additional Content](screenshots/Home%20page%20-%20Additional%20Content.png)

Additional dashboard content and interface sections.

---

## Add Pet

![Add Pet](screenshots/add-pet.png)

Form to add a new pet with profile image and details.

---

## Pet Profile

![Pet Profile](screenshots/pet-profile.png)

Displays complete pet information including breed, age, weight, gender, vaccination status and profile photo.

---

## Vaccination Records

![Vaccination Records](screenshots/pet-profile(Vaccination%20Records).png)

Displays all vaccination records for the selected pet along with veterinarian details, due dates, and options to edit or delete records.

---

## Add Vaccination

![Vaccinations](screenshots/vaccinations.png)

Add vaccination details including vaccine name, vaccination date, next due date, veterinarian, and notes.

---

# 📂 Project Structure

```text
pawfolio/
│
├── app/
│   ├── static/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   └── __init__.py
│
├── migrations/
├── nginx/
├── scripts/
├── terraform/
├── screenshots/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── requirements.txt
├── run.py
├── .dockerignore
└── README.md
```
---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/rishikatoch/pawfolio.git
```

Move into the project

```bash
cd pawfolio
```

Create virtual environment

```bash
python3 -m venv .venv
```

Activate virtual environment

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run database migrations

```bash
flask db upgrade
```

Run the application

```bash
python run.py
```

Visit

```
http://127.0.0.1:5000
```

---

# 🐳 Docker

Run the application locally using Docker Compose:

```bash
docker compose up --build
```

For production deployments, use:

```bash
./scripts/deploy.sh
```

The deployment script automatically:

- Pulls the latest source code
- Retrieves secrets from AWS Systems Manager Parameter Store
- Starts Docker containers
- Runs Flask database migrations
- Starts the application behind Nginx
```bash
docker compose up --build
```

---

# 🔒 Security

- Password hashing using Werkzeug
- Flask-Login authentication
- User-specific authorization
- Protected routes
- Secure file upload handling
- Environment variables for configuration
- AWS Systems Manager Parameter Store for secret management
- PostgreSQL database
- Automatic database migrations using Alembic
- Nginx reverse proxy

---

# 📦 Releases

## Latest Release

**🐾 Pawfolio v1.2.0 – AWS Production Deployment**

### Highlights

- AWS EC2 Deployment
- Terraform Infrastructure
- Nginx Reverse Proxy
- Gunicorn Production Server
- PostgreSQL
- Docker Compose Production
- AWS Systems Manager Parameter Store
- Automatic Database Migrations

# 👨‍💻 Author

**Rishi Katoch**

Mechanical Engineer transitioning into DevOps, Cloud and Python Development.

GitHub:
https://github.com/rishikatoch

LinkedIn:
https://www.linkedin.com/in/rishi-katoch-885732322/

---

# ⭐ Future Roadmap

## Version 1.3.0

- GitHub Actions CI/CD
- Amazon ECR
- Automatic Deployment Pipeline

## Version 1.4.0

- HTTPS (SSL/TLS)
- CloudWatch Monitoring
- Custom Domain
- Security Headers

## Future Enhancements

- Email Reminder System
- Dashboard Analytics
- Weight Tracking
- Kubernetes Deployment
- DevSecOps Integration
  - Trivy
  - Checkov
---

If you found this project useful, consider giving it a ⭐ on GitHub.
