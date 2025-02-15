from langchain.tools import BaseTool
from pydantic import BaseModel, ValidationError
from typing import Dict, Any

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str

class Meal(BaseModel):
    name: str
    prep_time_minutes: int
    calories_per_person: int
    ingredients: list[Ingredient]
    recipe: str

class MealsData(BaseModel):
    year: int
    month: str
    day: int
    meals: Dict[str, Meal]

class JSONValidatorTool(BaseTool):
    name = "json_validator"
    description = "Validates a JSON input to check if it follows the expected meal structure."
    
    def _run(self, json_data: Dict[str, Any]) -> str:
        try:
            MealsData(**json_data)
            return "JSON is valid."
        except ValidationError as e:
            return f"Invalid JSON format: {e}"
    
    async def _arun(self, json_data: Dict[str, Any]) -> str:
        raise NotImplementedError("JSONValidatorTool does not support async yet.")
