# Add this import at the top with other imports
from database import SessionLocal

# Add this AFTER creating tables (around line 20)
models.Base.metadata.create_all(bind=engine)

# Add this startup event
@app.on_event("startup")
def init_database():
    db = SessionLocal()
    try:
        from seed import seed_exercises, seed_foods
        
        exercise_count = db.query(models.Exercise).count()
        if exercise_count == 0:
            print("🌱 Seeding database...")
            seed_exercises()
            seed_foods()
            print("✅ Database seeded!")
        else:
            print(f"✅ Database already has {exercise_count} exercises")
    except Exception as e:
        print(f"⚠️ Seeding check failed: {e}")
    finally:
        db.close()

# Rest of your code...
