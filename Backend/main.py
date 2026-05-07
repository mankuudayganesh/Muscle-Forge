from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
import uvicorn
import logging

# Import your modules
from database import get_db, engine
import models
from logic import PlanGenerator
from schemas import UserCreate

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables (MUST be after importing models)
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Muscle Forge API", version="2.0.0")

# CORS middleware - Allow all origins for Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5500",
        "https://muscleforgee.netlify.app",
        "https://*.netlify.app",
        "https://mankuudayganesh.github.io",
        "https://*.github.io",
        "https://muscle-forgee.onrender.com",
        "*"  # Allow all during development (can restrict later)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== DATABASE INITIALIZATION ON STARTUP ==========
@app.on_event("startup")
def init_database():
    """Seed database on first startup if empty"""
    db = SessionLocal()
    try:
        from seed import seed_exercises, seed_foods
        
        # Check if exercises exist
        exercise_count = db.query(models.Exercise).count()
        if exercise_count == 0:
            logger.info("🌱 Database empty - seeding exercises and foods...")
            seed_exercises()
            seed_foods()
            logger.info("✅ Database seeded successfully!")
        else:
            logger.info(f"✅ Database already has {exercise_count} exercises and {db.query(models.Food).count()} foods")
    except Exception as e:
        logger.error(f"⚠️ Seeding error: {e}")
    finally:
        db.close()

# Import SessionLocal for startup event
from database import SessionLocal

# ========== STATIC FILES MOUNTING ==========
# Try multiple possible paths for frontend assets
possible_paths = [
    os.path.join(os.path.dirname(__file__), "../frontend/assets"),
    os.path.join(os.path.dirname(__file__), "frontend/assets"),
    os.path.join(os.path.dirname(__file__), "../assets"),
    os.path.join(os.path.dirname(__file__), "assets"),
]

static_mounted = False
for assets_path in possible_paths:
    abs_path = os.path.abspath(assets_path)
    if os.path.exists(abs_path):
        app.mount("/assets", StaticFiles(directory=abs_path), name="assets")
        logger.info(f"✅ Static files mounted from: {abs_path}")
        static_mounted = True
        break

if not static_mounted:
    logger.warning("⚠️ Could not find frontend/assets folder! Images may not load.")

# ========== ROOT ENDPOINTS ==========

@app.get("/")
async def root():
    return {
        "message": "💪 Muscle Forge API is running!", 
        "status": "active", 
        "static_mounted": static_mounted,
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        exercise_count = db.query(models.Exercise).count()
        food_count = db.query(models.Food).count()
        return {
            "status": "healthy",
            "database": "connected",
            "exercises_available": exercise_count,
            "foods_available": food_count,
            "static_mounted": static_mounted
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# ========== PLAN GENERATION ENDPOINT ==========

@app.post("/api/generate-plan")
async def generate_plan(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"📊 Received user data: {user_data.dict()}")
        logger.info(f"💰 Budget received: ₹{user_data.budget}")
        
        generator = PlanGenerator()
        plan = generator.generate_plan(user_data, db)
        
        # Save user
        db_user = models.User(
            name=user_data.name,
            gender=user_data.gender,
            age=user_data.age,
            height=user_data.height,
            weight=user_data.weight,
            budget=user_data.budget,
            experience=user_data.experience,
            goal=user_data.goal,
            diet_preference=user_data.diet_preference,
            workout_location=user_data.workout_location,
            activity_level=user_data.activity_level
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Save plans
        for i, meal in enumerate(plan["daily_meals"][:7]):
            db_plan = models.Plan(
                user_id=db_user.id,
                day=i+1,
                breakfast=str(meal.get("breakfast", {}).get("name", "")),
                lunch=str(meal.get("lunch", {}).get("name", "")),
                dinner=str(meal.get("dinner", {}).get("name", "")),
                snacks=str(meal.get("snacks", {}).get("name", "")),
                workout=str(plan["daily_workout"][i]) if i < len(plan["daily_workout"]) else "",
                calories=meal.get("calories", 0),
                protein=meal.get("protein", 0)
            )
            db.add(db_plan)
        
        db.commit()
        
        response_data = {
            "success": True,
            "user_id": db_user.id,
            "name": user_data.name,
            "gender": user_data.gender,
            "weekly_budget": user_data.budget,
            "daily_budget": round(user_data.budget / 7, 2),
            "bmi": plan["bmi"],
            "bmr": plan["bmr"],
            "target_calories": plan["target_calories"],
            "target_protein": plan["target_protein"],
            "target_carbs": plan["target_carbs"],
            "target_fat": plan["target_fat"],
            "daily_meals": plan["daily_meals"],
            "daily_workout": plan["daily_workout"],
            "tips": plan["tips"],
            "grocery_list": plan["grocery_list"],
            "weekly_cost": plan["weekly_cost"],
            "diet_preference": user_data.diet_preference
        }
        
        logger.info(f"✅ Plan generated successfully for ₹{user_data.budget} budget")
        return response_data
    
    except Exception as e:
        logger.error(f"❌ Error generating plan: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ========== EXERCISES ENDPOINT ==========

@app.get("/api/exercises")
async def get_exercises(difficulty: str = None, category: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Exercise)
    if difficulty:
        query = query.filter(models.Exercise.difficulty == difficulty)
    if category:
        query = query.filter(models.Exercise.category == category)
    
    exercises = query.limit(50).all()
    return [
        {
            "id": e.id,
            "name": e.name,
            "category": e.category,
            "difficulty": e.difficulty,
            "instructions": e.instructions,
            "image_url": e.image_url or "/assets/images/exercises/default.jpg",
            "sets": e.sets_1,
            "reps": e.reps_1,
            "weight": e.weight_1
        }
        for e in exercises
    ]

# ========== FOODS ENDPOINT ==========

@app.get("/api/foods")
async def get_foods(category: str = None, is_veg: bool = None, db: Session = Depends(get_db)):
    query = db.query(models.Food)
    if category:
        query = query.filter(models.Food.category == category)
    if is_veg is not None:
        query = query.filter(models.Food.is_veg == is_veg)
    
    foods = query.limit(50).all()
    return [
        {
            "id": f.id,
            "name": f.name,
            "hindi_name": f.hindi_name or "",
            "protein": f.protein or 0,
            "calories": f.calories or 0,
            "carbs": f.carbs or 0,
            "fat": f.fat or 0,
            "price": f.price or 0,
            "price_unit": f.price_unit or "kg",
            "serving_size": f.serving_size or "100g",
            "is_veg": f.is_veg,
            "category": f.category or "General",
            "image_url": f.image_url or "/assets/images/foods/default.jpg"
        }
        for f in foods
    ]

# ========== TEST STATIC FILE ENDPOINT ==========
@app.get("/test-image/{path:path}")
async def test_image(path: str):
    """Debug endpoint to check if image exists"""
    from fastapi.responses import JSONResponse
    import os
    
    full_path = os.path.join(os.path.dirname(__file__), "../frontend/assets/images", path)
    if os.path.exists(full_path):
        return JSONResponse(content={"exists": True, "path": full_path})
    else:
        return JSONResponse(content={"exists": False, "path": full_path}, status_code=404)

# ========== RUN SERVER ==========
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
