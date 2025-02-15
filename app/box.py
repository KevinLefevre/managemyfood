import os
import json

class DayMeal:
    def __init__(self, year: int, month: int, day: int, base_dir: str = "data"):
        self.year = year
        self.month = month
        self.day = day
        self.base_dir = base_dir
        self.lunch = None   # Will store lunch meal dict
        self.dinner = None  # Will store dinner meal dict

    def load_data(self):
        """ Load the JSON file for this day into self.lunch and self.dinner. """
        month_str = f"{self.month:02d}"
        day_str = f"{self.day:02d}"
        file_path = os.path.join(self.base_dir, str(self.year), month_str, f"{day_str}.json")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        meals = data.get("meals", {})
        self.lunch = meals.get("lunch", None)
        self.dinner = meals.get("dinner", None)

    def get_lunch_name(self):
        if self.lunch and "name" in self.lunch:
            return self.lunch["name"]
        return ""

    def get_dinner_name(self):
        if self.dinner and "name" in self.dinner:
            return self.dinner["name"]
        return ""
