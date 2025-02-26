import pandas as pd

# Read the original CSV file
df = pd.read_csv('form1.csv')

# List of columns to keep
columns_to_keep = [
    'Text_Size',
    'Image_Size',
    'Digital_Challenges',
    'Application_Challenges',
    'age',
    'Tech_Comfort',
    'Student_Status',
    'Education_Level',
    'Current_Device'
]

# Create new dataframe with only the specified columns
processed_df = df[columns_to_keep]

# Define mapping dictionaries for categorical variables
digital_challenges_mapping = {
    'Vision difficulties': 1,
    'Hand tremors or motor control issues': 2,
    'Difficulty with precise clicking/tapping': 3,
    'Memory or cognitive challenges (Do you forget or get lost on the navigation)': 4,
    'Hearing impairment': 5
}

application_challenges_mapping = {
    'Difficulty reading small text': 1,
    'Difficulty navigating menus': 2,
    'Difficulty distinguishing colours': 3,
    'Difficulty understanding instructions': 4,
    'Difficulty clicking small buttons or icons': 5,
    'Slow application performance': 6,
    'Sound or audio not being clear enough': 7
}

education_level_mapping = {
    'None completed yet': 1,
    'Primary/Elementary school': 2,
    'Secondary/High school/GCSE': 3,
    'A-levels or equivalent': 4,
    'Vocational training/Trade school': 5,
    "Bachelor's degree": 6,
    "Master's degree": 7,
    'Doctorate or equivalent': 8,
    'Prefer not to answer': 9,
    'Overseas or Different Countries Education systems': 10
}

current_device_mapping = {
    'Laptop': 1,
    'PC Desktop': 2,
    'Mobile Phone': 3,
    'Tablet or Ipad': 4
}

# Function to convert multiple choice answers to numeric lists
def convert_multiple_choices(x, mapping):
    if pd.isna(x):
        return []
    choices = x.split(', ')  # Assuming choices are separated by comma and space
    return [mapping.get(choice, 0) for choice in choices]

# Convert multiple choice columns
processed_df['Digital_Challenges'] = processed_df['Digital_Challenges'].apply(
    lambda x: convert_multiple_choices(x, digital_challenges_mapping))

processed_df['Application_Challenges'] = processed_df['Application_Challenges'].apply(
    lambda x: convert_multiple_choices(x, application_challenges_mapping))

# Convert single choice columns
processed_df['Education_Level'] = processed_df['Education_Level'].map(education_level_mapping)
processed_df['Current_Device'] = processed_df['Current_Device'].map(current_device_mapping)

# Convert Text_Size and Image_Size to numeric if they aren't already
processed_df['Text_Size'] = pd.to_numeric(processed_df['Text_Size'], errors='coerce')
processed_df['Image_Size'] = pd.to_numeric(processed_df['Image_Size'], errors='coerce')

# Convert age to numeric
processed_df['age'] = pd.to_numeric(processed_df['age'], errors='coerce')

# Convert Tech_Comfort to numeric if it's not already
processed_df['Tech_Comfort'] = pd.to_numeric(processed_df['Tech_Comfort'], errors='coerce')

# Convert Student_Status to numeric (assuming it's binary Yes/No)
processed_df['Student_Status'] = processed_df['Student_Status'].map({'Yes': 1, 'No': 0})

# Save the processed dataframe to a new CSV file
processed_df.to_csv('data.csv', index=False)

print("Processed data has been saved to 'data.csv'")
