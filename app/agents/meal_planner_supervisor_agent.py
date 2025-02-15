# app/agents/meal_planner_supervisor_agent.py

from typing import List, Dict, Any
import datetime

from app.agents.meal_creation_agent import MealCreationAgent
from app.tools.write_meal_file_tool import WriteMealFileTool

class MealPlannerSupervisorAgent:
    """
    A supervisor agent that orchestrates multiple day meal creation
    and writes them to disk.
    """

    def __init__(self, openai_api_key: str):
        """
        Args:
            openai_api_key: Your OpenAI API key for the creation agent.
        """
        self.openai_api_key = openai_api_key
        self.meal_creator = MealCreationAgent(openai_api_key=self.openai_api_key)
        self.file_writer = WriteMealFileTool()

    def create_multi_day_plan(self, start_year: int, start_month: int, start_day: int,
                              num_days: int, user_constraints: str) -> List[Dict[str, Any]]:
        """
        Generates a multi-day plan by calling the meal creation agent for each day,
        then writes each day’s JSON to data/<year>/<month>/<day>.json
        """
        plan_data = []
        date_obj = datetime.date(start_year, start_month, start_day)

        for i in range(num_days):
            # Each day, create a meal JSON
            constraints = f"For day {date_obj}, {user_constraints}"
            meal_json = self.meal_creator.create_meal(constraints)

            # Overwrite the day fields with the correct date
            meal_json["year"] = date_obj.year
            meal_json["month"] = f"{date_obj.month:02d}"  # or just int if you prefer
            meal_json["day"] = date_obj.day

            # Write to disk
            self.file_writer.run(meal_json)

            plan_data.append(meal_json)
            # Move to next day
            date_obj += datetime.timedelta(days=1)

        return plan_data
