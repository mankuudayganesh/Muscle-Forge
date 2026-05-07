import random
import math
from typing import Dict, List, Any
from sqlalchemy.orm import Session
import models

class PlanGenerator:
    def generate_plan(self, user_data, db: Session) -> Dict[str, Any]:
        # Extract user data
        gender = user_data.gender
        age = user_data.age
        height = user_data.height
        weight = user_data.weight
        goal = user_data.goal
        diet_pref = user_data.diet_preference
        experience = user_data.experience
        weekly_budget = user_data.budget
        
        daily_budget = weekly_budget / 7 if weekly_budget else 500
        
        print(f"💰 Weekly Budget: ₹{weekly_budget}")
        print(f"💰 Daily Budget: ₹{daily_budget}")
        print(f"🥗 Diet Preference: {diet_pref}")
        print(f"⚖️ Weight: {weight}kg, Height: {height}cm, Age: {age}")
        
        # Calculate BMI
        bmi = weight / ((height/100) ** 2)
        
        # Calculate BMR
        if gender == "male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (4.799 * height) - (4.330 * age)
        
        tdee = bmr * 1.55
        
        # Calculate target calories based on goal
        if goal == "muscle_gain":
            target_calories = int(tdee + 300)
            protein_per_kg = 2.0
        elif goal == "fat_loss":
            target_calories = int(tdee - 450)
            protein_per_kg = 1.8
        elif goal == "lean_body":
            target_calories = int(tdee + 100)
            protein_per_kg = 1.9
        else:
            target_calories = int(tdee)
            protein_per_kg = 1.6
        
        target_protein = int(weight * protein_per_kg)
        target_fat = int((target_calories * 0.25) / 9)
        target_carbs = int((target_calories - (target_protein * 4) - (target_fat * 9)) / 4)
        
        print(f"🎯 Target Calories: {target_calories}")
        print(f"🥩 Target Protein: {target_protein}g")
        
        # Get exercises from database
        exercises = db.query(models.Exercise).all()
        print(f"📋 Total exercises found: {len(exercises)}")
        
        # Group exercises by category
        exercise_map = {}
        for ex in exercises:
            cat = ex.category if ex.category else "General"
            if cat not in exercise_map:
                exercise_map[cat] = []
            exercise_map[cat].append(ex)
        
        # Get ALL foods from database
        all_foods = db.query(models.Food).all()
        print(f"🍽️ Total foods in DB: {len(all_foods)}")
        
        # IMPORTANT: Whey Protein and Peanut Butter - mandatory items
        whey_protein = [f for f in all_foods if "Whey" in f.name or "whey" in f.name.lower()]
        peanut_butter = [f for f in all_foods if "Peanut Butter" in f.name or "peanut" in f.name.lower()]
        
        # SEPARATE FOODS BASED ON DIET PREFERENCE
        fruits = [f for f in all_foods if f.category == "fruits"]
        dry_fruits = [f for f in all_foods if f.category == "dry_fruits"]
        
        if diet_pref == "veg":
            vegetables = [f for f in all_foods if f.category == "vegetables"]
            dairy = [f for f in all_foods if f.category == "dairy"]
            non_veg = []
            print(f"🍎 VEG Foods - Fruits: {len(fruits)}, Dry Fruits: {len(dry_fruits)}, Vegetables: {len(vegetables)}, Dairy: {len(dairy)}")
            all_allowed_foods = vegetables + dairy + fruits + dry_fruits
        else:
            non_veg = [f for f in all_foods if f.category == "non_veg"]
            dairy = [f for f in all_foods if f.category == "dairy"]
            vegetables = []
            print(f"🍖 NON-VEG Foods - Fruits: {len(fruits)}, Dry Fruits: {len(dry_fruits)}, Non-Veg: {len(non_veg)}, Dairy: {len(dairy)}")
            all_allowed_foods = non_veg + dairy + fruits + dry_fruits
        
        # Generate daily meals with proper rotation
        daily_meals = self._generate_meals_with_proper_rotation(
            all_allowed_foods, fruits, dry_fruits, vegetables, dairy, non_veg,
            daily_budget, target_calories, target_protein, diet_pref
        )
        
        # Generate workout plan
        daily_workout = self._generate_workout_schedule(exercise_map, experience, gender)
        
        # Generate grocery list with mandatory items
        grocery_list = self._generate_grocery_from_db(
            all_allowed_foods, fruits, dry_fruits, vegetables, dairy, non_veg,
            whey_protein, peanut_butter, weekly_budget, diet_pref
        )
        
        # Generate tips with budget-friendly advice
        tips = [
            {"icon": "💧", "title": "Hydration", "desc": "Drink 3-4 liters of water daily"},
            {"icon": "😴", "title": "Sleep", "desc": "Get 7-8 hours of quality sleep"},
            {"icon": "📊", "title": "Track Progress", "desc": "Take weekly measurements & photos"},
            {"icon": "🧘", "title": "Recovery", "desc": "Take 1-2 rest days per week"},
            {"icon": "🥩", "title": "Protein Goal", "desc": f"Your daily protein target is {target_protein}g. That's about {round(target_protein/30)}g per meal!"},
            {"icon": "💰", "title": "Budget Tip", "desc": f"Daily budget: ₹{round(daily_budget,2)}. Buy staples in bulk!"},
            {"icon": "🥤", "title": "Supplement", "desc": "Consider Whey Protein for quick protein intake (within budget)"},
            {"icon": "🥜", "title": "Healthy Fats", "desc": "Peanut butter is great for healthy fats and protein"},
            {"icon": "🔄", "title": "Daily Rotation", "desc": "We rotate your foods daily for variety and balanced nutrition!"},
            {"icon": "📱", "title": "Track Your Meals", "desc": "Use apps to log food and track macros"},
            {"icon": "🍳", "title": "Meal Prep", "desc": "Cook in batches to save time and money"},
        ]
        
        weekly_cost = sum(item.get("cost", 0) for item in grocery_list)
        
        # Ensure grocery list doesn't exceed budget
        if weekly_cost > weekly_budget and weekly_budget > 0:
            factor = weekly_budget / weekly_cost
            for item in grocery_list:
                item["cost"] = round(item["cost"] * factor, 2)
            weekly_cost = weekly_budget
        
        return {
            "success": True,
            "name": user_data.name,
            "gender": gender,
            "diet_preference": diet_pref,
            "bmi": round(bmi, 1),
            "bmr": int(bmr),
            "tdee": int(tdee),
            "target_calories": target_calories,
            "target_protein": target_protein,
            "target_carbs": target_carbs,
            "target_fat": target_fat,
            "daily_budget": round(daily_budget, 2),
            "weekly_budget": weekly_budget,
            "daily_meals": daily_meals,
            "daily_workout": daily_workout,
            "tips": tips,
            "grocery_list": grocery_list,
            "weekly_cost": round(weekly_cost, 2)
        }
    
    def _generate_meals_with_proper_rotation(self, all_foods, fruits, dry_fruits, vegetables, dairy, non_veg,
                                               daily_budget, target_calories, target_protein, diet_pref):
        """Generate meal plans with proper daily rotation:
           NON-VEG: 1 Non-Veg + 1 Dairy + 1 Fruit + 1 Dry Fruit per day
           VEG: 1 Vegetable + 1 Dairy + 1 Fruit + 1 Dry Fruit per day"""
        
        daily_meals = []
        
        # Create rotated lists (each day gets different items)
        fruits_list = fruits.copy()
        dry_fruits_list = dry_fruits.copy()
        dairy_list = dairy.copy()
        
        # Shuffle for random distribution
        random.shuffle(fruits_list)
        random.shuffle(dry_fruits_list)
        random.shuffle(dairy_list)
        
        if diet_pref == "veg":
            veg_list = vegetables.copy()
            random.shuffle(veg_list)
            # Ensure fallback if list is empty
            if not veg_list and all_foods:
                veg_list = [f for f in all_foods if f.category in ["vegetables", "fruits"]]
        else:
            non_veg_list = non_veg.copy()
            # Sort by protein content (highest first)
            non_veg_list.sort(key=lambda x: x.protein or 0, reverse=True)
            random.shuffle(non_veg_list)
            # Ensure fallback if list is empty
            if not non_veg_list and all_foods:
                non_veg_list = [f for f in all_foods if f.category in ["non_veg", "dairy"]]
        
        # Define meal types with proper calorie distribution
        meal_types = [
            {"key": "breakfast", "name": "Breakfast", "time": "7:00 AM", "icon": "🌅", "calorie_percent": 0.25, "protein_percent": 0.25},
            {"key": "lunch", "name": "Lunch", "time": "1:00 PM", "icon": "☀️", "calorie_percent": 0.35, "protein_percent": 0.35},
            {"key": "dinner", "name": "Dinner", "time": "8:00 PM", "icon": "🌙", "calorie_percent": 0.30, "protein_percent": 0.30},
            {"key": "snacks", "name": "Snacks", "time": "4:30 PM", "icon": "🍌", "calorie_percent": 0.10, "protein_percent": 0.10}
        ]
        
        for day in range(7):
            day_meal = {
                "day": day + 1,
                "daily_budget": round(daily_budget, 2),
                "calories": target_calories,
                "protein": target_protein
            }
            
            remaining_budget = daily_budget
            
            # Get items for this day (different from other days) with fallbacks
            fruit_for_day = fruits_list[day % len(fruits_list)] if fruits_list else None
            dry_fruit_for_day = dry_fruits_list[day % len(dry_fruits_list)] if dry_fruits_list else None
            dairy_for_day = dairy_list[day % len(dairy_list)] if dairy_list else None
            
            if diet_pref == "veg":
                veg_for_day = veg_list[day % len(veg_list)] if veg_list else None
                day_items = {
                    "veg": veg_for_day,
                    "dairy": dairy_for_day,
                    "fruit": fruit_for_day,
                    "dry_fruit": dry_fruit_for_day
                }
            else:
                non_veg_for_day = non_veg_list[day % len(non_veg_list)] if non_veg_list else None
                day_items = {
                    "non_veg": non_veg_for_day,
                    "dairy": dairy_for_day,
                    "fruit": fruit_for_day,
                    "dry_fruit": dry_fruit_for_day
                }
            
            # Print daily combo for debugging
            if diet_pref == "veg":
                print(f"📅 Day {day+1} Combo: 🥬 {veg_for_day.name if veg_for_day else 'None'} + 🥛 {dairy_for_day.name if dairy_for_day else 'None'} + 🍎 {fruit_for_day.name if fruit_for_day else 'None'} + 🥜 {dry_fruit_for_day.name if dry_fruit_for_day else 'None'}")
            else:
                print(f"📅 Day {day+1} Combo: 🍗 {non_veg_for_day.name if non_veg_for_day else 'None'} + 🥛 {dairy_for_day.name if dairy_for_day else 'None'} + 🍎 {fruit_for_day.name if fruit_for_day else 'None'} + 🥜 {dry_fruit_for_day.name if dry_fruit_for_day else 'None'}")
            
            # Distribute the 4 daily items across 4 meals
            if diet_pref == "veg":
                meal_items = [
                    {"meal": "breakfast", "item": dairy_for_day},
                    {"meal": "lunch", "item": fruit_for_day},
                    {"meal": "dinner", "item": veg_for_day},
                    {"meal": "snacks", "item": dry_fruit_for_day}
                ]
            else:
                meal_items = [
                    {"meal": "breakfast", "item": dairy_for_day},
                    {"meal": "lunch", "item": non_veg_for_day},
                    {"meal": "dinner", "item": fruit_for_day},
                    {"meal": "snacks", "item": dry_fruit_for_day}
                ]
            
            for meal in meal_types:
                selected_food = None
                
                # Find matching item for this meal
                for mi in meal_items:
                    if mi["meal"] == meal["key"] and mi["item"] is not None:
                        selected_food = mi["item"]
                        break
                
                # If no specific item, use any available from daily items
                if not selected_food:
                    for item_type, item in day_items.items():
                        if item is not None:
                            selected_food = item
                            break
                
                # Fallback if still no food - use any food from allowed list
                if not selected_food and all_foods:
                    if all_foods:
                        selected_food = random.choice(all_foods)
                
                if selected_food:
                    meal_calories = round(target_calories * meal["calorie_percent"])
                    meal_protein = round(target_protein * meal["protein_percent"])
                    
                    # Calculate cost (budget-friendly)
                    food_price = selected_food.price or 80
                    if selected_food.price_unit == "kg" and food_price > 10:
                        serving_cost = (food_price / 1000) * 150
                    elif selected_food.price_unit == "liter":
                        serving_cost = (food_price / 1000) * 250
                    else:
                        serving_cost = food_price
                    
                    # Ensure cost doesn't exceed budget
                    max_meal_cost = remaining_budget * meal["calorie_percent"]
                    meal_cost = min(serving_cost, max_meal_cost)
                    
                    image_url = selected_food.image_url or "/assets/images/foods/default.jpg"
                    image_url = image_url.replace(" ", "%20")
                    
                    day_meal[meal["key"]] = {
                        "name": selected_food.name,
                        "hindi_name": selected_food.hindi_name or "",
                        "calories": meal_calories,
                        "protein": meal_protein,
                        "price": round(meal_cost, 2),
                        "serving_size": selected_food.serving_size or "150g",
                        "image_url": image_url,
                        "meal_time": meal["time"],
                        "meal_icon": meal["icon"],
                        "meal_name": meal["name"]
                    }
                    
                    remaining_budget -= meal_cost
                else:
                    # Ultimate fallback
                    day_meal[meal["key"]] = {
                        "name": "Fresh Fruits" if meal["key"] != "lunch" else "Balanced Meal",
                        "hindi_name": "",
                        "calories": round(target_calories * meal["calorie_percent"]),
                        "protein": round(target_protein * meal["protein_percent"]),
                        "price": round(daily_budget * meal["calorie_percent"], 2),
                        "serving_size": "1 serving",
                        "image_url": "/assets/images/foods/default.jpg",
                        "meal_time": meal["time"],
                        "meal_icon": meal["icon"],
                        "meal_name": meal["name"]
                    }
            
            daily_meals.append(day_meal)
        
        return daily_meals
    
    def _generate_workout_schedule(self, exercise_map, experience, gender):
        """Generate 7-day workout schedule"""
        
        workout_schedule = [
            {"day": 1, "name": "Monday", "focus": "Chest Day 💪", "muscles": ["Chest"]},
            {"day": 2, "name": "Tuesday", "focus": "Back Day 🔥", "muscles": ["Back"]},
            {"day": 3, "name": "Wednesday", "focus": "Leg Day 🦵", "muscles": ["Legs"]},
            {"day": 4, "name": "Thursday", "focus": "Shoulder Day 🏋️", "muscles": ["Shoulders"]},
            {"day": 5, "name": "Friday", "focus": "Arms Day 💪", "muscles": ["Biceps", "Triceps"]},
            {"day": 6, "name": "Saturday", "focus": "Cardio & Core ❤️", "muscles": ["Cardio", "Core"]},
            {"day": 7, "name": "Sunday", "focus": "Rest Day 🧘", "muscles": []}
        ]
        
        daily_workout = []
        used_exercises = set()
        
        for schedule in workout_schedule:
            if schedule["focus"] == "Rest Day 🧘":
                daily_workout.append({
                    "day": schedule["day"],
                    "name": schedule["name"],
                    "focus": schedule["focus"],
                    "rest": True,
                    "message": "Rest and recovery day! Light stretching or walking recommended.",
                    "exercises": []
                })
                continue
            
            day_exercises = []
            for muscle in schedule["muscles"]:
                matching_exercises = []
                for cat, ex_list in exercise_map.items():
                    if muscle.lower() in cat.lower() or cat.lower() in muscle.lower():
                        for ex in ex_list:
                            if ex.name not in used_exercises:
                                matching_exercises.append(ex)
                
                if matching_exercises:
                    num_exercises = 3 if muscle in ["Biceps", "Triceps"] else 4
                    exercises_for_muscle = random.sample(matching_exercises, min(num_exercises, len(matching_exercises)))
                    for ex in exercises_for_muscle:
                        used_exercises.add(ex.name)
                        
                        if experience == "beginner":
                            sets = ex.sets_1 or 3
                            reps = ex.reps_1 or "10-12"
                            weight = ex.weight_1 or "Bodyweight"
                        elif experience == "intermediate":
                            sets = ex.sets_2 or ex.sets_1 or 4
                            reps = ex.reps_2 or ex.reps_1 or "8-12"
                            weight = ex.weight_2 or ex.weight_1 or "Moderate"
                        else:
                            sets = ex.sets_3 or ex.sets_2 or ex.sets_1 or 5
                            reps = ex.reps_3 or ex.reps_2 or ex.reps_1 or "6-10"
                            weight = ex.weight_3 or ex.weight_2 or ex.weight_1 or "Heavy"
                        
                        image_url = ex.image_url or "/assets/images/exercises/default.jpg"
                        image_url = image_url.replace(" ", "%20")
                        
                        day_exercises.append({
                            "name": ex.name,
                            "category": ex.category,
                            "sets": sets,
                            "reps": reps,
                            "weight": weight,
                            "instructions": ex.instructions or "Maintain proper form throughout",
                            "image_url": image_url
                        })
            
            if not day_exercises:
                day_exercises.append({
                    "name": f"{schedule['focus']} - Basic Routine",
                    "category": schedule["focus"],
                    "sets": 3,
                    "reps": "10-12",
                    "weight": "Bodyweight",
                    "instructions": "Focus on proper form. Do 3 sets of each exercise.",
                    "image_url": "/assets/images/exercises/default.jpg"
                })
            
            daily_workout.append({
                "day": schedule["day"],
                "name": schedule["name"],
                "focus": schedule["focus"],
                "rest": False,
                "exercises": day_exercises
            })
        
        return daily_workout
    
    def _generate_grocery_from_db(self, all_foods, fruits, dry_fruits, vegetables, dairy, non_veg,
                                    whey_protein, peanut_butter, weekly_budget, diet_pref):
        """Generate budget-friendly grocery list with essential items"""
        
        grocery_list = []
        used_items = set()
        remaining_budget = weekly_budget if weekly_budget else 2000
        
        print(f"🛒 Starting grocery budget: ₹{remaining_budget}")
        
        # ========== MANDATORY ITEMS (Try to include within budget) ==========
        mandatory_items = []
        
        # Add Whey Protein if available and budget allows
        if whey_protein and remaining_budget >= 300:
            wp = whey_protein[0]
            cost = min(wp.price or 2500, remaining_budget * 0.25)
            if cost <= remaining_budget:
                mandatory_items.append({
                    "item": wp.name,
                    "hindi_name": wp.hindi_name or "",
                    "quantity": "1 kg (approx 30 servings)",
                    "cost": round(cost, 2),
                    "image_url": wp.image_url or "/assets/images/foods/default.jpg"
                })
                remaining_budget -= cost
                used_items.add(wp.name)
                print(f"✅ Added mandatory: {wp.name} (₹{cost})")
        
        # Add Peanut Butter if available and budget allows
        if peanut_butter and remaining_budget >= 150:
            pb = peanut_butter[0]
            cost = min(pb.price or 250, remaining_budget * 0.15)
            if cost <= remaining_budget:
                mandatory_items.append({
                    "item": pb.name,
                    "hindi_name": pb.hindi_name or "",
                    "quantity": "500g",
                    "cost": round(cost, 2),
                    "image_url": pb.image_url or "/assets/images/foods/default.jpg"
                })
                remaining_budget -= cost
                used_items.add(pb.name)
                print(f"✅ Added mandatory: {pb.name} (₹{cost})")
        
        grocery_list.extend(mandatory_items)
        
        # ========== CREATE ROTATED GROCERY LISTS ==========
        # Get unique items from each day's rotation
        fruits_list = [f for f in fruits if f.name not in used_items]
        dry_fruits_list = [f for f in dry_fruits if f.name not in used_items]
        dairy_list = [f for f in dairy if f.name not in used_items]
        
        if diet_pref == "veg":
            veg_list = [f for f in vegetables if f.name not in used_items]
            # Select items based on daily rotation needs
            categories = [
                (veg_list, 7, "500g", "🥬 Vegetables"),
                (dairy_list, 7, "500g", "🥛 Dairy"),
                (fruits_list, 7, "500g", "🍎 Fruits"),
                (dry_fruits_list, 7, "250g", "🥜 Dry Fruits")
            ]
        else:
            non_veg_list = [f for f in non_veg if f.name not in used_items]
            # Sort non-veg by price (cheaper first) for budget
            non_veg_list.sort(key=lambda x: x.price or 100)
            categories = [
                (non_veg_list, 7, "1 kg", "🍗 Non-Veg"),
                (dairy_list, 7, "500g", "🥛 Dairy"),
                (fruits_list, 7, "500g", "🍎 Fruits"),
                (dry_fruits_list, 7, "250g", "🥜 Dry Fruits")
            ]
        
        for cat_foods, num_items, quantity, label in categories:
            available = [f for f in cat_foods if f.name not in used_items]
            if available:
                # Take enough items for all 7 days, but limit to available
                selected = available[:min(num_items, len(available))]
                for food in selected:
                    if remaining_budget <= 10:  # Stop if budget is almost exhausted
                        break
                    
                    used_items.add(food.name)
                    food_price = food.price or 80
                    cost = min(food_price, remaining_budget * 0.15)
                    
                    # Adjust quantity for expensive items
                    if "kg" in quantity and food_price > 500:
                        quantity = "500g"
                        cost = min(cost, remaining_budget * 0.1)
                    elif "kg" in quantity and food_price > 200:
                        quantity = "500g"
                    
                    image_url = food.image_url or "/assets/images/foods/default.jpg"
                    image_url = image_url.replace(" ", "%20")
                    
                    grocery_list.append({
                        "item": food.name,
                        "hindi_name": food.hindi_name or "",
                        "quantity": quantity,
                        "cost": round(cost, 2),
                        "image_url": image_url
                    })
                    remaining_budget -= cost
                    print(f"🛒 Added {label}: {food.name} (₹{cost})")
        
        # Scale costs if total exceeds budget
        total = sum(item["cost"] for item in grocery_list)
        if total > weekly_budget and weekly_budget > 0 and total > 0:
            factor = weekly_budget / total
            for item in grocery_list:
                item["cost"] = round(item["cost"] * factor, 2)
            print(f"💰 Scaled grocery list from ₹{total} to ₹{weekly_budget}")
        
        print(f"🛒 Final grocery list total: ₹{sum(item['cost'] for item in grocery_list)} (Budget: ₹{weekly_budget})")
        
        return grocery_list
