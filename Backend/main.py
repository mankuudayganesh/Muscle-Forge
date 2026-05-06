from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import uvicorn
import logging

# Local imports - ensure these files exist in your repo!
from database import get_db, engine
import models
from logic import PlanGenerator
from schemas import UserCreate

# Setup logging for production debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Muscle Forge API", version="2.0.0")

# ========== PRODUCTION CORS SETUP ==========
# This allows your Netlify frontend to talk to this Render backend
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://your-site-name.netlify.app", # REPLACE with your actual Netlify URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== API ENDPOINTS ==========

@app.get("/")
async def root():
    return {
        "message": "💪 Muscle Forge API is running!", 
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Simple query to verify DB connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.post("/api/generate-plan")
async def generate_plan(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"📊 Generating plan for: {user_data.name} (Budget: ₹{user_data.budget})")
        
        generator = PlanGenerator()
        plan = generator.generate_plan(user_data, db)
        
        # Save User Profile
        db_user = models.User(**user_data.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Save Weekly Plans
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
        
        # Add user_id to the response so the frontend can track the session
        plan["user_id"] = db_user.id
        plan["success"] = True
        return plan
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate plan.")

# ========== DATA FETCHING ENDPOINTS ==========

@app.get("/api/exercises")
async def get_exercises(difficulty: str = None, category: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Exercise)
    if difficulty: query = query.filter(models.Exercise.difficulty == difficulty)
    if category: query = query.filter(models.Exercise.category == category)
    return query.limit(50).all()

@app.get("/api/foods")
async def get_foods(category: str = None, is_veg: bool = None, db: Session = Depends(get_db)):
    query = db.query(models.Food)
    if category: query = query.filter(models.Food.category == category)
    if is_veg is not None: query = query.filter(models.Food.is_veg == is_veg)
    return query.limit(50).all()

if __name__ == "__main__":
    # Get port from environment variable for Render compatibility
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
