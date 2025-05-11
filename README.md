# Obsedo

Obsedo is a minimalist personal task manager built with Flask, Docker, and SQLite.

### ✨ Core Features

- Add, view, and delete tasks
- Mark tasks as complete
- Track priority, category, and optional due dates
- Clean interface with real-time updates

### 🛠️ Tech Stack

- **Backend:** Python + Flask + SQLAlchemy
- **Frontend:** HTML + Vanilla JS
- **Database:** SQLite (dev), with optional cloud upgrade planned
- **Infrastructure:** Docker + Docker Compose

---

## 🚀 Getting Started

### Requirements

- Python 3.11+
- Docker & Docker Compose

### Run in Docker

```bash
git clone https://github.com/jvlyndark/obsedo.git
cd obsedo
docker-compose up --build
```

Then visit http://localhost:5001 in your browser.

### 💻 Run Locally Without Docker (Optional)

Only do this if you want to run the code without containers:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

You'll need Python 3.11+ installed. This is mainly useful for debugging or development.

## 🧩 Roadmap

- [ ] Add OpenAI-powered task planning
- [x] Add GitHub Actions CI
- [ ] Add unit tests for Flask routes
- [ ] Deploy with Terraform + AWS

## 📄 License

This project is licensed under the MIT License.
See ./LICENSE for details.

---

## 🧪 Running Tests

To run tests locally:

```bash
pytest tests/
```

Make sure `pytest` is installed:

```bash
pip install pytest
```

---

## 🔁 GitHub Actions: Lint + Test

Tests and flake8 linting are automatically run on every push. CI is defined in `.github/workflows/ci.yml`.

---

## ☁️ Deploy to AWS with Terraform (Coming Soon)

We're setting up deployment infrastructure using:

- **Terraform** for infra-as-code
- **AWS ECS** for container hosting
- **S3** for static files (optional)
- **GitHub Actions** for CI/CD

Steps will be added as this infrastructure is developed.

## ✉️ Contact

#### Ursula J. d'Ark - ursulajdark at gmail dot com

#### Project Link: https://github.com/jvlyndark/obsedo
