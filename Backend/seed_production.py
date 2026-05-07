import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def run_seed():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            age INTEGER NOT NULL,
            height FLOAT NOT NULL,
            weight FLOAT NOT NULL,
            budget FLOAT NOT NULL,
            experience VARCHAR(20) NOT NULL,
            goal VARCHAR(20) NOT NULL,
            diet_preference VARCHAR(20) NOT NULL,
            workout_location VARCHAR(20) NOT NULL,
            activity_level VARCHAR(20) DEFAULT 'moderate',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS exercises (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            target_muscle VARCHAR(50),
            difficulty VARCHAR(20) NOT NULL,
            sets_1 INTEGER DEFAULT 3,
            reps_1 VARCHAR(20) DEFAULT '10-12',
            weight_1 VARCHAR(20) DEFAULT 'Bodyweight',
            sets_2 INTEGER DEFAULT 4,
            reps_2 VARCHAR(20) DEFAULT '8-10',
            weight_2 VARCHAR(20) DEFAULT 'Moderate',
            sets_3 INTEGER DEFAULT 5,
            reps_3 VARCHAR(20) DEFAULT '6-8',
            weight_3 VARCHAR(20) DEFAULT 'Heavy',
            equipment_cost INTEGER DEFAULT 0,
            equipment VARCHAR(100) DEFAULT 'Basic',
            instructions TEXT DEFAULT 'Maintain proper form throughout.',
            image_url VARCHAR(255)
        );
        
        CREATE TABLE IF NOT EXISTS foods (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            hindi_name VARCHAR(100),
            price FLOAT NOT NULL DEFAULT 50,
            price_unit VARCHAR(20) DEFAULT 'kg',
            protein FLOAT DEFAULT 0,
            calories FLOAT DEFAULT 0,
            carbs FLOAT DEFAULT 0,
            fat FLOAT DEFAULT 0,
            serving_size VARCHAR(50) DEFAULT '100g',
            is_veg BOOLEAN DEFAULT TRUE,
            price_per_100g FLOAT DEFAULT 0,
            category VARCHAR(50) DEFAULT 'General',
            image_url VARCHAR(255)
        );
        
        CREATE TABLE IF NOT EXISTS plans (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            day INTEGER,
            breakfast TEXT DEFAULT '',
            lunch TEXT DEFAULT '',
            dinner TEXT DEFAULT '',
            snacks TEXT DEFAULT '',
            workout TEXT DEFAULT '',
            calories INTEGER DEFAULT 0,
            protein INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    run_seed()
