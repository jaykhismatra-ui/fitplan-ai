# services/workout_service.py
# Rule-based AI engine for generating personalized workout plans

# ─── EXERCISE DATABASE ────────────────────────────────────────────────────────

EXERCISES = {
    "gym": {
        "chest": [
            {"name": "Bench Press", "sets": 4, "reps": "8-10", "rest_sec": 90, "muscle": "Pectorals"},
            {"name": "Incline Dumbbell Press", "sets": 3, "reps": "10-12", "rest_sec": 75, "muscle": "Upper Chest"},
            {"name": "Cable Flyes", "sets": 3, "reps": "12-15", "rest_sec": 60, "muscle": "Chest"},
        ],
        "back": [
            {"name": "Deadlift", "sets": 4, "reps": "5-6", "rest_sec": 120, "muscle": "Full Back"},
            {"name": "Pull-Ups / Lat Pulldown", "sets": 4, "reps": "8-10", "rest_sec": 90, "muscle": "Lats"},
            {"name": "Seated Cable Row", "sets": 3, "reps": "10-12", "rest_sec": 75, "muscle": "Mid Back"},
        ],
        "legs": [
            {"name": "Barbell Squat", "sets": 4, "reps": "8-10", "rest_sec": 120, "muscle": "Quads / Glutes"},
            {"name": "Leg Press", "sets": 3, "reps": "12-15", "rest_sec": 90, "muscle": "Quads"},
            {"name": "Romanian Deadlift", "sets": 3, "reps": "10-12", "rest_sec": 90, "muscle": "Hamstrings"},
            {"name": "Calf Raises", "sets": 4, "reps": "15-20", "rest_sec": 60, "muscle": "Calves"},
        ],
        "shoulders": [
            {"name": "Overhead Press", "sets": 4, "reps": "8-10", "rest_sec": 90, "muscle": "Deltoids"},
            {"name": "Lateral Raises", "sets": 3, "reps": "12-15", "rest_sec": 60, "muscle": "Side Delts"},
            {"name": "Face Pulls", "sets": 3, "reps": "15", "rest_sec": 60, "muscle": "Rear Delts"},
        ],
        "arms": [
            {"name": "Barbell Curl", "sets": 3, "reps": "10-12", "rest_sec": 60, "muscle": "Biceps"},
            {"name": "Tricep Pushdown", "sets": 3, "reps": "10-12", "rest_sec": 60, "muscle": "Triceps"},
            {"name": "Hammer Curl", "sets": 3, "reps": "12", "rest_sec": 60, "muscle": "Brachialis"},
        ],
        "cardio": [
            {"name": "Treadmill Run", "sets": 1, "reps": "30 min", "rest_sec": 0, "muscle": "Cardiovascular"},
            {"name": "Stationary Bike", "sets": 1, "reps": "25 min", "rest_sec": 0, "muscle": "Cardiovascular"},
            {"name": "Rowing Machine", "sets": 1, "reps": "20 min", "rest_sec": 0, "muscle": "Full Body Cardio"},
        ],
        "core": [
            {"name": "Cable Crunches", "sets": 3, "reps": "15-20", "rest_sec": 60, "muscle": "Abs"},
            {"name": "Hanging Leg Raises", "sets": 3, "reps": "12-15", "rest_sec": 60, "muscle": "Core"},
            {"name": "Plank", "sets": 3, "reps": "60 sec", "rest_sec": 60, "muscle": "Core"},
        ],
    },
    "home": {
        "chest": [
            {"name": "Push-Ups", "sets": 4, "reps": "15-20", "rest_sec": 60, "muscle": "Chest"},
            {"name": "Wide Push-Ups", "sets": 3, "reps": "12-15", "rest_sec": 60, "muscle": "Outer Chest"},
            {"name": "Diamond Push-Ups", "sets": 3, "reps": "10-12", "rest_sec": 60, "muscle": "Inner Chest / Triceps"},
        ],
        "back": [
            {"name": "Superman Hold", "sets": 3, "reps": "12-15", "rest_sec": 60, "muscle": "Lower Back"},
            {"name": "Resistance Band Rows", "sets": 3, "reps": "15", "rest_sec": 60, "muscle": "Back"},
            {"name": "Doorframe Pull-Ups", "sets": 3, "reps": "8-10", "rest_sec": 75, "muscle": "Lats"},
        ],
        "legs": [
            {"name": "Bodyweight Squats", "sets": 4, "reps": "20-25", "rest_sec": 60, "muscle": "Quads"},
            {"name": "Lunges", "sets": 3, "reps": "15 each leg", "rest_sec": 60, "muscle": "Quads / Glutes"},
            {"name": "Glute Bridges", "sets": 3, "reps": "20", "rest_sec": 60, "muscle": "Glutes / Hamstrings"},
            {"name": "Wall Sit", "sets": 3, "reps": "45 sec", "rest_sec": 60, "muscle": "Quads"},
        ],
        "shoulders": [
            {"name": "Pike Push-Ups", "sets": 3, "reps": "10-12", "rest_sec": 60, "muscle": "Shoulders"},
            {"name": "Lateral Arm Raises (water bottles)", "sets": 3, "reps": "15", "rest_sec": 60, "muscle": "Side Delts"},
        ],
        "arms": [
            {"name": "Tricep Dips (chair)", "sets": 3, "reps": "12-15", "rest_sec": 60, "muscle": "Triceps"},
            {"name": "Resistance Band Curls", "sets": 3, "reps": "15", "rest_sec": 60, "muscle": "Biceps"},
        ],
        "cardio": [
            {"name": "Jumping Jacks", "sets": 3, "reps": "40", "rest_sec": 30, "muscle": "Full Body"},
            {"name": "High Knees", "sets": 3, "reps": "30 sec", "rest_sec": 30, "muscle": "Cardiovascular"},
            {"name": "Burpees", "sets": 3, "reps": "10", "rest_sec": 45, "muscle": "Full Body"},
        ],
        "core": [
            {"name": "Crunches", "sets": 3, "reps": "20", "rest_sec": 45, "muscle": "Abs"},
            {"name": "Leg Raises", "sets": 3, "reps": "15", "rest_sec": 45, "muscle": "Lower Abs"},
            {"name": "Plank", "sets": 3, "reps": "45 sec", "rest_sec": 60, "muscle": "Core"},
            {"name": "Russian Twists", "sets": 3, "reps": "20 total", "rest_sec": 45, "muscle": "Obliques"},
        ],
    },
    "none": {
        "full_body": [
            {"name": "Push-Ups", "sets": 3, "reps": "10-15", "rest_sec": 60, "muscle": "Chest / Arms"},
            {"name": "Bodyweight Squats", "sets": 3, "reps": "20", "rest_sec": 60, "muscle": "Legs"},
            {"name": "Plank", "sets": 3, "reps": "30 sec", "rest_sec": 45, "muscle": "Core"},
            {"name": "Lunges", "sets": 3, "reps": "10 each leg", "rest_sec": 60, "muscle": "Legs"},
            {"name": "Glute Bridges", "sets": 3, "reps": "15", "rest_sec": 45, "muscle": "Glutes"},
        ],
        "cardio": [
            {"name": "Brisk Walking / Jogging", "sets": 1, "reps": "30 min", "rest_sec": 0, "muscle": "Cardiovascular"},
            {"name": "Jumping Jacks", "sets": 3, "reps": "30", "rest_sec": 30, "muscle": "Full Body"},
            {"name": "High Knees", "sets": 3, "reps": "30 sec", "rest_sec": 30, "muscle": "Cardiovascular"},
        ],
        "core": [
            {"name": "Crunches", "sets": 3, "reps": "15", "rest_sec": 45, "muscle": "Abs"},
            {"name": "Plank", "sets": 3, "reps": "30 sec", "rest_sec": 45, "muscle": "Core"},
            {"name": "Leg Raises", "sets": 3, "reps": "12", "rest_sec": 45, "muscle": "Lower Abs"},
        ],
    },
}

# Weekly templates: maps (equipment, goal) → 7-day muscle focus sequence
WEEKLY_TEMPLATES = {
    "gym": {
        "muscle_gain": ["chest", "back", "legs", "shoulders", "arms", "cardio", "rest"],
        "weight_loss": ["cardio", "full_body_circuit", "cardio", "full_body_circuit", "cardio", "core", "rest"],
        "maintenance": ["chest", "cardio", "legs", "rest", "back", "shoulders", "core"],
    },
    "home": {
        "muscle_gain": ["chest", "back", "legs", "shoulders", "arms", "cardio", "rest"],
        "weight_loss": ["cardio", "legs", "cardio", "chest", "cardio", "core", "rest"],
        "maintenance": ["chest", "cardio", "legs", "rest", "cardio", "core", "rest"],
    },
    "none": {
        "muscle_gain": ["full_body", "rest", "full_body", "rest", "full_body", "cardio", "rest"],
        "weight_loss": ["cardio", "full_body", "cardio", "full_body", "cardio", "core", "rest"],
        "maintenance": ["full_body", "cardio", "rest", "full_body", "cardio", "rest", "core"],
    },
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate BMI from weight and height."""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def categorize_bmi(bmi: float) -> str:
    """Categorize BMI into standard WHO ranges."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmr(age: int, gender: str, weight_kg: float, height_cm: float) -> float:
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation."""
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return round(bmr, 1)


def calculate_daily_calories(bmr: float, fitness_goal: str, bmi_category: str) -> float:
    """Estimate daily calorie needs based on goal and activity level."""
    # Moderate activity multiplier (suitable for students)
    tdee = bmr * 1.55

    if fitness_goal == "weight_loss":
        return round(tdee - 500, 0)     # 500 cal deficit → ~0.5 kg/week loss
    elif fitness_goal == "muscle_gain":
        return round(tdee + 300, 0)     # 300 cal surplus for lean gains
    else:
        return round(tdee, 0)           # Maintenance = TDEE


def _get_intensity(bmi_category: str, fitness_goal: str) -> str:
    """Determine workout intensity based on BMI and goal."""
    if bmi_category in ("Obese", "Overweight"):
        return "low_to_moderate"        # Reduce injury risk
    elif bmi_category == "Underweight":
        return "moderate"               # Build gradually
    else:
        if fitness_goal == "muscle_gain":
            return "high"
        elif fitness_goal == "weight_loss":
            return "moderate_to_high"
        else:
            return "moderate"


def _adjust_for_intensity(exercise: dict, intensity: str) -> dict:
    """Scale sets/reps based on workout intensity."""
    ex = dict(exercise)  # Copy to avoid mutating original
    if intensity == "low_to_moderate":
        ex["sets"] = max(2, ex["sets"] - 1)
        ex["note"] = "Focus on form. Take longer rests if needed."
    elif intensity == "high":
        ex["sets"] = min(5, ex["sets"] + 1)
        ex["note"] = "Push hard. Progressive overload each week."
    else:
        ex["note"] = "Maintain steady pace and good form."
    return ex


def _get_duration(focus: str, intensity: str) -> int:
    """Estimate workout duration in minutes."""
    base = {"cardio": 35, "core": 25, "rest": 0, "full_body": 40, "full_body_circuit": 40}
    if focus in base:
        return base[focus]
    return 50 if intensity == "high" else 40 if intensity == "moderate" else 35


def generate_workout_plan(profile: dict) -> dict:
    """
    Main AI engine: generates a 7-day personalized workout plan.
    profile is a dict with keys: equipment, fitness_goal, bmi_category
    """
    equipment = profile["equipment"]
    goal = profile["fitness_goal"]
    bmi_cat = profile["bmi_category"]
    intensity = _get_intensity(bmi_cat, goal)

    template = WEEKLY_TEMPLATES.get(equipment, WEEKLY_TEMPLATES["none"])
    day_sequence = template.get(goal, template["maintenance"])
    ex_db = EXERCISES.get(equipment, EXERCISES["none"])

    weekly_plan = []

    for i, focus in enumerate(day_sequence):
        day_name = DAYS[i]

        if focus == "rest":
            weekly_plan.append({
                "day": day_name,
                "focus": "Rest / Active Recovery",
                "exercises": [{"name": "Light Walk / Stretching", "sets": 1, "reps": "20-30 min",
                               "rest_sec": 0, "muscle": "Recovery", "note": "Let your body recover."}],
                "total_duration_minutes": 20,
            })
            continue

        if focus in ex_db:
            exercises = [_adjust_for_intensity(e, intensity) for e in ex_db[focus]]
        elif focus == "full_body_circuit":
            exercises = []
            for muscle in ["chest", "legs", "core", "cardio"]:
                if muscle in ex_db:
                    exercises.append(_adjust_for_intensity(ex_db[muscle][0], intensity))
        elif focus == "full_body" and "full_body" in ex_db:
            exercises = [_adjust_for_intensity(e, intensity) for e in ex_db["full_body"]]
        else:
            exercises = []
            for muscle in ["cardio", "core"]:
                if muscle in ex_db:
                    exercises.extend([_adjust_for_intensity(e, intensity) for e in ex_db[muscle][:2]])

        weekly_plan.append({
            "day": day_name,
            "focus": focus.replace("_", " ").title(),
            "exercises": exercises,
            "total_duration_minutes": _get_duration(focus, intensity),
        })

    intensity_labels = {
        "low_to_moderate": "Low to Moderate",
        "moderate": "Moderate",
        "moderate_to_high": "Moderate to High",
        "high": "High",
    }

    return {
        "weekly_plan": weekly_plan,
        "intensity": intensity_labels.get(intensity, intensity),
        "notes": _build_workout_notes(bmi_cat, goal, equipment),
    }


def _build_workout_notes(bmi_cat: str, goal: str, equipment: str) -> str:
    """Generate smart workout advice based on user data."""
    notes = []
    if bmi_cat == "Obese":
        notes.append("Start slow — consistency over intensity. Consider consulting a doctor.")
    elif bmi_cat == "Overweight":
        notes.append("Cardio + strength training is the winning combo for fat loss.")
    elif bmi_cat == "Underweight":
        notes.append("Focus on progressive overload and eat in a calorie surplus.")

    if goal == "weight_loss":
        notes.append("Stay hydrated and maintain your calorie deficit throughout the week.")
    elif goal == "muscle_gain":
        notes.append("Prioritize compound lifts and consume 1.6–2.2g protein per kg of body weight.")
    else:
        notes.append("Consistency is key — aim for 4-5 active days per week.")

    if equipment == "none":
        notes.append("No equipment? Bodyweight training is highly effective when done consistently!")

    return " | ".join(notes)
