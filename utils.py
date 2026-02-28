# utils.py - Utility functions: password hashing, validation

import hashlib
import os
import re


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with a random salt."""
    salt = os.urandom(32).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verify a plain password against a stored hash."""
    try:
        salt, hashed = stored_hash.split(":")
        return hashlib.sha256((salt + plain_password).encode()).hexdigest() == hashed
    except Exception:
        return False


def validate_profile(data: dict) -> list:
    """Validate profile form data. Returns list of error messages."""
    errors = []

    age = data.get("age", "")
    try:
        age = int(age)
        if not (10 <= age <= 100):
            errors.append("Age must be between 10 and 100.")
    except (ValueError, TypeError):
        errors.append("Age must be a valid number.")

    try:
        h = float(data.get("height_cm", 0))
        if not (100 <= h <= 250):
            errors.append("Height must be between 100 and 250 cm.")
    except (ValueError, TypeError):
        errors.append("Height must be a valid number.")

    try:
        w = float(data.get("weight_kg", 0))
        if not (20 <= w <= 300):
            errors.append("Weight must be between 20 and 300 kg.")
    except (ValueError, TypeError):
        errors.append("Weight must be a valid number.")

    valid_goals = ("weight_loss", "muscle_gain", "maintenance")
    if data.get("fitness_goal") not in valid_goals:
        errors.append("Please select a valid fitness goal.")

    valid_diets = ("vegetarian", "vegan", "non_veg")
    if data.get("dietary_preference") not in valid_diets:
        errors.append("Please select a valid dietary preference.")

    valid_cultures = ("indian", "western", "mixed")
    if data.get("cultural_preference") not in valid_cultures:
        errors.append("Please select a valid cultural preference.")

    valid_budgets = ("low", "medium", "high")
    if data.get("budget_level") not in valid_budgets:
        errors.append("Please select a valid budget level.")

    valid_equipment = ("gym", "home", "none")
    if data.get("equipment") not in valid_equipment:
        errors.append("Please select a valid equipment option.")

    return errors
