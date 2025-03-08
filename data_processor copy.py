import pandas as pd
import tkinter as tk
from tkinter import filedialog

# DEPLOY A GUI THAT SHOWS ALL THE CSV IN THIS FOLDER
def choose_csv():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])  # Let the user choose a CSV file
    return file_path

# WITH A TEXT BOX FOR THE USER TO CHOOSE A NAME FOR THE CSV TO BE CREATED
def get_new_csv_name():
    root = tk.Tk()
    root.title("Enter the New CSV Name")
    label = tk.Label(root, text="Enter the name of the new CSV file (without extension):")
    label.pack(padx=10, pady=5)
    new_name_entry = tk.Entry(root)
    new_name_entry.pack(padx=10, pady=5)
    
    def on_submit():
        root.quit()

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(padx=10, pady=10)
    
    root.mainloop()

    # Return the name entered by the user
    return new_name_entry.get() + ".csv"  # Append '.csv' extension

# Function to convert multiple choice answers to numeric lists
def convert_multiple_choices(x, mapping):
    if pd.isna(x):
        return []
    choices = x.split(', ')  # Assuming choices are separated by comma and space
    return [mapping.get(choice, 0) for choice in choices]

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

# DEPLOY A GUI TO CHOOSE A CSV FILE
file_name = choose_csv()
if not file_name:
    print("No file selected. Exiting.")
    exit()

# Read the original CSV file
df = pd.read_csv(file_name)

# CHANGE ALL THE COLUMNS NAME IN THE CHOSEN CSV TO THIS ONES RESPECTIVELY:
df.columns = [
    'Timestamp', 'Text_Size', 'Image_Size', 'Digital_Challenges', 
    'Application_Challenges', 'age', 'Tech_Comfort', 'Primary_devices', 
    'Student_Status', 'Education_Level', 'Platforms_used', 'feedbackBlackBoard',
    'feedbackMoodle', 'feedbackBrightspace', 'feedbackCanvas', 'feedbackAtutor',
    'feedbackAula', 'Current_Device'
]

# Create new dataframe with only the specified columns
processed_df = df[columns_to_keep]

# Convert multiple choice columns
processed_df.loc[:, 'Digital_Challenges'] = processed_df['Digital_Challenges'].apply(
    lambda x: convert_multiple_choices(x, digital_challenges_mapping))

processed_df.loc[:, 'Application_Challenges'] = processed_df['Application_Challenges'].apply(
    lambda x: convert_multiple_choices(x, application_challenges_mapping))

# Convert single choice columns
processed_df.loc[:, 'Education_Level'] = processed_df['Education_Level'].map(education_level_mapping)
processed_df.loc[:, 'Current_Device'] = processed_df['Current_Device'].map(current_device_mapping)

# Convert Text_Size and Image_Size to numeric if they aren't already
processed_df.loc[:, 'Text_Size'] = pd.to_numeric(processed_df['Text_Size'], errors='coerce')
processed_df.loc[:, 'Image_Size'] = pd.to_numeric(processed_df['Image_Size'], errors='coerce')

# Convert age to numeric
processed_df.loc[:, 'age'] = pd.to_numeric(processed_df['age'], errors='coerce')

# Convert Tech_Comfort to numeric if it's not already
processed_df.loc[:, 'Tech_Comfort'] = pd.to_numeric(processed_df['Tech_Comfort'], errors='coerce')

# Convert Student_Status to numeric (assuming it's binary Yes/No)
processed_df.loc[:, 'Student_Status'] = processed_df['Student_Status'].map({'Yes': 1, 'No': 0})

# Get the new CSV file name from the user
new_csv_name = get_new_csv_name()

# Save the processed dataframe to a new CSV file
processed_df.to_csv(new_csv_name, index=False)

print(f"Processed data has been saved to '{new_csv_name}'")
