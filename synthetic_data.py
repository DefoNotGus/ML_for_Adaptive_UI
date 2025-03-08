#TOOL FOR SAMPLING DATA FOR THE ML

import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Load the original dataset
file_path = "your_survey_data.csv"  # Update with the correct path
df = pd.read_csv(file_path)

# Function to generate synthetic survey data by sampling from real responses
def generate_synthetic_survey_data(n, original_df):
    synthetic_data = []
    
    for _ in range(n):
        row = {}
        for col in original_df.columns:
            if "timestamp" in col.lower():  # Generate a random timestamp
                row[col] = fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S")
            else:
                # Drop empty values and check if there are any valid choices
                valid_choices = original_df[col].dropna().tolist()
                row[col] = random.choice(valid_choices) if valid_choices else "N/A"  # Fallback value
        
        synthetic_data.append(row)
    
    return pd.DataFrame(synthetic_data)

# Generate 100 synthetic responses
synthetic_df = generate_synthetic_survey_data(100, df)

# Append synthetic data to the original dataset
combined_df = pd.concat([df, synthetic_df], ignore_index=True)

# Save the combined dataset
output_file = "combined_survey_data.csv"
combined_df.to_csv(output_file, index=False)

print(f"Synthetic data generated and saved as {output_file}")
