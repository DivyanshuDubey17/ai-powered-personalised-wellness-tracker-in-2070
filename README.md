# 2070 Neural Wellness Planner 🧠✨

AI-powered wellness dashboard built with Flask + Google Gemini, offering
personalised mental-health, fitness, and nutrition plans—plus VR sessions,
mood tracking, and voice-driven journaling.

---

## Table of Contents
1. Features
2. Tech Stack
3. Project Structure
4. Quick Start (Dev)
5. Environment Variables
6. Useful Commands
7. API Reference
8. Database Schema
9. Roadmap / Ideas
10. Contributing
11. License

---

## 1️⃣ Features
* ✨ AI wellness plan generator (Gemini 1.5 Flash)
* 🎙️ Speech-to-text feelings journaling
* 🎤 Voice command shortcuts (Web Speech API)
* 🥽 VR content carousel (therapy / meditation / exercise)
* 📊 Mood & stress sliders with historical spark-line
* 🏆 Gamification: streaks, XP, badges *(planned)*
* 🌗 Light / dark theme toggle *(planned)*
* 🔒 JWT-secure APIs + Flask-Login sessions

---

## 2️⃣ Tech Stack
* **Backend:** Flask 2.x, SQLAlchemy, Flask-Login, Flask-Migrate
* **AI:** Google Gemini API
* **DB:** SQLite (dev) – easy swap to Postgres/MySQL
* **Frontend:** Bootstrap 5, Chart.js 4, vanilla JS
* **Auth:** bcrypt password hashing
* **Deployment:** Gunicorn + Nginx *(prod suggestion)*

---

## 3️⃣ Project Structure
personalized_wellness/
├── app.py # Flask entry-point
├── ai_wellness.py # Gemini wrapper class
├── models.py # SQLAlchemy models
├── config.py # Config object
├── requirements.txt
├── templates/
│ ├── base.html
│ ├── dashboard.html
│ └── ...
├── static/
│ ├── css/style.css
│ └── js/wellness.js
└── .env.example # sample env file


---

## 4️⃣ Quick Start (Dev)

1. Clone & enter project
git clone <repo_url>
cd personalized_wellness

2. Python env
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

3. Install deps
pip install -r requirements.txt

4. Configure environment
cp .env.example .env

→ fill GEMINI_API_KEY & SECRET_KEY
5. Run dev server
python app.py
Open `http://127.0.0.1:5000/`.

---

## 5️⃣ Environment Variables (`.env`)
GEMINI_API_KEY=your_google_gemini_key
SECRET_KEY=flask_session_secret
SQLALCHEMY_DATABASE_URI=sqlite:///wellness_2070.db # optional override


---

## 6️⃣ Useful Commands
| Task | Command |
|------|---------|
| Initialise DB (first run) | `python app.py` (auto-creates tables) |
| Generate migration | `flask db migrate -m "message"` |
| Apply migration | `flask db upgrade` |
| Create admin user (Python shell) | `from app import db,User; User(...); db.session.commit()` |
| Freeze deps | `pip freeze > requirements.txt` |

---

## 7️⃣ API Reference (JSON ⇄ AJAX)
| Method | Endpoint | Body / Params | Purpose |
|--------|----------|--------------|---------|
| POST | `/api/generate-ai-wellness-plan` | mood_score, stress_level, energy_level, feelings_description | Returns personalised plan |
| POST | `/api/analyze-feelings` | feelings_text | Returns emotion analysis |
| POST | `/api/log-mood` | mood_score, stress_level, energy_level | Saves daily mood |
| GET  | `/api/mood-series` *(planned)* | — | Last 7 mood scores for spark-line |

---

## 8️⃣ Database Schema (snapshot)

User
├─ id (PK)
├─ username, email, password
├─ age, fitness_level, health_goals
└─ created_date

WellnessPlan
├─ id (PK), user_id (FK)
├─ mental_health_plan, fitness_plan, nutrition_plan
├─ personalized_insights, motivation_message
├─ is_active, created_date

MoodLog
├─ id (PK), user_id (FK)
├─ mood_score, stress_level, energy_level, notes
└─ log_date

FeelingsLog
├─ id (PK), user_id (FK)
├─ feelings_text, ai_analysis
└─ created_date

VRContent(Wanted to implement further)
├─ id (PK), title, content_type
├─ description, duration, difficulty_level, file_path  


---

## 9️⃣ Roadmap / Ideas
- [ ] Dark-mode + neon accent theme  
- [ ] Animated mic waveform during speech-to-text  
- [ ] Streak & XP gamification overlay  
- [ ] OAuth sign-in (Google / GitHub)  
- [ ] Push notifications for plan reminders  
- [ ] Dockerfile & CI workflow  

---

## 🔟 Contributing
Pull requests are welcome! Please:
1. Fork → branch → PR.
2. Follow PEP-8 and run `black .`.
3. Describe the change clearly.

For major changes open an issue first to discuss.

---

## 11 License
MIT – see `LICENSE` for full text.
