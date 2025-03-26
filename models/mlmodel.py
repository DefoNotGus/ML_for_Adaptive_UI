import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Define file path
DATA_FILE = 'data.csv'  # Update with actual file path

# Load data safely
try:
    data = pd.read_csv(DATA_FILE)
    print("Data loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file '{DATA_FILE}' was not found.")
    exit()
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# Data Preprocessing
# Handle missing values
data.fillna({
    'Education_Level': data['Education_Level'].median(),  # Replace NaN with median education level
    'Digital_Challenges': '[]',  # Replace NaN with empty list representation
    'Application_Challenges': '[]'
}, inplace=True)

# Convert categorical lists (stored as strings) to numerical feature counts
def count_list_elements(value):
    """Safely count elements in a list stored as a string."""
    try:
        return len(eval(value)) if isinstance(value, str) else 0
    except:
        return 0

data['Digital_Challenges'] = data['Digital_Challenges'].apply(count_list_elements)
data['Application_Challenges'] = data['Application_Challenges'].apply(count_list_elements)

# Define input features (X) and target variables (y)
FEATURES = ['age', 'Digital_Challenges', 'Application_Challenges', 'Education_Level', 'Current_Device']
TARGETS = ['Text_Size', 'Image_Size']

if not all(col in data.columns for col in FEATURES + TARGETS):
    print("Error: Missing required columns in dataset.")
    exit()

X = data[FEATURES]
y_text_size = data['Text_Size']
y_image_size = data['Image_Size']

# Split dataset into training and testing sets (30% test data)
X_train, X_test, y_train_text, y_test_text = train_test_split(X, y_text_size, test_size=0.3, random_state=42)
_, _, y_train_image, y_test_image = train_test_split(X, y_image_size, test_size=0.3, random_state=42)

# Initialize and train Random Forest models
rf_text_size = RandomForestRegressor(random_state=42, n_estimators=100)
rf_image_size = RandomForestRegressor(random_state=42, n_estimators=100)

rf_text_size.fit(X_train, y_train_text)
rf_image_size.fit(X_train, y_train_image)

# Make predictions
y_pred_text = rf_text_size.predict(X_test)
y_pred_image = rf_image_size.predict(X_test)

# Evaluate model performance
def evaluate_model(y_true, y_pred, label):
    """Calculate and print RMSE and R^2 score."""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"{label} Prediction:")
    print(f"RMSE: {rmse:.4f}")
    print(f"R^2: {r2:.4f}\n")

evaluate_model(y_test_text, y_pred_text, "Font Size")
evaluate_model(y_test_image, y_pred_image, "Image Size")

# Save trained models for later deployment
joblib.dump(rf_text_size, 'rf_text_size.pkl')
joblib.dump(rf_image_size, 'rf_image_size.pkl')
print("Models saved successfully for deployment.")
