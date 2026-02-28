# main.py - FitPlan AI - Flask Application with all features

import os, json, hashlib
from datetime import datetime, date, timedelta
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, send_file)
from database import get_db, create_tables
from utils import hash_password, verify_password, validate_profile
from services.workout_service import (
    calculate_bmi, categorize_bmi, calculate_bmr,
    calculate_daily_calories, generate_workout_plan
)
from services.diet_service import generate_diet_plan

# ── APP SETUP ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fitplan-ai-secret-2024")

# ── SECURITY: Secret Admin URL ─────────────────────────────────────────────
# Change ADMIN_SECRET in .env file to your own secret path
ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "jay-admin-9321")

# ── SECURITY: Login Rate Limiting ──────────────────────────────────────────
# Stores failed attempts: { ip_address: {"count": 0, "locked_until": datetime} }
login_attempts = {}
MAX_ATTEMPTS = 5          # Max wrong attempts allowed
LOCKOUT_MINUTES = 15      # Minutes to lock after too many attempts
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ── AUTH HELPERS ──────────────────────────────────────────────────────────────
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        db = get_db()
        user = db.execute("SELECT is_admin FROM users WHERE id=?", (session["user_id"],)).fetchone()
        db.close()
        if not user or not user["is_admin"]:
            return render_template("403.html"), 403
        return f(*args, **kwargs)
    return decorated

# ── HOME ──────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ── AUTH ──────────────────────────────────────────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if len(username) < 3:
            return render_template("register.html", error="Username must be at least 3 characters.")
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters.")
        if "@" not in email:
            return render_template("register.html", error="Please enter a valid email.")
        db = get_db()
        existing = db.execute("SELECT id FROM users WHERE username=? OR email=?", (username, email)).fetchone()
        if existing:
            db.close()
            return render_template("register.html", error="Username or email already registered.")
        db.execute("INSERT INTO users (username, email, hashed_password) VALUES (?,?,?)",
                   (username, email, hash_password(password)))
        db.commit()
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        db.close()
        return redirect(url_for("profile_page"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        ip = request.remote_addr or "unknown"
        now = datetime.now()

        # ── Check if IP is locked out ──────────────────────────────────────
        if ip in login_attempts:
            attempt_data = login_attempts[ip]
            if attempt_data.get("locked_until") and now < attempt_data["locked_until"]:
                mins_left = int((attempt_data["locked_until"] - now).seconds / 60) + 1
                return render_template("login.html",
                    error=f"Too many failed attempts. Try again in {mins_left} minute(s).",
                    locked=True)

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        db.close()

        if not user or not verify_password(password, user["hashed_password"]):
            # ── Record failed attempt ──────────────────────────────────────
            if ip not in login_attempts:
                login_attempts[ip] = {"count": 0, "locked_until": None}
            login_attempts[ip]["count"] += 1
            attempts_left = MAX_ATTEMPTS - login_attempts[ip]["count"]

            if login_attempts[ip]["count"] >= MAX_ATTEMPTS:
                login_attempts[ip]["locked_until"] = now + timedelta(minutes=LOCKOUT_MINUTES)
                return render_template("login.html",
                    error=f"Account locked for {LOCKOUT_MINUTES} minutes due to too many failed attempts.",
                    locked=True)

            return render_template("login.html",
                error=f"Invalid username or password. {attempts_left} attempt(s) remaining.")

        if not user["is_active"]:
            return render_template("login.html",
                error="Your account has been deactivated. Contact admin.")

        # ── Successful login — reset attempts ──────────────────────────────
        if ip in login_attempts:
            del login_attempts[ip]

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["is_admin"] = bool(user["is_admin"])
        # Store secret in session so navbar link works (never shown in HTML source)
        if user["is_admin"]:
            session["admin_secret"] = ADMIN_SECRET
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ── PROFILE ───────────────────────────────────────────────────────────────────
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():
    db = get_db()
    user_id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    profile = db.execute("SELECT * FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()

    if request.method == "POST":
        # Handle profile photo upload
        photo_filename = user["profile_photo"]
        if "photo" in request.files:
            photo = request.files["photo"]
            if photo and photo.filename and allowed_file(photo.filename):
                ext = photo.filename.rsplit(".", 1)[1].lower()
                photo_filename = f"user_{user_id}.{ext}"
                photo.save(os.path.join(UPLOAD_FOLDER, photo_filename))
                db.execute("UPDATE users SET profile_photo=? WHERE id=?", (photo_filename, user_id))

        data = request.form.to_dict()
        errors = validate_profile(data)
        if errors:
            db.close()
            return render_template("profile.html", profile=dict(profile) if profile else None,
                                   user=dict(user), errors=errors)

        age = int(data["age"])
        gender = data["gender"]
        height_cm = float(data["height_cm"])
        weight_kg = float(data["weight_kg"])
        bmi = calculate_bmi(weight_kg, height_cm)
        bmi_category = categorize_bmi(bmi)
        bmr = calculate_bmr(age, gender, weight_kg, height_cm)
        daily_calories = calculate_daily_calories(bmr, data["fitness_goal"], bmi_category)

        if profile:
            db.execute("""UPDATE user_profiles SET age=?,gender=?,height_cm=?,weight_kg=?,bmi=?,
                bmi_category=?,fitness_goal=?,dietary_preference=?,cultural_preference=?,
                budget_level=?,equipment=?,bmr=?,daily_calories=?,updated_at=CURRENT_TIMESTAMP
                WHERE user_id=?""",
                (age,gender,height_cm,weight_kg,bmi,bmi_category,data["fitness_goal"],
                 data["dietary_preference"],data["cultural_preference"],data["budget_level"],
                 data["equipment"],bmr,daily_calories,user_id))
        else:
            db.execute("""INSERT INTO user_profiles
                (user_id,age,gender,height_cm,weight_kg,bmi,bmi_category,fitness_goal,
                 dietary_preference,cultural_preference,budget_level,equipment,bmr,daily_calories)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (user_id,age,gender,height_cm,weight_kg,bmi,bmi_category,data["fitness_goal"],
                 data["dietary_preference"],data["cultural_preference"],data["budget_level"],
                 data["equipment"],bmr,daily_calories))
        db.commit()
        db.close()
        return redirect(url_for("dashboard"))

    db.close()
    return render_template("profile.html", profile=dict(profile) if profile else None, user=dict(user))

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    user_id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    profile = db.execute("SELECT * FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()
    workout_plan = diet_plan = None
    progress_logs = []
    if profile:
        lw = db.execute("SELECT plan_data FROM workout_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,)).fetchone()
        ld = db.execute("SELECT plan_data FROM diet_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,)).fetchone()
        workout_plan = json.loads(lw["plan_data"]) if lw else None
        diet_plan = json.loads(ld["plan_data"]) if ld else None
        # Last 7 days progress
        progress_logs = db.execute(
            "SELECT * FROM progress_logs WHERE user_id=? ORDER BY log_date DESC LIMIT 7", (user_id,)
        ).fetchall()
    db.close()
    return render_template("dashboard.html", user=dict(user),
                           profile=dict(profile) if profile else None,
                           workout_plan=workout_plan, diet_plan=diet_plan,
                           progress_logs=[dict(p) for p in progress_logs])

# ── GENERATE PLANS ────────────────────────────────────────────────────────────
@app.route("/generate-workout", methods=["POST"])
@login_required
def generate_workout():
    db = get_db()
    user_id = session["user_id"]
    profile = db.execute("SELECT * FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()
    if not profile:
        db.close()
        return redirect(url_for("profile_page"))
    plan_data = generate_workout_plan(dict(profile))
    db.execute("INSERT INTO workout_plans (user_id, plan_data) VALUES (?,?)",
               (user_id, json.dumps(plan_data)))
    db.commit()
    db.close()
    return redirect(url_for("dashboard") + "#workout")

@app.route("/generate-diet", methods=["POST"])
@login_required
def generate_diet():
    db = get_db()
    user_id = session["user_id"]
    profile = db.execute("SELECT * FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()
    if not profile:
        db.close()
        return redirect(url_for("profile_page"))
    plan_data = generate_diet_plan(dict(profile))
    db.execute("INSERT INTO diet_plans (user_id, plan_data) VALUES (?,?)",
               (user_id, json.dumps(plan_data)))
    db.commit()
    db.close()
    return redirect(url_for("dashboard") + "#diet")

# ── WORKOUT PLAN PAGE ─────────────────────────────────────────────────────────
@app.route("/workout-plan")
@login_required
def workout_plan_page():
    db = get_db()
    user_id = session["user_id"]
    latest = db.execute("SELECT plan_data, created_at FROM workout_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,)).fetchone()
    db.close()
    plan = json.loads(latest["plan_data"]) if latest else None
    created_at = latest["created_at"] if latest else None
    return render_template("workout_plan.html", plan=plan, created_at=created_at)

# ── DIET PLAN PAGE ────────────────────────────────────────────────────────────
@app.route("/diet-plan")
@login_required
def diet_plan_page():
    db = get_db()
    user_id = session["user_id"]
    latest = db.execute("SELECT plan_data, created_at FROM diet_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,)).fetchone()
    db.close()
    plan = json.loads(latest["plan_data"]) if latest else None
    created_at = latest["created_at"] if latest else None
    return render_template("diet_plan.html", plan=plan, created_at=created_at)

# ── PROGRESS TRACKER ──────────────────────────────────────────────────────────
@app.route("/progress", methods=["GET", "POST"])
@login_required
def progress():
    db = get_db()
    user_id = session["user_id"]
    profile = db.execute("SELECT * FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()

    if request.method == "POST":
        log_date = request.form.get("log_date", str(date.today()))
        weight_kg = request.form.get("weight_kg", "")
        water_ml = request.form.get("water_ml", 0)
        notes = request.form.get("notes", "")
        try:
            weight_kg = float(weight_kg) if weight_kg else None
            water_ml = int(water_ml) if water_ml else 0
            db.execute("""INSERT INTO progress_logs (user_id, log_date, weight_kg, water_ml, notes)
                VALUES (?,?,?,?,?) ON CONFLICT(user_id, log_date)
                DO UPDATE SET weight_kg=excluded.weight_kg,
                water_ml=excluded.water_ml, notes=excluded.notes""",
                (user_id, log_date, weight_kg, water_ml, notes))
            db.commit()
        except Exception as e:
            print("Progress log error:", e)

    logs = db.execute(
        "SELECT * FROM progress_logs WHERE user_id=? ORDER BY log_date DESC LIMIT 30", (user_id,)
    ).fetchall()

    # Build chart data (last 14 days)
    chart_labels = []
    chart_weights = []
    chart_water = []
    for log in reversed(logs[:14]):
        chart_labels.append(log["log_date"])
        chart_weights.append(log["weight_kg"] if log["weight_kg"] else None)
        chart_water.append(log["water_ml"] or 0)

    db.close()
    today = str(date.today())
    return render_template("progress.html",
                           logs=[dict(l) for l in logs],
                           profile=dict(profile) if profile else None,
                           chart_labels=json.dumps(chart_labels),
                           chart_weights=json.dumps(chart_weights),
                           chart_water=json.dumps(chart_water),
                           today=today)

# ── DOWNLOAD PDF (text-based plan) ───────────────────────────────────────────
@app.route("/download-plan")
@login_required
def download_plan():
    db = get_db()
    user_id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    profile = db.execute("SELECT * FROM user_profiles WHERE user_id=?", (user_id,)).fetchone()
    lw = db.execute("SELECT plan_data FROM workout_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,)).fetchone()
    ld = db.execute("SELECT plan_data FROM diet_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,)).fetchone()
    db.close()

    workout_plan = json.loads(lw["plan_data"]) if lw else None
    diet_plan = json.loads(ld["plan_data"]) if ld else None

    # Generate a nicely formatted text plan
    lines = []
    lines.append("=" * 60)
    lines.append("       FITPLAN AI - PERSONALIZED FITNESS PLAN")
    lines.append("=" * 60)
    lines.append(f"  Name    : {user['username'].upper()}")
    if profile:
        lines.append(f"  BMI     : {profile['bmi']} ({profile['bmi_category']})")
        lines.append(f"  Goal    : {profile['fitness_goal'].replace('_',' ').title()}")
        lines.append(f"  Calories: {int(profile['daily_calories'])} kcal/day")
    lines.append(f"  Date    : {datetime.now().strftime('%B %d, %Y')}")
    lines.append("=" * 60)

    if workout_plan:
        lines.append("")
        lines.append("  7-DAY WORKOUT PLAN")
        lines.append("-" * 60)
        lines.append(f"  Intensity: {workout_plan['intensity']}")
        lines.append("")
        for day in workout_plan["weekly_plan"]:
            lines.append(f"  {day['day'].upper()} — {day['focus']} ({day['total_duration_minutes']} min)")
            for ex in day["exercises"]:
                lines.append(f"    • {ex['name']:<30} {ex['sets']} sets x {ex['reps']}")
            lines.append("")
        if workout_plan.get("notes"):
            lines.append(f"  AI Tip: {workout_plan['notes']}")

    if diet_plan:
        lines.append("")
        lines.append("  DAILY DIET PLAN")
        lines.append("-" * 60)
        lines.append(f"  Target Calories : {diet_plan['target_calories']} kcal")
        lines.append(f"  Total Calories  : {diet_plan['total_calories']} kcal")
        lines.append(f"  Protein         : {diet_plan['total_protein_g']}g")
        lines.append(f"  Carbs           : {diet_plan['total_carbs_g']}g")
        lines.append(f"  Fat             : {diet_plan['total_fat_g']}g")
        lines.append("")
        for meal_name, items in [("BREAKFAST", diet_plan["breakfast"]),
                                  ("LUNCH", diet_plan["lunch"]),
                                  ("DINNER", diet_plan["dinner"]),
                                  ("SNACKS", diet_plan["snacks"])]:
            if items:
                lines.append(f"  {meal_name}:")
                for item in items:
                    lines.append(f"    • {item['name']:<35} {item['qty']} — {item['cal']} kcal")
                lines.append("")
        if diet_plan.get("notes"):
            lines.append(f"  Nutrition Tip: {diet_plan['notes']}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  Generated by FitPlan AI")
    lines.append("=" * 60)

    content = "\n".join(lines)

    # Save as text file and send
    import tempfile
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
    tmp.write(content)
    tmp.close()

    filename = f"FitPlan_{user['username']}_{datetime.now().strftime('%Y%m%d')}.txt"
    return send_file(tmp.name, as_attachment=True, download_name=filename, mimetype="text/plain")

# ── ADMIN DASHBOARD ───────────────────────────────────────────────────────────
@app.route("/<admin_secret>/dashboard")
@admin_required
def admin_dashboard(admin_secret=None):
    if admin_secret != ADMIN_SECRET:
        return render_template("404.html"), 404
    db = get_db()
    users = db.execute("""
        SELECT u.id, u.username, u.email, u.is_active, u.is_admin, u.created_at,
               p.bmi, p.bmi_category, p.fitness_goal, p.weight_kg,
               (SELECT COUNT(*) FROM workout_plans wp WHERE wp.user_id = u.id) as workout_count,
               (SELECT COUNT(*) FROM diet_plans dp WHERE dp.user_id = u.id) as diet_count
        FROM users u
        LEFT JOIN user_profiles p ON p.user_id = u.id
        ORDER BY u.created_at DESC
    """).fetchall()

    stats = {
        "total_users": db.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "active_users": db.execute("SELECT COUNT(*) FROM users WHERE is_active=1").fetchone()[0],
        "total_workouts": db.execute("SELECT COUNT(*) FROM workout_plans").fetchone()[0],
        "total_diets": db.execute("SELECT COUNT(*) FROM diet_plans").fetchone()[0],
        "total_logs": db.execute("SELECT COUNT(*) FROM progress_logs").fetchone()[0],
    }
    db.close()
    return render_template("admin.html", users=[dict(u) for u in users],
                           stats=stats, admin_secret=ADMIN_SECRET)

@app.route("/<admin_secret>/toggle-user/<int:user_id>", methods=["POST"])
@admin_required
def admin_toggle_user(user_id, admin_secret=None):
    if admin_secret != ADMIN_SECRET:
        return render_template("404.html"), 404
    db = get_db()
    user = db.execute("SELECT is_active, is_admin FROM users WHERE id=?", (user_id,)).fetchone()
    if user and not user["is_admin"]:
        new_status = 0 if user["is_active"] else 1
        db.execute("UPDATE users SET is_active=? WHERE id=?", (new_status, user_id))
        db.commit()
    db.close()
    return redirect(f"/{ADMIN_SECRET}/dashboard")

@app.route("/<admin_secret>/delete-user/<int:user_id>", methods=["POST"])
@admin_required
def admin_delete_user(user_id, admin_secret=None):
    if admin_secret != ADMIN_SECRET:
        return render_template("404.html"), 404
    db = get_db()
    user = db.execute("SELECT is_admin FROM users WHERE id=?", (user_id,)).fetchone()
    if user and not user["is_admin"]:
        db.execute("DELETE FROM progress_logs WHERE user_id=?", (user_id,))
        db.execute("DELETE FROM workout_plans WHERE user_id=?", (user_id,))
        db.execute("DELETE FROM diet_plans WHERE user_id=?", (user_id,))
        db.execute("DELETE FROM user_profiles WHERE user_id=?", (user_id,))
        db.execute("DELETE FROM users WHERE id=?", (user_id,))
        db.commit()
    db.close()
    return redirect(f"/{ADMIN_SECRET}/dashboard")

@app.route("/<admin_secret>/make-admin/<int:user_id>", methods=["POST"])
@admin_required
def admin_make_admin(user_id, admin_secret=None):
    if admin_secret != ADMIN_SECRET:
        return render_template("404.html"), 404
    db = get_db()
    db.execute("UPDATE users SET is_admin=1 WHERE id=?", (user_id,))
    db.commit()
    db.close()
    return redirect(f"/{ADMIN_SECRET}/dashboard")

# ── ERROR PAGES ───────────────────────────────────────────────────────────────
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

# ── RUN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    create_tables()
    # Create default admin user
    db = get_db()
    admin = db.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if not admin:
        from utils import hash_password as hp
        db.execute("INSERT INTO users (username, email, hashed_password, is_admin) VALUES (?,?,?,1)",
                   ("admin", "admin@fitplan.com", hp("admin123")))
        db.commit()
        print("✅ Admin created: username=admin password=admin123")
    db.close()
    print("\n🚀 FitPlan AI is running!")
    print("   Open : http://127.0.0.1:8080")
    print("   Admin: http://127.0.0.1:8080/admin (login as admin/admin123)\n")
    app.run(debug=False, host="127.0.0.1", port=8080, threaded=True)
