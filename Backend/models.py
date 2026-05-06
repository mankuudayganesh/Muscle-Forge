from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    budget = Column(Float, nullable=False)
    experience = Column(String(20), nullable=False)
    goal = Column(String(20), nullable=False)
    diet_preference = Column(String(20), nullable=False)
    workout_location = Column(String(20), nullable=False)
    activity_level = Column(String(20), default="moderate")
    created_at = Column(DateTime, default=datetime.now)

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    target_muscle = Column(String(50))
    difficulty = Column(String(20), nullable=False)
    sets_1 = Column(Integer, default=3)
    reps_1 = Column(String(20), default="10-12")
    weight_1 = Column(String(20), default="Bodyweight")
    sets_2 = Column(Integer, default=4)
    reps_2 = Column(String(20), default="8-10")
    weight_2 = Column(String(20), default="Moderate")
    sets_3 = Column(Integer, default=5)
    reps_3 = Column(String(20), default="6-8")
    weight_3 = Column(String(20), default="Heavy")
    equipment_cost = Column(Integer, default=0)
    equipment = Column(String(100), default="Basic")
    instructions = Column(Text, default="Maintain proper form throughout the exercise.")
    image_url = Column(String(255), nullable=True, default="/assets/images/exercises/default.jpg")

class Food(Base):
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hindi_name = Column(String(100), nullable=True)
    price = Column(Float, nullable=False, default=50)
    price_unit = Column(String(20), default="kg")
    protein = Column(Float, default=0)
    calories = Column(Float, default=0)
    carbs = Column(Float, default=0)
    fat = Column(Float, default=0)
    serving_size = Column(String(50), default="100g")
    is_veg = Column(Boolean, default=True)
    price_per_100g = Column(Float, default=0)
    category = Column(String(50), default="General")
    image_url = Column(String(255), nullable=True, default="/assets/images/foods/default.jpg")

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    day = Column(Integer)
    breakfast = Column(Text, default="")
    lunch = Column(Text, default="")
    dinner = Column(Text, default="")
    snacks = Column(Text, default="")
    workout = Column(Text, default="")
    calories = Column(Integer, default=0)
    protein = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)