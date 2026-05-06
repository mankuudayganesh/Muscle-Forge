from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    gender: str
    age: int
    height: float
    weight: float
    budget: float
    experience: str
    goal: str
    diet_preference: str
    workout_location: str
    activity_level: str = "moderate"

class PlanResponse(BaseModel):
    user_id: int
    name: str
    gender: str
    bmi: float
    bmr: int
    target_calories: int
    target_protein: int
    target_carbs: int
    target_fat: int
    daily_meals: List[dict]
    daily_workout: List[dict]
    tips: List[dict]
    grocery_list: List[dict]
    weekly_cost: float