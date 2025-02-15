import os
import json
from langchain.tools import BaseTool
from typing import Dict, Any

class WriteMealFileTool(BaseTool):
    name = "write_meal_file"
    description = "Writes a meal JSON to the correct day file in data/<year>/<month>/<day>.json."

    def _run(self, meal_json: Dict[str, Any]) -> str:
        """
        meal_json: A dictionary matching the MealsData schema.
        We'll store it in data/<year>/<month>/<day>.json
        """
        year = meal_json["year"]
        month_str = str(meal_json["month"]).zfill(2)
        day_num = meal_json["day"]
        day_str = str(day_num).zfill(2)

        folder_path = os.path.join("data", str(year), month_str)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"{day_str}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(meal_json, f, indent=2)

        return f"Meal JSON written to {file_path}"

    async def _arun(self, meal_json: Dict[str, Any]) -> str:
        raise NotImplementedError("WriteMealFileTool does not support async yet.")
