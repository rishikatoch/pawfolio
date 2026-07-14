# 🐾 Pawfolio

Pawfolio is a Flask-based Pet Management System that helps pet owners manage their pets, vaccination records, and health information in one place.

The application supports secure user authentication, multiple pets per user, vaccination tracking, photo uploads, and a modern responsive interface.

---

## ✨ Features

- 🔐 User Registration & Login
- 🐶 Add Multiple Pets
- 📸 Upload Pet Photos
- 📝 Edit & Delete Pets
- 💉 Add Vaccination Records
- ✏️ Edit Vaccination Records
- 🗑️ Delete Vaccination Records
- 👤 User-specific Dashboard (Each user can only access their own pets)
- 🎨 Modern Responsive UI
- 🐳 Docker Support
- 🗄️ Database Migrations using Flask-Migrate

---

## 🚀 Planned Features

- 📅 Vaccination Reminders
- 📧 Email Notifications
- 🐾 Pet Health Records
- 📈 Weight History Tracking
- ☁️ AWS Deployment using Terraform
- 🔔 Dashboard Analytics

---

## 🛠️ Technologies Used

- Python
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Migrate
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- Docker
- Git & GitHub

---

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

```
pawfolio/
│
├── app/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   └── __init__.py
│
├── migrations/
├── screenshots/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
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

Build and run the application

```bash
docker compose up --build
```

---

# 🔒 Security

- Password hashing using Werkzeug
- User authentication with Flask-Login
- User-specific access control
- Protected routes
- Secure file upload handling

---

# 👨‍💻 Author

**Rishi Katoch**

Mechanical Engineer transitioning into DevOps, Cloud and Python Development.

GitHub:
https://github.com/rishikatoch

LinkedIn:
https://www.linkedin.com/in/rishi-katoch-885732322/

---

# ⭐ Future Roadmap

- AWS Deployment
- Terraform Infrastructure
- PostgreSQL
- Email Reminder System
- Docker Production Setup
- CI/CD using GitHub Actions
- Kubernetes Deployment
- DevSecOps Integration (Trivy & Checkov)

---

If you found this project useful, consider giving it a ⭐ on GitHub.