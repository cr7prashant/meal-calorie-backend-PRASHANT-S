from pydantic import BaseModel, Field
from typing import Optional

class CaloriesRequest(BaseModel):
    dish_name: str = Field(..., min_length=1, example="chicken biryani")
    servings: int = Field(..., gt=0, example=2)

class CaloriesResponse(BaseModel):
    dish_name: str
    servings: int
    calories_per_serving: float
    total_calories: float
    source: str = "USDA FoodData Central"

    class Config:
        from_attributes = True