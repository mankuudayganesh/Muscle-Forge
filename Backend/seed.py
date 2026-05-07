from database import SessionLocal, engine
import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DON'T drop tables - just create if not exist
models.Base.metadata.create_all(bind=engine)

def seed_exercises():
    db = SessionLocal()
    
    # Check if already seeded
    existing = db.query(models.Exercise).count()
    if existing > 0:
        logger.info(f"Exercises already exist ({existing}), skipping seed")
        db.close()
        return
    
    exercises = [
        # CHEST
        ("Barbell Bench Press", "Chest", "Chest", "Intermediate", 3, "10-12", "40kg", 4, "8-10", "60kg", 5, "6-8", "80kg", 300, "Barbell", "Lie flat on bench, grip bar shoulder-width, lower to chest, press up.", "/assets/images/exercises/chest/Barbell-Bench-Press.gif"),
        ("Incline Dumbbell Press", "Chest", "Upper Chest", "Intermediate", 3, "10-12", "15kg each", 4, "8-10", "22kg", 5, "6-8", "30kg", 280, "Dumbbells", "Set bench to 30-45°, press dumbbells up from chest.", "/assets/images/exercises/chest/incline dumbbell press.gif"),
        ("Decline Bench Press", "Chest", "Lower Chest", "Intermediate", 3, "10-12", "35kg", 4, "8-10", "55kg", 5, "6-8", "75kg", 290, "Barbell", "Angle targets lower pectoral fibres.", "/assets/images/exercises/chest/declined bench press.gif"),
        ("Dumbbell Flyes", "Chest", "Chest", "Beginner", 3, "12-15", "10kg each", 4, "10-12", "15kg", 5, "8-10", "20kg", 220, "Dumbbells", "Arms slightly bent, open wide, squeeze at top.", "/assets/images/exercises/chest/dumbell flyes.gif"),
        ("Push Ups", "Chest", "Chest", "Beginner", 3, "15-20", "Bodyweight", 4, "20-25", "Bodyweight", 5, "25-40", "Weighted", 150, "Bodyweight", "Keep core tight, chest to floor each rep.", "/assets/images/exercises/chest/pushups.gif"),
        
        # BACK
        ("Deadlift", "Back", "Lower Back", "Advanced", 3, "8-10", "50kg", 4, "6-8", "90kg", 5, "4-6", "140kg", 450, "Barbell", "Hinge at hips, flat back, drive through heels.", "/assets/images/exercises/back/deadlift.webp"),
        ("Pull Ups", "Back", "Lats", "Intermediate", 3, "5-8", "Bodyweight", 4, "8-12", "Bodyweight", 5, "12-20", "Weighted", 250, "Pull-Up Bar", "Dead hang, pull elbows to hips, chin above bar.", "/assets/images/exercises/back/pull-ups.gif"),
        ("Lat Pulldown", "Back", "Lats", "Beginner", 3, "12-15", "25kg", 4, "10-12", "45kg", 5, "8-10", "65kg", 230, "Lat Pulldown", "Pull bar to upper chest, full stretch at top.", "/assets/images/exercises/back/Lat-Pulldown.gif"),
        ("Seated Cable Row", "Back", "Mid Back", "Beginner", 3, "12-15", "20kg", 4, "10-12", "40kg", 5, "8-10", "60kg", 220, "Cable Row", "Sit tall, pull to navel, squeeze shoulder blades.", "/assets/images/exercises/back/seated cable row.gif"),
        
        # LEGS
        ("Barbell Squat", "Legs", "Legs", "Intermediate", 3, "12-15", "40kg", 4, "8-10", "70kg", 5, "6-8", "110kg", 400, "Barbell", "Squat to parallel, drive knees out.", "/assets/images/exercises/legs/squats.jpg"),
        ("Leg Press", "Legs", "Legs", "Beginner", 3, "12-15", "80kg", 4, "10-12", "140kg", 5, "8-10", "220kg", 350, "Leg Press", "Lower until 90° knee angle, press through heels.", "/assets/images/exercises/legs/leg press.jpg"),
        ("Walking Lunges", "Legs", "Legs", "Beginner", 3, "12 each", "Bodyweight", 4, "15 each", "10kg", 5, "20 each", "20kg", 250, "Dumbbells", "Step forward, lower back knee to floor.", "/assets/images/exercises/legs/lunges.gif"),
        
        # SHOULDERS
        ("Dumbbell Shoulder Press", "Shoulders", "Shoulders", "Beginner", 3, "10-12", "12kg", 4, "8-10", "20kg", 5, "6-8", "30kg", 250, "Dumbbells", "Press dumbbells overhead, lower to ear height.", "/assets/images/exercises/shoulders/Dumbbell-Shoulder-Press.gif"),
        ("Lateral Raise", "Shoulders", "Side Delts", "Beginner", 3, "12-15", "5kg", 4, "10-12", "8kg", 5, "8-10", "12kg", 170, "Dumbbells", "Raise to shoulder height, pinkies slightly up.", "/assets/images/exercises/shoulders/Lateral-Raise.gif"),
        
        # BICEPS
        ("Barbell Curl", "Biceps", "Biceps", "Beginner", 3, "12-15", "15kg", 4, "10-12", "25kg", 5, "8-10", "40kg", 180, "Barbell", "Elbows pinned, curl to chin, squeeze at top.", "/assets/images/exercises/biceps/Barbell-Curl.gif"),
        ("Dumbbell Curl", "Biceps", "Biceps", "Beginner", 3, "12-15", "8kg", 4, "10-12", "14kg", 5, "8-10", "20kg", 170, "Dumbbells", "Supinate wrist as you curl.", "/assets/images/exercises/biceps/Dumbbell-Curl.gif"),
        ("Hammer Curl", "Biceps", "Biceps", "Beginner", 3, "12-15", "8kg", 4, "10-12", "14kg", 5, "8-10", "22kg", 175, "Dumbbells", "Neutral grip throughout.", "/assets/images/exercises/biceps/Hammer-Curl.gif"),
        
        # TRICEPS
        ("Tricep Pushdown", "Triceps", "Triceps", "Beginner", 3, "12-15", "15kg", 4, "10-12", "25kg", 5, "8-10", "40kg", 170, "Cable", "Elbows pinned, push bar down to lockout.", "/assets/images/exercises/triceps/Pushdown.gif"),
        ("Tricep Dips", "Triceps", "Triceps", "Intermediate", 3, "8-10", "Bodyweight", 4, "10-15", "Bodyweight", 5, "15-20", "Weighted", 240, "Dip Bars", "Stay upright to target triceps.", "/assets/images/exercises/triceps/tricep dips.gif"),
        
        # CORE
        ("Crunches", "Core", "Abs", "Beginner", 3, "20-25", "Bodyweight", 4, "25-30", "Bodyweight", 5, "30-40", "Weighted", 120, "Bodyweight", "Curl upper back off floor.", "/assets/images/exercises/core/crunches.jpg"),
        ("Leg Raises", "Core", "Abs", "Intermediate", 3, "12-15", "Bodyweight", 4, "15-20", "Bodyweight", 5, "20-25", "Weighted", 150, "Bench", "Raise legs to 90°, lower slowly.", "/assets/images/exercises/core/LEG_RAISE.gif"),
        
        # CARDIO
        ("Treadmill Running", "Cardio", "Cardio", "Beginner", 3, "10 min", "Bodyweight", 4, "20 min", "Bodyweight", 5, "30 min", "Speed", 300, "Treadmill", "Start at comfortable pace.", "/assets/images/exercises/cardio/TREADMIl.gif"),
        ("Jump Rope", "Cardio", "Cardio", "Beginner", 3, "2 min", "Bodyweight", 4, "5 min", "Bodyweight", 5, "10 min", "Weighted", 250, "Jump Rope", "Land softly on balls of feet.", "/assets/images/exercises/cardio/jump rope.jpg"),
        ("Cycling", "Cardio", "Cardio", "Intermediate", 3, "15 min", "Bodyweight", 4, "25 min", "Bodyweight", 5, "35 min", "Resistance", 200, "Bike", "Keep steady pace, maintain good posture.", "/assets/images/exercises/cardio/cycling.jpg"),
    ]
    
    inserted = 0
    for ex in exercises:
        try:
            db_exercise = models.Exercise(
                name=ex[0], category=ex[1], target_muscle=ex[2], difficulty=ex[3],
                sets_1=ex[4], reps_1=ex[5], weight_1=ex[6],
                sets_2=ex[7], reps_2=ex[8], weight_2=ex[9],
                sets_3=ex[10], reps_3=ex[11], weight_3=ex[12],
                equipment_cost=ex[13], equipment=ex[14], instructions=ex[15],
                image_url=ex[16]
            )
            db.add(db_exercise)
            inserted += 1
        except Exception as e:
            logger.error(f"Failed to insert exercise {ex[0]}: {e}")
    
    db.commit()
    logger.info(f"✅ Seeded {inserted} exercises")
    db.close()

def seed_foods():
    db = SessionLocal()
    
    # Check if already seeded
    existing = db.query(models.Food).count()
    if existing > 0:
        logger.info(f"Foods already exist ({existing}), skipping seed")
        db.close()
        return
    
    foods = [
        # FRUITS
        ("Apple", "Seb", 140, "kg", 0.5, 95, 25, 0.3, "1 medium", True, 14, "fruits", "/assets/images/foods/fruits/apple.jpg"),
        ("Banana", "Kela", 40, "kg", 1.1, 105, 27, 0.4, "1 medium", True, 4, "fruits", "/assets/images/foods/fruits/Banana (3).jpg"),
        ("Orange", "Santra", 80, "kg", 1.2, 62, 15, 0.2, "1 medium", True, 8, "fruits", "/assets/images/foods/fruits/orange.jpg"),
        ("Mango", "Aam", 100, "kg", 0.8, 60, 15, 0.4, "100g", True, 10, "fruits", "/assets/images/foods/fruits/mango.jpg"),
        ("Pomegranate", "Anar", 120, "kg", 1.7, 83, 19, 1.2, "100g", True, 12, "fruits", "/assets/images/foods/fruits/pomogranite.jpg"),
        ("Watermelon", "Tarbuj", 25, "kg", 0.6, 30, 8, 0.2, "100g", True, 2.5, "fruits", "/assets/images/foods/fruits/watermelon.jpg"),
        ("Papaya", "Papita", 35, "kg", 0.5, 43, 11, 0.3, "100g", True, 3.5, "fruits", "/assets/images/foods/fruits/papaya.jpg"),
        ("Grapes", "Angoor", 100, "kg", 0.7, 69, 18, 0.2, "100g", True, 10, "fruits", "/assets/images/foods/fruits/grapes.jpg"),
        
        # DRY FRUITS
        ("Almonds", "Badam", 1100, "kg", 21, 579, 22, 49, "30g", True, 110, "dry_fruits", "/assets/images/foods/dry_fruits/almonds.jpg"),
        ("Cashews", "Kaju", 1000, "kg", 18, 553, 30, 44, "30g", True, 100, "dry_fruits", "/assets/images/foods/dry_fruits/cashews.jpg"),
        ("Walnuts", "Akhrot", 1200, "kg", 15, 654, 14, 65, "30g", True, 120, "dry_fruits", "/assets/images/foods/dry_fruits/walnuts.jpg"),
        ("Peanuts", "Moongphali", 100, "kg", 26, 567, 16, 49, "30g", True, 10, "dry_fruits", "/assets/images/foods/dry_fruits/peanuts.jpg"),
        
        # DAIRY
        ("Paneer", "Paneer", 350, "kg", 18, 265, 6, 21, "100g", True, 35, "dairy", "/assets/images/foods/dairy/paneer.jpg"),
        ("Milk", "Doodh", 60, "liter", 8, 150, 12, 8, "250ml", True, 6, "dairy", "/assets/images/foods/dairy/full fatty milk.jpg"),
        ("Whey Protein", "Whey Protein", 2500, "kg", 75, 380, 5, 6, "30g scoop", True, 250, "dairy", "/assets/images/foods/dairy/whey-protein.jpg"),
        ("Oats", "Oats", 80, "kg", 12, 350, 60, 5, "40g", True, 8, "breakfast", "/assets/images/foods/dairy/oats.jpg"),
        ("Peanut Butter", "Peanut Butter", 250, "500g", 25, 590, 20, 50, "20g", True, 25, "dry_fruits", "/assets/images/foods/dairy/peanut-butter.jpg"),
        
        # VEGETABLES
        ("Broccoli", "Broccoli", 70, "kg", 2.8, 34, 7, 0.4, "100g", True, 7, "vegetables", "/assets/images/foods/vegetables/Broccoli.jpg"),
        ("Spinach", "Palak", 15, "kg", 2.9, 23, 3.6, 0.4, "100g", True, 1.5, "vegetables", "/assets/images/foods/vegetables/Spinach.jpg"),
        ("Carrot", "Gajar", 45, "kg", 0.9, 41, 10, 0.2, "100g", True, 4.5, "vegetables", "/assets/images/foods/vegetables/Carrot.jpg"),
        ("Cauliflower", "Gobhi", 40, "kg", 1.9, 25, 5, 0.3, "100g", True, 4, "vegetables", "/assets/images/foods/vegetables/Cauliflower.jpg"),
        ("Tomato", "Tamatar", 40, "kg", 0.9, 18, 3.9, 0.2, "100g", True, 4, "vegetables", "/assets/images/foods/vegetables/Tomato.jpg"),
        ("Onion", "Pyaz", 35, "kg", 1.1, 40, 9, 0.1, "100g", True, 3.5, "vegetables", "/assets/images/foods/vegetables/Onion.jpg"),
        ("Potato", "Aloo", 35, "kg", 2, 77, 17, 0.1, "100g", True, 3.5, "vegetables", "/assets/images/foods/vegetables/Potato.jpg"),
        ("Sweet Potato", "Sweet Potato", 50, "kg", 1.6, 86, 20, 0.1, "100g", True, 5, "vegetables", "/assets/images/foods/vegetables/Sweet Potato.jpg"),
        ("Mushroom", "Khumb", 100, "kg", 3.1, 22, 3.3, 0.3, "100g", True, 10, "vegetables", "/assets/images/foods/vegetables/Mushroom.jpg"),
        ("Soya Chunks", "Soya Badi", 150, "kg", 52, 345, 33, 0.5, "100g", True, 15, "vegetables", "/assets/images/foods/vegetables/Soya Chunks.jpg"),
        
        # NON-VEG
        ("Chicken Breast", "Chicken Breast", 290, "kg", 31, 165, 0, 3.6, "100g", False, 29, "non_veg", "/assets/images/foods/non_veg/chicken breast.jpg"),
        ("Chicken Leg", "Chicken Leg", 260, "kg", 26, 184, 0, 8, "100g", False, 26, "non_veg", "/assets/images/foods/non_veg/chicken leg.jpg"),
        ("Eggs", "Anda", 5, "piece", 6, 78, 0.6, 5, "1 egg", False, 5, "non_veg", "/assets/images/foods/non_veg/Whole Egg.jpg"),
        ("Fish", "Machli", 300, "kg", 19, 162, 0, 9, "100g", False, 30, "non_veg", "/assets/images/foods/non_veg/Tuna Fish.jpg"),
        ("Mutton (Goat Meat)", "Bakra Gosht", 550, "kg", 25, 240, 0, 15, "100g", False, 55, "non_veg", "/assets/images/foods/non_veg/mutton.jpg"),
        ("Prawns", "Jhinga", 450, "kg", 24, 105, 0, 1.5, "100g", False, 45, "non_veg", "/assets/images/foods/non_veg/prawns.jpg"),
        ("Crab", "Kekda", 500, "kg", 19, 120, 0, 2, "100g", False, 50, "non_veg", "/assets/images/foods/non_veg/crab.jpg"),
        ("Lobster", "Lobster", 1200, "kg", 22, 130, 0, 1.5, "100g", False, 120, "non_veg", "/assets/images/foods/non_veg/lobster.jpg"),
    ]
    
    inserted = 0
    for food in foods:
        try:
            db_food = models.Food(
                name=food[0], hindi_name=food[1], price=food[2], price_unit=food[3],
                protein=food[4], calories=food[5], carbs=food[6], fat=food[7],
                serving_size=food[8], is_veg=food[9], price_per_100g=food[10],
                category=food[11], image_url=food[12]
            )
            db.add(db_food)
            inserted += 1
        except Exception as e:
            logger.error(f"Failed to insert food {food[0]}: {e}")
    
    db.commit()
    logger.info(f"✅ Seeded {inserted} foods")
    db.close()

if __name__ == "__main__":
    logger.info("🌱 Seeding database...")
    seed_exercises()
    seed_foods()
    logger.info("✨ Seeding complete!")
