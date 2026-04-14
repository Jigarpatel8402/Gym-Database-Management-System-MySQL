import csv
import random
from datetime import date, timedelta, time
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker()

# --- Configuration ---
MAX_MEMBER_ID = 1500  # Total members available
NUM_WORKOUT_PLANS = 2000 # Increased to 2000 (allows multiple plans per member)
NUM_ATTENDANCE = 1500    # Set to 1500
NUM_PROGRESS = 1000      # Set to 1000

# Set up date ranges for history (e.g., last 180 days)
today = date.today()
history_start_date = today - timedelta(days=180) 

# Helper to generate random time
def random_time(hour_min, hour_max):
    """Generates a random time object within specified hour range."""
    return time(
        random.randint(hour_min, hour_max), 
        random.randint(0, 59), 
        random.randint(0, 59)
    )

# ----------------------------------------------------------------------
## 1. WorkoutPlan Data Generation (2000 Records)
# NOTE: member_id is now randomized, allowing duplicates (multiple plans per member)
workoutplan_data = []
exercises = [
    'Bench Press', 'Squat', 'Deadlift', 'Overhead Press', 'Pull-ups',
    'Barbell Row', 'Dumbbell Curl', 'Triceps Extension', 'Leg Press', 
    'Treadmill Run', 'Elliptical Cardio', 'Yoga Session', 'Stretching Routine'
]

for i in range(1, NUM_WORKOUT_PLANS + 1):
    plan_id = i
    member_id = random.randint(1, MAX_MEMBER_ID) # Random member_id from 1 to 1500
    
    # Randomly determine if it's a strength (sets/reps) or cardio (duration/calories) exercise
    exercise = random.choice(exercises)
    
    # Logic to set sets/reps or duration/calories based on exercise type
    if 'Press' in exercise or 'Squat' in exercise or 'Deadlift' in exercise or 'Curl' in exercise or 'Extension' in exercise or 'Row' in exercise:
        sets = random.randint(3, 5)
        reps = random.choice([6, 8, 10, 12])
        duration = None
        calories_burned = None
    else: # Cardio/Other (Run, Cardio, Yoga, Stretching)
        sets = None
        reps = None
        duration = random.choice([20, 30, 45, 60])
        calories_burned = random.randint(100, 700)
        
        # Adjust calories for light activities
        if exercise in ['Yoga Session', 'Stretching Routine']:
            duration = random.choice([20, 30, 45])
            calories_burned = random.randint(50, 250)


    workoutplan_data.append({
        'plan_id': plan_id,
        'member_id': member_id,
        'exercise': exercise,
        'sets': sets,
        'reps': reps,
        'duration': duration, # Minutes
        'calories_burned': calories_burned
    })

# Create DataFrame and save to CSV
workoutplan_df = pd.DataFrame(workoutplan_data)
workoutplan_df.to_csv('workoutplan_data.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
print(f"Successfully created 'workoutplan_data.csv' with {NUM_WORKOUT_PLANS} records.")

# ----------------------------------------------------------------------
## 2. Attendance Data Generation (1500 Records)
attendance_data = []

for i in range(1, NUM_ATTENDANCE + 1):
    member_id = random.randint(1, MAX_MEMBER_ID)
    visit_date = fake.date_between(start_date=history_start_date, end_date=today)
    
    check_in = random_time(6, 21) # Check-in between 6 AM and 9 PM
    
    # Ensure check_out is later than check_in, and within a 3-hour window
    # Convert time to a common base for easy calculation
    check_in_dt_base = pd.to_datetime(str(visit_date) + ' ' + str(check_in))
    duration_minutes = random.randint(30, 180) # Visit lasts 30 min to 3 hours
    check_out_dt = check_in_dt_base + timedelta(minutes=duration_minutes)
    
    # Handle overnight checkouts (rare in a gym, but possible for late closing)
    # Here, we keep the date simple and just extract the time.
    
    attendance_data.append({
        'attendance_id': i,
        'member_id': member_id,
        'date': visit_date.isoformat(),
        'check_in': check_in.isoformat(),
        'check_out': check_out_dt.time().isoformat()
    })

# Create DataFrame and save to CSV
attendance_df = pd.DataFrame(attendance_data)
attendance_df.to_csv('attendance_data.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
print(f"Successfully created 'attendance_data.csv' with {NUM_ATTENDANCE} records.")

# ----------------------------------------------------------------------
## 3. Progress Data Generation (1000 Records)
progress_data = []
goal_statuses = ['On Track', 'Achieved', 'Needs Improvement', 'New Goal Set', 'Steady']

for i in range(1, NUM_PROGRESS + 1):
    member_id = random.randint(1, MAX_MEMBER_ID)
    progress_date = fake.date_between(start_date=history_start_date, end_date=today)
    
    # Generate body metrics
    weight_kg = round(random.uniform(50.0, 120.0), 1)
    
    # Simulate a fixed approximate height (to make BMI somewhat realistic, though not perfectly accurate)
    height_m = random.uniform(1.60, 1.90) 
    
    bmi = round(weight_kg / (height_m ** 2), 1)
    body_fat_pct = round(random.uniform(8.0, 45.0), 1)
    
    progress_data.append({
        'progress_id': i,
        'member_id': member_id,
        'date': progress_date.isoformat(),
        'weight_kg': weight_kg,
        'bmi': bmi,
        'body_fat_pct': body_fat_pct,
        'goal_status': random.choice(goal_statuses)
    })

# Create DataFrame and save to CSV
progress_df = pd.DataFrame(progress_data)
progress_df.to_csv('progress_data.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
print(f"Successfully created 'progress_data.csv' with {NUM_PROGRESS} records.")