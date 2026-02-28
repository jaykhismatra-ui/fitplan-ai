# services/diet_service.py
# Rule-based AI engine for generating personalized diet plans

FOOD_DB = {
    "indian": {
        "vegetarian": {
            "breakfast": [
                {"name": "Poha (Flattened Rice)", "qty": "1 bowl (200g)", "cal": 250, "protein_g": 5, "carbs_g": 48, "fat_g": 5, "budget": ["low", "medium", "high"]},
                {"name": "Oats with Milk & Banana", "qty": "1 bowl", "cal": 300, "protein_g": 10, "carbs_g": 50, "fat_g": 6, "budget": ["low", "medium", "high"]},
                {"name": "Idli with Sambar (3 pieces)", "qty": "3 idlis + sambar", "cal": 280, "protein_g": 9, "carbs_g": 52, "fat_g": 4, "budget": ["low", "medium", "high"]},
                {"name": "Moong Dal Chilla (2 pieces)", "qty": "2 chillas", "cal": 220, "protein_g": 12, "carbs_g": 30, "fat_g": 5, "budget": ["low", "medium", "high"]},
                {"name": "Paneer Paratha with Curd", "qty": "2 parathas + curd", "cal": 450, "protein_g": 18, "carbs_g": 55, "fat_g": 16, "budget": ["medium", "high"]},
                {"name": "Upma with Vegetables", "qty": "1 plate", "cal": 240, "protein_g": 7, "carbs_g": 42, "fat_g": 7, "budget": ["low", "medium", "high"]},
            ],
            "lunch": [
                {"name": "Dal Rice + Mixed Vegetable", "qty": "1 plate", "cal": 520, "protein_g": 18, "carbs_g": 90, "fat_g": 8, "budget": ["low", "medium", "high"]},
                {"name": "Rajma Chawal", "qty": "1 plate", "cal": 560, "protein_g": 20, "carbs_g": 95, "fat_g": 9, "budget": ["low", "medium", "high"]},
                {"name": "Chole with Roti (3 rotis)", "qty": "1 bowl chole + 3 rotis", "cal": 580, "protein_g": 22, "carbs_g": 92, "fat_g": 12, "budget": ["low", "medium", "high"]},
                {"name": "Paneer Butter Masala + Rice", "qty": "1 plate", "cal": 680, "protein_g": 28, "carbs_g": 85, "fat_g": 22, "budget": ["medium", "high"]},
                {"name": "Sambar Rice + Papadum", "qty": "1 plate", "cal": 480, "protein_g": 15, "carbs_g": 88, "fat_g": 7, "budget": ["low", "medium", "high"]},
            ],
            "dinner": [
                {"name": "Roti (3) + Dal Tadka + Salad", "qty": "3 rotis + 1 bowl dal", "cal": 480, "protein_g": 20, "carbs_g": 80, "fat_g": 9, "budget": ["low", "medium", "high"]},
                {"name": "Khichdi with Ghee", "qty": "1 large bowl", "cal": 420, "protein_g": 16, "carbs_g": 72, "fat_g": 9, "budget": ["low", "medium", "high"]},
                {"name": "Palak Paneer + 2 Rotis", "qty": "1 bowl + 2 rotis", "cal": 520, "protein_g": 24, "carbs_g": 58, "fat_g": 18, "budget": ["medium", "high"]},
                {"name": "Vegetable Pulao + Raita", "qty": "1 plate + raita", "cal": 450, "protein_g": 12, "carbs_g": 80, "fat_g": 10, "budget": ["low", "medium", "high"]},
            ],
            "snacks": [
                {"name": "Roasted Chana (Chickpeas)", "qty": "30g", "cal": 110, "protein_g": 6, "carbs_g": 16, "fat_g": 2, "budget": ["low", "medium", "high"]},
                {"name": "Banana", "qty": "1 medium", "cal": 90, "protein_g": 1, "carbs_g": 23, "fat_g": 0, "budget": ["low", "medium", "high"]},
                {"name": "Buttermilk (Chaas)", "qty": "1 glass", "cal": 70, "protein_g": 4, "carbs_g": 8, "fat_g": 2, "budget": ["low", "medium", "high"]},
                {"name": "Makhana Roasted", "qty": "30g", "cal": 105, "protein_g": 4, "carbs_g": 20, "fat_g": 1, "budget": ["medium", "high"]},
                {"name": "Peanut Chikki", "qty": "1 piece (30g)", "cal": 145, "protein_g": 4, "carbs_g": 18, "fat_g": 7, "budget": ["low", "medium", "high"]},
            ],
        },
        "non_veg": {
            "breakfast": [
                {"name": "Egg Bhurji + Toast (2 eggs)", "qty": "2 eggs + 2 slices", "cal": 320, "protein_g": 18, "carbs_g": 30, "fat_g": 14, "budget": ["low", "medium", "high"]},
                {"name": "Boiled Eggs + Poha", "qty": "2 eggs + 1 bowl", "cal": 380, "protein_g": 22, "carbs_g": 45, "fat_g": 12, "budget": ["low", "medium", "high"]},
                {"name": "Omelette (3 eggs) + Roti", "qty": "3 eggs + 2 rotis", "cal": 420, "protein_g": 26, "carbs_g": 40, "fat_g": 16, "budget": ["low", "medium", "high"]},
                {"name": "Chicken Sandwich (Whole Wheat)", "qty": "2 slices + 80g chicken", "cal": 380, "protein_g": 30, "carbs_g": 35, "fat_g": 10, "budget": ["medium", "high"]},
            ],
            "lunch": [
                {"name": "Chicken Curry + Rice", "qty": "1 bowl curry + rice", "cal": 620, "protein_g": 40, "carbs_g": 80, "fat_g": 14, "budget": ["medium", "high"]},
                {"name": "Egg Curry + 3 Rotis", "qty": "2 eggs + 3 rotis", "cal": 540, "protein_g": 28, "carbs_g": 72, "fat_g": 16, "budget": ["low", "medium", "high"]},
                {"name": "Fish Curry + Rice", "qty": "1 serving", "cal": 580, "protein_g": 38, "carbs_g": 75, "fat_g": 12, "budget": ["medium", "high"]},
                {"name": "Egg Fried Rice", "qty": "1 large plate", "cal": 480, "protein_g": 20, "carbs_g": 75, "fat_g": 12, "budget": ["low", "medium", "high"]},
            ],
            "dinner": [
                {"name": "Tandoori Chicken + 2 Rotis + Salad", "qty": "2 pieces + rotis", "cal": 520, "protein_g": 45, "carbs_g": 42, "fat_g": 14, "budget": ["medium", "high"]},
                {"name": "Grilled Fish + Roti + Dal", "qty": "1 serving", "cal": 480, "protein_g": 40, "carbs_g": 48, "fat_g": 12, "budget": ["medium", "high"]},
                {"name": "Egg Curry + Rice", "qty": "3 eggs + rice", "cal": 500, "protein_g": 26, "carbs_g": 68, "fat_g": 14, "budget": ["low", "medium", "high"]},
                {"name": "Chicken Soup + Bread", "qty": "1 bowl + 2 slices", "cal": 360, "protein_g": 32, "carbs_g": 35, "fat_g": 8, "budget": ["medium", "high"]},
            ],
            "snacks": [
                {"name": "Boiled Eggs (2)", "qty": "2 eggs", "cal": 140, "protein_g": 12, "carbs_g": 2, "fat_g": 10, "budget": ["low", "medium", "high"]},
                {"name": "Roasted Chana", "qty": "30g", "cal": 110, "protein_g": 6, "carbs_g": 16, "fat_g": 2, "budget": ["low", "medium", "high"]},
                {"name": "Banana + Peanut Butter", "qty": "1 banana + 1 tbsp PB", "cal": 190, "protein_g": 5, "carbs_g": 28, "fat_g": 7, "budget": ["medium", "high"]},
            ],
        },
        "vegan": {
            "breakfast": [
                {"name": "Oats with Soy Milk & Fruits", "qty": "1 bowl", "cal": 280, "protein_g": 9, "carbs_g": 50, "fat_g": 5, "budget": ["medium", "high"]},
                {"name": "Moong Dal Chilla (2)", "qty": "2 pieces", "cal": 220, "protein_g": 12, "carbs_g": 30, "fat_g": 4, "budget": ["low", "medium", "high"]},
                {"name": "Poha with Peanuts", "qty": "1 bowl", "cal": 270, "protein_g": 7, "carbs_g": 48, "fat_g": 7, "budget": ["low", "medium", "high"]},
            ],
            "lunch": [
                {"name": "Dal Rice + Sabzi", "qty": "1 plate", "cal": 520, "protein_g": 18, "carbs_g": 90, "fat_g": 7, "budget": ["low", "medium", "high"]},
                {"name": "Rajma Chawal", "qty": "1 plate", "cal": 560, "protein_g": 20, "carbs_g": 95, "fat_g": 8, "budget": ["low", "medium", "high"]},
                {"name": "Lentil Soup + Brown Rice", "qty": "1 bowl + 1 cup rice", "cal": 480, "protein_g": 18, "carbs_g": 85, "fat_g": 5, "budget": ["low", "medium", "high"]},
            ],
            "dinner": [
                {"name": "Vegetable Khichdi", "qty": "1 large bowl", "cal": 400, "protein_g": 14, "carbs_g": 72, "fat_g": 7, "budget": ["low", "medium", "high"]},
                {"name": "Chickpea Curry + 2 Rotis", "qty": "1 bowl + 2 rotis", "cal": 480, "protein_g": 18, "carbs_g": 80, "fat_g": 10, "budget": ["low", "medium", "high"]},
                {"name": "Tofu Stir Fry + Brown Rice", "qty": "1 plate", "cal": 450, "protein_g": 20, "carbs_g": 68, "fat_g": 12, "budget": ["medium", "high"]},
            ],
            "snacks": [
                {"name": "Roasted Chana", "qty": "30g", "cal": 110, "protein_g": 6, "carbs_g": 16, "fat_g": 2, "budget": ["low", "medium", "high"]},
                {"name": "Banana", "qty": "1 medium", "cal": 90, "protein_g": 1, "carbs_g": 23, "fat_g": 0, "budget": ["low", "medium", "high"]},
                {"name": "Mixed Nuts (Almonds/Walnuts)", "qty": "30g", "cal": 180, "protein_g": 5, "carbs_g": 7, "fat_g": 16, "budget": ["medium", "high"]},
                {"name": "Peanut Chikki", "qty": "1 piece", "cal": 145, "protein_g": 4, "carbs_g": 18, "fat_g": 7, "budget": ["low", "medium", "high"]},
            ],
        },
    },
    "western": {
        "vegetarian": {
            "breakfast": [
                {"name": "Greek Yogurt + Granola + Berries", "qty": "1 bowl", "cal": 320, "protein_g": 15, "carbs_g": 45, "fat_g": 8, "budget": ["medium", "high"]},
                {"name": "Scrambled Eggs on Toast (2 eggs)", "qty": "2 eggs + 2 slices", "cal": 340, "protein_g": 18, "carbs_g": 30, "fat_g": 16, "budget": ["low", "medium", "high"]},
                {"name": "Oatmeal with Honey & Nuts", "qty": "1 bowl", "cal": 350, "protein_g": 10, "carbs_g": 55, "fat_g": 10, "budget": ["low", "medium", "high"]},
            ],
            "lunch": [
                {"name": "Quinoa Veggie Bowl", "qty": "1 large bowl", "cal": 480, "protein_g": 16, "carbs_g": 72, "fat_g": 12, "budget": ["medium", "high"]},
                {"name": "Grilled Cheese + Tomato Soup", "qty": "2 sandwiches + 1 bowl", "cal": 520, "protein_g": 20, "carbs_g": 62, "fat_g": 22, "budget": ["low", "medium", "high"]},
                {"name": "Caesar Salad + Whole Grain Bread", "qty": "1 plate + 2 slices", "cal": 440, "protein_g": 14, "carbs_g": 50, "fat_g": 18, "budget": ["medium", "high"]},
            ],
            "dinner": [
                {"name": "Pasta Primavera (Whole Wheat)", "qty": "1 large bowl", "cal": 500, "protein_g": 16, "carbs_g": 82, "fat_g": 10, "budget": ["low", "medium", "high"]},
                {"name": "Veggie Burger + Sweet Potato Fries", "qty": "1 burger + fries", "cal": 580, "protein_g": 20, "carbs_g": 80, "fat_g": 16, "budget": ["medium", "high"]},
                {"name": "Lentil Soup + Crusty Bread", "qty": "2 bowls + bread", "cal": 460, "protein_g": 20, "carbs_g": 75, "fat_g": 8, "budget": ["low", "medium", "high"]},
            ],
            "snacks": [
                {"name": "Apple + Peanut Butter", "qty": "1 apple + 2 tbsp PB", "cal": 200, "protein_g": 6, "carbs_g": 28, "fat_g": 9, "budget": ["low", "medium", "high"]},
                {"name": "Mixed Nuts", "qty": "30g", "cal": 180, "protein_g": 5, "carbs_g": 7, "fat_g": 16, "budget": ["medium", "high"]},
                {"name": "Banana", "qty": "1 medium", "cal": 90, "protein_g": 1, "carbs_g": 23, "fat_g": 0, "budget": ["low", "medium", "high"]},
            ],
        },
        "non_veg": {
            "breakfast": [
                {"name": "Scrambled Eggs (3) + Toast + Bacon", "qty": "3 eggs + 2 slices", "cal": 450, "protein_g": 30, "carbs_g": 30, "fat_g": 22, "budget": ["medium", "high"]},
                {"name": "Omelette (3 eggs) + Whole Wheat Toast", "qty": "3 eggs + 2 slices", "cal": 380, "protein_g": 26, "carbs_g": 28, "fat_g": 18, "budget": ["low", "medium", "high"]},
                {"name": "Greek Yogurt + Granola + Berries", "qty": "1 bowl", "cal": 320, "protein_g": 15, "carbs_g": 45, "fat_g": 8, "budget": ["medium", "high"]},
            ],
            "lunch": [
                {"name": "Grilled Chicken Salad", "qty": "1 large bowl", "cal": 420, "protein_g": 38, "carbs_g": 25, "fat_g": 16, "budget": ["medium", "high"]},
                {"name": "Chicken Wrap (Whole Wheat)", "qty": "1 large wrap", "cal": 480, "protein_g": 36, "carbs_g": 48, "fat_g": 12, "budget": ["medium", "high"]},
                {"name": "Tuna Sandwich (Whole Grain)", "qty": "2 sandwiches", "cal": 420, "protein_g": 32, "carbs_g": 40, "fat_g": 12, "budget": ["low", "medium", "high"]},
            ],
            "dinner": [
                {"name": "Grilled Chicken + Broccoli + Brown Rice", "qty": "1 serving", "cal": 520, "protein_g": 48, "carbs_g": 55, "fat_g": 10, "budget": ["medium", "high"]},
                {"name": "Salmon Fillet + Asparagus + Quinoa", "qty": "1 serving", "cal": 580, "protein_g": 46, "carbs_g": 52, "fat_g": 18, "budget": ["high"]},
                {"name": "Ground Turkey Pasta", "qty": "1 large bowl", "cal": 560, "protein_g": 40, "carbs_g": 70, "fat_g": 14, "budget": ["medium", "high"]},
            ],
            "snacks": [
                {"name": "Hard Boiled Eggs (2)", "qty": "2 eggs", "cal": 140, "protein_g": 12, "carbs_g": 2, "fat_g": 10, "budget": ["low", "medium", "high"]},
                {"name": "Cottage Cheese + Fruits", "qty": "1 cup + fruits", "cal": 180, "protein_g": 14, "carbs_g": 20, "fat_g": 4, "budget": ["medium", "high"]},
                {"name": "Apple + Peanut Butter", "qty": "1 apple + 2 tbsp PB", "cal": 200, "protein_g": 6, "carbs_g": 28, "fat_g": 9, "budget": ["low", "medium", "high"]},
            ],
        },
        "vegan": {
            "breakfast": [
                {"name": "Oatmeal with Almond Milk + Berries", "qty": "1 bowl", "cal": 300, "protein_g": 8, "carbs_g": 55, "fat_g": 7, "budget": ["medium", "high"]},
                {"name": "Peanut Butter Banana Smoothie", "qty": "1 glass", "cal": 320, "protein_g": 10, "carbs_g": 48, "fat_g": 12, "budget": ["medium", "high"]},
                {"name": "Avocado Toast (Whole Wheat)", "qty": "2 slices + avocado", "cal": 340, "protein_g": 8, "carbs_g": 38, "fat_g": 18, "budget": ["medium", "high"]},
            ],
            "lunch": [
                {"name": "Chickpea Buddha Bowl", "qty": "1 large bowl", "cal": 500, "protein_g": 18, "carbs_g": 75, "fat_g": 12, "budget": ["medium", "high"]},
                {"name": "Black Bean Burrito", "qty": "1 large burrito", "cal": 520, "protein_g": 20, "carbs_g": 78, "fat_g": 12, "budget": ["medium", "high"]},
                {"name": "Lentil Soup + Whole Grain Bread", "qty": "2 bowls + bread", "cal": 460, "protein_g": 20, "carbs_g": 75, "fat_g": 7, "budget": ["low", "medium", "high"]},
            ],
            "dinner": [
                {"name": "Tofu Stir Fry + Brown Rice", "qty": "1 plate", "cal": 480, "protein_g": 22, "carbs_g": 68, "fat_g": 14, "budget": ["medium", "high"]},
                {"name": "Vegan Pasta with Marinara + Lentils", "qty": "1 large bowl", "cal": 520, "protein_g": 18, "carbs_g": 85, "fat_g": 8, "budget": ["low", "medium", "high"]},
            ],
            "snacks": [
                {"name": "Banana", "qty": "1 medium", "cal": 90, "protein_g": 1, "carbs_g": 23, "fat_g": 0, "budget": ["low", "medium", "high"]},
                {"name": "Mixed Nuts", "qty": "30g", "cal": 180, "protein_g": 5, "carbs_g": 7, "fat_g": 16, "budget": ["medium", "high"]},
                {"name": "Hummus + Carrot Sticks", "qty": "3 tbsp + 100g carrot", "cal": 150, "protein_g": 5, "carbs_g": 18, "fat_g": 7, "budget": ["medium", "high"]},
                {"name": "Roasted Chickpeas", "qty": "30g", "cal": 120, "protein_g": 6, "carbs_g": 18, "fat_g": 3, "budget": ["low", "medium", "high"]},
            ],
        },
    },
}


def _filter_by_budget(items, budget):
    return [i for i in items if budget in i["budget"]]


def _select_meals(items, target_calories, count=1):
    if not items:
        return []
    items_sorted = sorted(items, key=lambda x: abs(x["cal"] - target_calories))
    return items_sorted[:count]


def generate_diet_plan(profile: dict) -> dict:
    """
    Main AI engine: generates a daily personalized diet plan.
    profile is a dict with diet/cultural/budget/goal keys.
    """
    cultural = profile["cultural_preference"]
    diet_type = profile["dietary_preference"]
    budget = profile["budget_level"]
    target_calories = profile.get("daily_calories") or 2000
    fitness_goal = profile["fitness_goal"]

    cultures = ["indian", "western"] if cultural == "mixed" else [cultural]

    def get_items(meal_type):
        items = []
        for cult in cultures:
            db = FOOD_DB.get(cult, {}).get(diet_type, {})
            items.extend(db.get(meal_type, []))
        filtered = _filter_by_budget(items, budget)
        if not filtered:
            # Fallback: ignore budget constraint
            return items
        return filtered

    splits = {"breakfast": 0.25, "lunch": 0.35, "dinner": 0.30, "snacks": 0.10}
    plan = {}
    actual_total = 0

    for meal_type, ratio in splits.items():
        meal_target = target_calories * ratio
        available = get_items(meal_type)
        count = 2 if meal_type == "snacks" else 1
        selected = _select_meals(available, meal_target // count, count=count)

        formatted = []
        for item in selected:
            formatted.append({
                "name": item["name"],
                "qty": item["qty"],
                "cal": item["cal"],
                "protein_g": item["protein_g"],
                "carbs_g": item["carbs_g"],
                "fat_g": item["fat_g"],
            })
            actual_total += item["cal"]

        plan[meal_type] = formatted

    total_protein = sum(i["protein_g"] for items in plan.values() for i in items)
    total_carbs = sum(i["carbs_g"] for items in plan.values() for i in items)
    total_fat = sum(i["fat_g"] for items in plan.values() for i in items)

    return {
        "breakfast": plan.get("breakfast", []),
        "lunch": plan.get("lunch", []),
        "dinner": plan.get("dinner", []),
        "snacks": plan.get("snacks", []),
        "total_calories": actual_total,
        "total_protein_g": round(total_protein, 1),
        "total_carbs_g": round(total_carbs, 1),
        "total_fat_g": round(total_fat, 1),
        "target_calories": int(target_calories),
        "notes": _build_diet_notes(profile, actual_total),
    }


def _build_diet_notes(profile: dict, actual_cal: int) -> str:
    notes = []
    if profile.get("budget_level") == "low":
        notes.append("Budget-friendly picks! Dal, rice, eggs, and seasonal vegetables are affordable & nutritious.")
    if profile.get("fitness_goal") == "muscle_gain":
        notes.append("Aim for 1.6–2g of protein per kg body weight. Add protein snacks between meals.")
    elif profile.get("fitness_goal") == "weight_loss":
        notes.append("Keep portions in check. Eat slowly, stay hydrated, and avoid processed foods.")
    if profile.get("dietary_preference") == "vegan":
        notes.append("Ensure you get B12, iron, and omega-3 from fortified foods or supplements.")
    if profile.get("bmi_category") in ("Obese", "Overweight"):
        notes.append("Reduce refined carbs and fried foods. Prioritize vegetables and lean proteins.")
    return " | ".join(notes) if notes else "Follow the plan consistently and stay well hydrated throughout the day."
