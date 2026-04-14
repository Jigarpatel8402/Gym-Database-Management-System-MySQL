import csv
import random
from datetime import date, timedelta
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker()

# --- Configuration ---
NUM_PAYMENTS = 500
NUM_EQUIPMENTS = 100
# Total number of members available in your Member table
MAX_MEMBER_ID = 1500 

# --- Payment Data Generation (500 Records with Unique member_id from 1500) ---
payment_data = []
payment_statuses = ['Paid', 'Pending', 'Overdue', 'Cancelled']

# Set up date ranges
today = date.today()
start_date = today - timedelta(days=365) # Payments over the last year

# 1. Generate a list of 500 unique member IDs sampled from 1 to 1500
# This is the key step to ensure uniqueness while respecting the pool size.
try:
    unique_member_ids = random.sample(range(1, MAX_MEMBER_ID + 1), NUM_PAYMENTS) 
except ValueError:
    print(f"Error: NUM_PAYMENTS ({NUM_PAYMENTS}) cannot be greater than MAX_MEMBER_ID ({MAX_MEMBER_ID}).")
    exit()

def generate_payment_record(payment_id, member_id):
    """Generates a single fake payment record."""
    payment_date = fake.date_between(start_date=start_date, end_date=today)
    
    # Calculate due date
    reference_date = payment_date + timedelta(days=random.randint(-15, 15))
    due_date = reference_date + timedelta(days=random.randint(7, 30))

    # Determine status
    status = random.choice(payment_statuses)
    if status == 'Pending' and due_date < today:
        status = 'Overdue'
    elif status == 'Paid' and payment_date > today:
        # Prevent 'Paid' status for future dates
        payment_date = due_date - timedelta(days=random.randint(1, 5))
        if payment_date > today:
             payment_date = today

    return {
        'payment_id': payment_id,
        'member_id': member_id, 
        'amount': round(random.uniform(25.00, 150.00), 2),
        'payment_date': payment_date.isoformat(),
        'due_date': due_date.isoformat(),
        'status': status
    }

# Loop through the list of unique member IDs
for i in range(NUM_PAYMENTS):
    payment_id = i + 1
    member_id_to_assign = unique_member_ids[i]
    payment_data.append(generate_payment_record(payment_id, member_id_to_assign))

# Create DataFrame and save to CSV
payments_df = pd.DataFrame(payment_data)
payments_df.to_csv('payment_data.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
print(f"Successfully created 'payment_data.csv' with {NUM_PAYMENTS} records and unique member IDs sampled from 1 to {MAX_MEMBER_ID}.")

# ----------------------------------------------------------------------

## Equipment Data Generation (100 Records)
equipment_data = []
equipment_types = ['Cardio', 'Strength', 'Free Weight', 'Accessory']
cardio_names = ['Treadmill', 'Elliptical', 'Spin Bike', 'Rowing Machine']
strength_names = ['Leg Press', 'Bench Press', 'Lat Pulldown', 'Cable Crossover']
free_weight_names = ['Dumbbell Rack', 'Barbell Set', 'Kettlebell Set', 'Weight Plates']
accessory_names = ['Yoga Mat', 'Resistance Band', 'Foam Roller']
condition_statuses = ['Excellent', 'Good', 'Needs Minor Repair', 'Out of Service']

def generate_equipment_record(equipment_id):
    """Generates a single fake equipment record."""
    equipment_type = random.choice(equipment_types)
    name = "Unknown"
    
    if equipment_type == 'Cardio':
        name = random.choice(cardio_names)
    elif equipment_type == 'Strength':
        name = random.choice(strength_names)
    elif equipment_type == 'Free Weight':
        name = random.choice(free_weight_names)
    elif equipment_type == 'Accessory':
        name = random.choice(accessory_names)
    
    # Generate a maintenance date within the last 18 months
    maintenance_date = fake.date_between(start_date=today - timedelta(days=540), end_date=today)
    
    return {
        'equipment_id': equipment_id,
        'name': name,
        'type': equipment_type,
        'maintenance_date': maintenance_date.isoformat(),
        'condition_status': random.choice(condition_statuses)
    }

for i in range(1, NUM_EQUIPMENTS + 1):
    equipment_data.append(generate_equipment_record(i))

# Create DataFrame and save to CSV
equipment_df = pd.DataFrame(equipment_data)
equipment_df.to_csv('equipment_data.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
print(f"Successfully created 'equipment_data.csv' with {NUM_EQUIPMENTS} records.")