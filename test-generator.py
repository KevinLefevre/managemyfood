import os
import json
import calendar
import random

def generate_daily_json(year=2025, base_dir="data"):
    """
    For each month (1..12), create a subfolder data/<year>/<month:02d>/
    Then for each day in that month, create day.json (01.json, 02.json, etc.).
    Each file includes a sample 'lunch' and 'dinner' with fields:
      name, prep_time_minutes, calories_per_person, ingredients, recipe.
    """
    # Sample data for demonstration
    sample_lunches = [
        {
            "name": "Grilled Chicken Salad",
            "prep_time_minutes": 15,
            "calories_per_person": 320,
            "ingredients": [
                {"name": "Chicken Breast", "quantity": 1, "unit": "pc"},
                {"name": "Lettuce",        "quantity": 2, "unit": "cup"},
                {"name": "Tomato",         "quantity": 1, "unit": "pc"}
            ],
            "recipe": "1) Season and grill chicken.\n2) Chop lettuce and tomato.\n3) Toss with dressing."
        },
        {
            "name": "Veggie Wrap",
            "prep_time_minutes": 10,
            "calories_per_person": 280,
            "ingredients": [
                {"name": "Tortilla",      "quantity": 1, "unit": "pc"},
                {"name": "Mixed Veggies", "quantity": 1, "unit": "cup"},
                {"name": "Cheese",        "quantity": 1, "unit": "slice"}
            ],
            "recipe": "1) Warm tortilla.\n2) Fill with veggies and cheese.\n3) Roll it up."
        },
        {
            "name": "Tuna Sandwich",
            "prep_time_minutes": 5,
            "calories_per_person": 300,
            "ingredients": [
                {"name": "Bread", "quantity": 2, "unit": "slice"},
                {"name": "Tuna",  "quantity": 1, "unit": "can"},
                {"name": "Mayo",  "quantity": 1, "unit": "tbsp"}
            ],
            "recipe": "1) Drain tuna.\n2) Mix with mayo.\n3) Spread on bread."
        }
    ]

    sample_dinners = [
        {
            "name": "Pasta Bolognese",
            "prep_time_minutes": 25,
            "calories_per_person": 450,
            "ingredients": [
                {"name": "Spaghetti",     "quantity": 200, "unit": "g"},
                {"name": "Ground Beef",   "quantity": 100, "unit": "g"},
                {"name": "Tomato Sauce",  "quantity": 1,   "unit": "cup"}
            ],
            "recipe": "1) Brown beef.\n2) Add sauce and simmer.\n3) Boil pasta and combine."
        },
        {
            "name": "Chicken Fajitas",
            "prep_time_minutes": 20,
            "calories_per_person": 400,
            "ingredients": [
                {"name": "Tortilla",       "quantity": 2,  "unit": "pc"},
                {"name": "Chicken Breast", "quantity": 1,  "unit": "pc"},
                {"name": "Bell Pepper",    "quantity": 1,  "unit": "pc"}
            ],
            "recipe": "1) Slice chicken & peppers.\n2) Sauté with seasoning.\n3) Serve in tortillas."
        },
        {
            "name": "Vegetable Stir-Fry",
            "prep_time_minutes": 15,
            "calories_per_person": 350,
            "ingredients": [
                {"name": "Mixed Veggies",  "quantity": 2,  "unit": "cup"},
                {"name": "Soy Sauce",      "quantity": 2,  "unit": "tbsp"},
                {"name": "Tofu",           "quantity": 1,  "unit": "cup"}
            ],
            "recipe": "1) Sauté veggies & tofu.\n2) Add soy sauce.\n3) Stir until tender."
        }
    ]

    # Ensure the base directory for the year exists
    year_folder = os.path.join(base_dir, str(year))
    os.makedirs(year_folder, exist_ok=True)

    for month in range(1, 13):
        month_str = f"{month:02d}"
        month_folder = os.path.join(year_folder, month_str)
        os.makedirs(month_folder, exist_ok=True)

        # Number of days in this month
        _, num_days = calendar.monthrange(year, month)

        for day in range(1, num_days + 1):
            day_str = f"{day:02d}"
            day_json_path = os.path.join(month_folder, f"{day_str}.json")

            # Randomly pick a lunch & dinner from the samples
            lunch_choice = random.choice(sample_lunches)
            dinner_choice = random.choice(sample_dinners)

            # Build the dictionary for this day
            day_data = {
                "year": year,
                "month": month_str,
                "day": day,
                "meals": {
                    "lunch": lunch_choice,
                    "dinner": dinner_choice
                }
            }

            # Write day.json
            with open(day_json_path, "w", encoding="utf-8") as f:
                json.dump(day_data, f, indent=2)

            print(f"Created {day_json_path}")


if __name__ == "__main__":
    generate_daily_json(year=2025)
