"""
seed_data.py - Creates sample test users with profiles.
Run this AFTER the app has been started at least once (to create DB tables).

Usage:
    python seed_data.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db, create_tables
from utils import hash_password
from services.workout_service import (
    calculate_bmi, categorize_bmi, calculate_bmr, calculate_daily_calories
)

TEST_USERS = [
    {
        "username": "testuser",
        "email": "test@fitplan.com",
        "password": "test123",
        "profile": {
            "age": 21, "gender": "male",
            "height_cm": 175.0, "weight_kg": 75.0,
            "fitness_goal": "muscle_gain",
            "dietary_preference": "non_veg",
            "cultural_preference": "indian",
            "budget_level": "medium",
            "equipment": "gym",
        }
    },
    {
        "username": "priya",
        "email": "priya@fitplan.com",
        "password": "priya123",
        "profile": {
            "age": 22, "gender": "female",
            "height_cm": 163.0, "weight_kg": 58.0,
            "fitness_goal": "weight_loss",
            "dietary_preference": "vegetarian",
            "cultural_preference": "indian",
            "budget_level": "low",
            "equipment": "home",
        }
    },
    {
        "username": "alex",
        "email": "alex@fitplan.com",
        "password": "alex123",
        "profile": {
            "age": 24, "gender": "male",
            "height_cm": 180.0, "weight_kg": 90.0,
            "fitness_goal": "weight_loss",
            "dietary_preference": "non_veg",
            "cultural_preference": "western",
            "budget_level": "high",
            "equipment": "gym",
        }
    },
]


def seed():
    create_tables()
    db = get_db()

    for ud in TEST_USERS:
        existing = db.execute(
            "SELECT id FROM users WHERE username = ?", (ud["username"],)
        ).fetchone()

        if existing:
            print(f"⚠️  User '{ud['username']}' already exists, skipping.")
            continue

        db.execute(
            "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
            (ud["username"], ud["email"], hash_password(ud["password"]))
        )
        db.commit()
        user = db.execute("SELECT id FROM users WHERE username = ?", (ud["username"],)).fetchone()

        p = ud["profile"]
        bmi = calculate_bmi(p["weight_kg"], p["height_cm"])
        bmi_cat = categorize_bmi(bmi)
        bmr = calculate_bmr(p["age"], p["gender"], p["weight_kg"], p["height_cm"])
        daily_cal = calculate_daily_calories(bmr, p["fitness_goal"], bmi_cat)

        db.execute("""
            INSERT INTO user_profiles
                (user_id, age, gender, height_cm, weight_kg, bmi, bmi_category,
                 fitness_goal, dietary_preference, cultural_preference,
                 budget_level, equipment, bmr, daily_calories)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user["id"], p["age"], p["gender"], p["height_cm"], p["weight_kg"],
              bmi, bmi_cat, p["fitness_goal"], p["dietary_preference"],
              p["cultural_preference"], p["budget_level"], p["equipment"], bmr, daily_cal))
        db.commit()

        print(f"✅ Created: {ud['username']} | BMI: {bmi} ({bmi_cat}) | Calories: {int(daily_cal)}/day")

    db.close()
    print("\n🌱 Seed complete!")
    print("\n📋 Test Accounts:")
    for ud in TEST_USERS:
        print(f"   {ud['username']:12} | password: {ud['password']}")


if __name__ == "__main__":
    seed()
