# scripts/_generate_hr_test_data.py
# Author: EmranAli24
# Last Updated: 2025-07-13 19:47:23
#
# This utility script generates a noisy HR-themed dataset for testing.
# It creates a CSV with employees, departments, and jobs, and introduces
# noise via duplicate columns (for dependents and phone numbers).

import pandas as pd
from faker import Faker
import random
import argparse
import os

def generate_hr_test_data(num_employees=100):
    """Generates a DataFrame with noisy, denormalized HR data."""
    fake = Faker()

    # --- 1. Create the "lookup" entities (the 'one' side of relationships) ---
    departments = [{'department_id': i+10, 'department_name': fake.job()} for i in range(10)]
    locations = [{'location_id': fake.uuid4(), 'city': fake.city(), 'country': fake.country()} for _ in range(5)]
    for dept in departments:
        dept.update(random.choice(locations)) # Denormalize location into department

    data = []
    for i in range(num_employees):
        dept = random.choice(departments)
        
        # --- 2. Create the primary record (the 'many' side) ---
        record = {
            'Employee ID': 1000 + i,
            'Full Name': fake.name(),
            'Email Address': fake.email(),
            'Hire Date': fake.date_between(start_date='-10y', end_date='today'),
            'Department Name': dept['department_name'],
            'City': dept['city'],
            'Country': dept['country']
        }

        # --- 3. Introduce Noise: Duplicate Columns ---
        # Add a variable number of dependents
        num_dependents = random.randint(0, 3)
        for j in range(num_dependents):
            col_name = 'Dependent' if j == 0 else f'Dependent.{j}'
            record[col_name] = fake.name()
            
        # Add a variable number of phone numbers
        num_phones = random.randint(1, 2)
        for j in range(num_phones):
            col_name = 'Phone Number' if j == 0 else f'Phone Number.{j}'
            record[col_name] = fake.phone_number()

        data.append(record)
        
        # --- 4. Introduce Noise: Continuation Rows ---
        # Occasionally add a row that should be a continuation of the previous one
        if random.random() < 0.1: # 10% chance
            continuation_record = {k: '' for k in record}
            # Add a new dependent to the otherwise empty row
            continuation_record['Dependent'] = fake.name()
            data.append(continuation_record)

    df = pd.DataFrame(data)
    
    # Reorder columns to be more realistic and messy
    col_order = [
        'Employee ID', 'Full Name', 'Email Address', 'Dependent', 'Dependent.1', 'Dependent.2',
        'Phone Number', 'Phone Number.1', 'Department Name', 'City', 'Country', 'Hire Date'
    ]
    # Filter to only include columns that were actually generated in this run
    existing_cols = [c for c in col_order if c in df.columns]
    return df[existing_cols]

def main(args):
    """Main function to generate and save the HR test data."""
    print(f"--- Generating a new noisy HR test dataset with {args.num_records} employees ---")
    
    noisy_df = generate_hr_test_data(args.num_records)
    
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    noisy_df.to_csv(args.output, index=False)
    
    print(f"\n✅ Successfully generated and saved HR test data to '{args.output}'")
    print(f"  - The file has {len(noisy_df)} rows and {len(noisy_df.columns)} columns.")
    print("  - It contains duplicate 'Dependent' and 'Phone Number' columns for testing.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Noisy HR Schema Test Data Generator.")
    parser.add_argument('-n', '--num-records', type=int, default=100,
                        help="Number of primary employee records to generate.")
    parser.add_argument('-o', '--output', type=str, default="data/raw/hr_test_data.csv",
                        help="Path to save the output noisy CSV file.")
    
    args = parser.parse_args()
    main(args)