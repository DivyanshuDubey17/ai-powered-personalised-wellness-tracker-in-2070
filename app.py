"""
app.py  –  Neural-Wellness 2070
────────────────────────────────────────────────────────────────────
• Flask + SQLAlchemy + Flask-Login + Bcrypt
• Duplicate-safe registration
• AI plan / feeling / mood APIs unchanged
"""

from flask import (
    Flask, render_template, url_for, flash,
    redirect, request, jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, logout_user,
    current_user, login_required
)
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json, os

# ── local modules ────────────────────────────────────────────────
from config         import Config
from models         import db, User, WellnessPlan, MoodLog, VRContent, FeelingsLog
from ai_wellness    import GeminiWellnessAI

# ── Flask & extensions ───────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)

login_manager            = LoginManager(app)
login_manager.login_view = "login"

# AI helper
ai_wellness = GeminiWellnessAI()

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# Jinja filter to safely load JSON
@app.template_filter("from_json")
def from_json_filter(value):
    try:
        return json.loads(value) if value else []
    except (ValueError, TypeError):
        return []

# ── Pages ────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("home.html")

# 1️⃣  REGISTER  – duplicate-safe
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"].strip()
        email    = request.form["email"].strip().lower()
        raw_pw   = request.form["password"]

        # stop early if user exists
        if User.query.filter(
            (User.email==email) | (User.username==username)
        ).first():
            flash("Username or e-mail already registered.", "danger")
            return redirect(url_for("register"))

        pw_hash = bcrypt.generate_password_hash(raw_pw).decode("utf-8")
        user    = User(
            username      = username,
            email         = email,
            password      = pw_hash,
            age           = int(request.form.get("age", 25)),
            fitness_level = request.form.get("fitness_level", "beginner"),
            health_goals  = request.form.get("health_goals", "")
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:                # last-chance defence
            db.session.rollback()
            flash("Username or e-mail already registered.", "danger")
            return redirect(url_for("register"))

        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# 2️⃣  LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form["email"].strip().lower()
        ).first()

        if user and bcrypt.check_password_hash(
            user.password, request.form["password"]
        ):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid e-mail or password.", "danger")

    return render_template("login.html")

# 3️⃣  DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    plan_row = WellnessPlan.query.filter_by(
        user_id=current_user.id, is_active=True
    ).first()

    plan = None
    if plan_row:
        try:
            plan = {
                "mental_health_plan" : json.loads(plan_row.mental_health_plan) or [],
                "fitness_plan"       : json.loads(plan_row.fitness_plan)       or [],
                "nutrition_plan"     : json.loads(plan_row.nutrition_plan)     or [],
                "personalized_insights" : plan_row.personalized_insights or "",
                "motivation_message"    : plan_row.motivation_message    or ""
            }
        except (ValueError, TypeError):
            plan = None

    moods     = MoodLog.query.filter_by(user_id=current_user.id)\
                  .order_by(MoodLog.log_date.desc()).limit(7).all()
    feelings  = FeelingsLog.query.filter_by(user_id=current_user.id)\
                  .order_by(FeelingsLog.created_date.desc()).limit(3).all()
    vr_items  = VRContent.query.limit(3).all()

    return render_template(
        "dashboard.html",
        plan=plan, moods=moods,
        feelings=feelings, vr_content=vr_items
    )

# 4️⃣  AI PLAN GENERATION  (unchanged)
@app.route("/api/generate-ai-wellness-plan", methods=["POST"])
@login_required
def generate_plan():
    try:
        data = request.get_json()

        user_data = {
            "age"          : current_user.age,
            "fitness_level": current_user.fitness_level,
            "health_goals" : current_user.health_goals,
            "mood_score"   : data.get("mood_score", 5),
            "stress_level" : data.get("stress_level", 5),
            "energy_level" : data.get("energy_level", 5)
        }

        desc   = data.get("feelings_description", "")
        ai_out = ai_wellness.generate_wellness_plan(user_data, desc)

        # optional feelings log
        if desc:
            feelings = ai_wellness.analyze_feelings(desc)
            db.session.add(
                FeelingsLog(
                    user_id=current_user.id,
                    feelings_text=desc,
                    ai_analysis=json.dumps(feelings)
                )
            )

        # deactivate old plans
        WellnessPlan.query.filter_by(
            user_id=current_user.id, is_active=True
        ).update({"is_active": False})

        # save new plan
        db.session.add(
            WellnessPlan(
                user_id=current_user.id,
                mental_health_plan = json.dumps(ai_out["mental_health"]),
                fitness_plan       = json.dumps(ai_out["fitness"]),
                nutrition_plan     = json.dumps(ai_out["nutrition"]),
                personalized_insights = ai_out["personalized_insights"],
                motivation_message    = ai_out["motivation_message"]
            )
        )
        db.session.commit()

        return jsonify({"success": True, "plan": ai_out})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# feelings-analysis and mood-log endpoints unchanged …
# voice-command endpoint unchanged …

# 5️⃣  LOGOUT
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

# ── create tables & sample VR on first run ───────────────────────
with app.app_context():
    db.create_all()

    if not VRContent.query.first():
        db.session.add_all([
            VRContent(title="Neural Calm Forest", content_type="meditation",
                      description="Forest meditation with biometric feedback",
                      duration=15, difficulty_level="beginner"),
            VRContent(title="Quantum Mindfulness Space", content_type="therapy",
                      description="Quantum-rendered therapy environment",
                      duration=30, difficulty_level="advanced"),
            VRContent(title="Holographic Yoga Studio", content_type="exercise",
                      description="AI-guided yoga with neural form correction",
                      duration=45, difficulty_level="intermediate")
        ])
        db.session.commit()

# ── run ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
