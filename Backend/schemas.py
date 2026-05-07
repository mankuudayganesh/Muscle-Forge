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

class UserResponse(BaseModel):
    id: int
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
    activity_level: str
    created_at: str

class ExerciseResponse(BaseModel):
    id: int
    name: str
    category: str
    target_muscle: Optional[str] = None
    difficulty: str
    sets: int
    reps: str
    weight: str
    instructions: str
    image_url: str

class FoodResponse(BaseModel):
    id: int
    name: str
    hindi_name: Optional[str] = None
    protein: float
    calories: float
    carbs: float
    fat: float
    price: float
    price_unit: str
    serving_size: str
    is_veg: bool
    category: str
    image_url: str
