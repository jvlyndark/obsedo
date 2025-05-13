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

- [x] Add OpenAI-powered task planning
- [x] Add GitHub Actions CI
- [x] Add unit tests for Flask routes
- [x] Deploy with Terraform + AWS
- [ ] Allow users to provide their own OpenAI key client-side
- [ ] Add filtering + sorting (priority, category, completion)
- [ ] Responsive UI redesign (mobile & dark mode)
- [ ] Add task editing

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

### 🤖 AI-Powered Task Planning (Optional)

Obsedo supports OpenAI integration for automatic task breakdown.

Just enter a goal like:

> "Plan a trip to Berlin"

Obsedo will generate actionable tasks using GPT-3.5.

To enable:

1. Get an [OpenAI API key](https://platform.openai.com/account/api-keys)
2. Set it in your `.env` file:
   OPENAI_API_KEY=your-key-here

If no key is set, the feature is disabled gracefully.

---

## ☁️ Deploy to AWS with Terraform

Obsedo is fully deployable to the cloud using:

- **Terraform** for infra-as-code
- **AWS EC2** for hosting
- **Docker Compose** for service management
- **GitHub Actions** for CI/CD (Terraform apply coming soon)

You can find Terraform config under `/infra`.

Deployment spins up an EC2 instance, installs Docker, and launches the app via `docker-compose`.

Steps will be added as this infrastructure is developed.

## ✉️ Contact

#### Ursula J. d'Ark - ursulajdark at gmail dot com

#### Project Link: https://github.com/jvlyndark/obsedo
