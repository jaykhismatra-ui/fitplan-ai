# 💪 FitPlan AI — Personalized Workout & Diet Planner

A full-stack AI-powered web app built with **Python (Flask) + SQLite + HTML/CSS/JS**.
Generates intelligent, personalized workout and diet plans based on body type, goals, cultural food habits, and budget — **zero paid APIs required**.

---

## 📁 Project Structure

```
workout_planner/
├── main.py                  # Flask app — all routes
├── database.py              # SQLite setup (built-in sqlite3)
├── utils.py                 # Password hashing, validation
├── seed_data.py             # Create sample test users
├── requirements.txt
│
├── services/
│   ├── workout_service.py   # AI workout generation engine
│   └── diet_service.py      # AI diet generation engine
│
├── templates/               # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html / register.html
│   ├── profile.html
│   ├── dashboard.html
│   ├── workout_plan.html
│   └── diet_plan.html
│
└── static/
    ├── css/style.css
    └── js/app.js
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.9 or higher (Python 3.12 tested ✅)
- No external database required — SQLite is built into Python

### Step 1: (Optional) Create Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
> Note: Flask, Werkzeug, and Jinja2 are the only dependencies. All are standard and free.

### Step 3: Run the Application
```bash
python main.py
```

### Step 4: Open in Browser
```
http://localhost:5000
```

### Step 5: (Optional) Create Sample Test Users
```bash
python seed_data.py
```

---

## 🧪 Sample Test Accounts

| Username | Password  | Goal        | Diet       | Culture | Budget |
|----------|-----------|-------------|------------|---------|--------|
| testuser | test123   | Muscle Gain | Non-Veg    | Indian  | Medium |
| priya    | priya123  | Weight Loss | Vegetarian | Indian  | Low    |
| alex     | alex123   | Weight Loss | Non-Veg    | Western | High   |

> These accounts are pre-populated with profiles. Just log in and click "Generate Plan"!

---

## 🤖 AI Logic Explained

### 1. BMI Calculation
```
BMI = weight (kg) / height (m)²
```
| Range     | Category    |
|-----------|-------------|
| < 18.5    | Underweight |
| 18.5–24.9 | Normal      |
| 25–29.9   | Overweight  |
| ≥ 30      | Obese       |

### 2. BMR (Basal Metabolic Rate) — Mifflin-St Jeor Equation
```
Male:   BMR = 10W + 6.25H - 5A + 5
Female: BMR = 10W + 6.25H - 5A - 161
```
*(W = weight in kg, H = height in cm, A = age in years)*

### 3. Daily Calorie Target
```
TDEE = BMR × 1.55 (moderate activity)
Weight Loss:  TDEE - 500 kcal
Muscle Gain:  TDEE + 300 kcal
Maintenance:  TDEE
```

### 4. Workout Personalization
- Equipment → selects gym/home/bodyweight exercises
- Goal + BMI → determines intensity (low/moderate/high)
- Sets/reps auto-scaled per intensity level
- 7-day template varies per goal type

### 5. Diet Personalization
- Cultural preference → Indian/Western/Mixed food database
- Dietary type → filters Veg/Vegan/Non-Veg items
- Budget → filters affordable options (low/medium/high)
- Calorie split: 25% breakfast | 35% lunch | 30% dinner | 10% snacks

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3.9+ with Flask            |
| Database   | SQLite (via Python's sqlite3)     |
| Templates  | Jinja2 (included with Flask)      |
| Frontend   | HTML5 + CSS3 + Vanilla JavaScript |
| Auth       | Session-based + SHA-256 password  |
| Server     | Flask dev server (Werkzeug)       |

---

## 🔑 Key Features

- ✅ User registration & login (session-based)
- ✅ Profile setup with BMI auto-calculation
- ✅ 7-day personalized workout plan
- ✅ Daily meal plan (4 meals: B/L/D/S)
- ✅ Cultural food adaptation (Indian / Western / Mixed)
- ✅ Budget-aware diet selection
- ✅ Equipment-based workout adaptation
- ✅ Calorie & macro breakdown
- ✅ Plan regeneration + history stored in DB
- ✅ Live BMI calculator on profile form
- ✅ Mobile-responsive UI
- ✅ Zero external paid API dependencies
