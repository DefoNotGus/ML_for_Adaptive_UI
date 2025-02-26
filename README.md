# ML_for_Adaptive_UI
My honours Project prototype

# Data Procesing:

## Overview
This script processes a CSV file (`form1.csv`) containing survey data and outputs a cleaned and transformed version as `data.csv`. The main steps include:
- Reading the CSV file
- Selecting relevant columns
- Mapping categorical data to numerical values
- Handling multiple-choice answers
- Converting numeric data types
- Saving the processed data to a new CSV file

---

## Step-by-Step Explanation

### 1. Read the Original CSV File
```python
import pandas as pd
df = pd.read_csv('form1.csv')
```
The script uses pandas to load `form1.csv` into a DataFrame.

### 2. Select Relevant Columns
```python
columns_to_keep = [
    'Text_Size', 'Image_Size', 'Digital_Challenges', 'Application_Challenges',
    'age', 'Tech_Comfort', 'Student_Status', 'Education_Level', 'Current_Device'
]
processed_df = df[columns_to_keep]
```
A subset of columns is extracted to remove unnecessary data.

### 3. Define Mapping Dictionaries
```python
digital_challenges_mapping = { 'Vision difficulties': 1, ... }
application_challenges_mapping = { 'Difficulty reading small text': 1, ... }
education_level_mapping = { 'None completed yet': 1, ... }
current_device_mapping = { 'Laptop': 1, ... }
```
Categorical values are mapped to numerical values for easier processing.

### 4. Convert Multiple-Choice Answers
```python
def convert_multiple_choices(x, mapping):
    if pd.isna(x): return []
    choices = x.split(', ')
    return [mapping.get(choice, 0) for choice in choices]
```
This function converts multiple-choice responses (comma-separated strings) into lists of numerical values.
```python
processed_df['Digital_Challenges'] = processed_df['Digital_Challenges'].apply(
    lambda x: convert_multiple_choices(x, digital_challenges_mapping))
processed_df['Application_Challenges'] = processed_df['Application_Challenges'].apply(
    lambda x: convert_multiple_choices(x, application_challenges_mapping))
```
Each multiple-choice column is processed using the defined mappings.

### 5. Convert Single-Choice Answers
```python
processed_df['Education_Level'] = processed_df['Education_Level'].map(education_level_mapping)
processed_df['Current_Device'] = processed_df['Current_Device'].map(current_device_mapping)
```
Single-choice categorical values are directly mapped to numeric values.

### 6. Convert Numeric Columns
```python
processed_df['Text_Size'] = pd.to_numeric(processed_df['Text_Size'], errors='coerce')
processed_df['Image_Size'] = pd.to_numeric(processed_df['Image_Size'], errors='coerce')
processed_df['age'] = pd.to_numeric(processed_df['age'], errors='coerce')
processed_df['Tech_Comfort'] = pd.to_numeric(processed_df['Tech_Comfort'], errors='coerce')
```
Ensures that numeric fields are properly converted.

### 7. Convert Binary Data
```python
processed_df['Student_Status'] = processed_df['Student_Status'].map({'Yes': 1, 'No': 0})
```
Binary categorical data is converted to numerical representation.

### 8. Save Processed Data
```python
processed_df.to_csv('data.csv', index=False)
print("Processed data has been saved to 'data.csv'")
```
The cleaned dataset is saved as `data.csv`.

---

## Summary
- Extracts and cleans survey data
- Converts categorical values to numerical format
- Handles multiple-choice responses properly
- Saves a processed version for further analysis

This processed dataset is now ready for machine learning or statistical analysis.

