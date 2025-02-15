# app/agents/meal_creation_agent.py

import json
from typing import Dict, Any

from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Suppose you have your JSONValidatorTool
# from app.tools.json_validator_tool import JSONValidatorTool
# Or adjust import path accordingly
from app.tools.json_validator_tool import JSONValidatorTool

MEAL_CREATION_PROMPT = """
You are a meal creation assistant. The user wants a meal with certain constraints:

{user_constraints}

Output valid JSON matching this Pydantic schema:

{
  "year": <int>,
  "month": "<string>",
  "day": <int>,
  "meals": {
    "lunch": {
      "name": "<string>",
      "prep_time_minutes": <int>,
      "calories_per_person": <int>,
      "ingredients": [
        { "name": "<string>", "quantity": <float>, "unit": "<string>" }
      ],
      "recipe": "<string>"
    },
    "dinner": {
      "name": "<string>",
      "prep_time_minutes": <int>,
      "calories_per_person": <int>,
      "ingredients": [
        { "name": "<string>", "quantity": <float>, "unit": "<string>" }
      ],
      "recipe": "<string>"
    }
  }
}

No extra commentary, only JSON.
"""

class MealCreationAgent:
    """
    A simple agent that, given user constraints, produces a single day’s
    meal JSON (both lunch and dinner) validated by JSONValidatorTool.
    """

    def __init__(self, openai_api_key: str, temperature: float = 0.7):
        """
        Args:
            openai_api_key: Your OpenAI API key.
            temperature: LLM temperature for creativity.
        """
        self.openai_api_key = openai_api_key
        self.temperature = temperature
        self._setup_chain()

    def _setup_chain(self):
        """
        Creates the LLMChain with a prompt template for meal creation.
        """
        prompt = PromptTemplate(
            input_variables=["user_constraints"],
            template=MEAL_CREATION_PROMPT
        )
        # Create an LLM instance with the provided API key
        self.llm = OpenAI(
            openai_api_key=self.openai_api_key,
            temperature=self.temperature
        )
        self.chain = LLMChain(llm=self.llm, prompt=prompt)
        self.validator_tool = JSONValidatorTool()

    def create_meal(self, user_constraints: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Generates a meal JSON based on user constraints, ensures it's valid.
        Raises ValueError if it can't produce valid JSON within max_retries.
        """
        for attempt in range(max_retries):
            # 1) Run the LLM chain with user constraints
            raw_output = self.chain.run(user_constraints=user_constraints)

            # 2) Attempt to parse as JSON
            try:
                json_data = json.loads(raw_output)
            except json.JSONDecodeError:
                continue  # Not valid JSON, try again

            # 3) Validate with JSONValidatorTool
            result = self.validator_tool.run(json_data)
            if "JSON is valid." in result:
                # We have valid JSON
                return json_data
            else:
                # Possibly re-prompt or just loop
                pass

        raise ValueError("Could not generate valid meal JSON within retries.")
