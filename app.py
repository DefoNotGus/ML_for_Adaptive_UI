from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import json
import os

app = Flask(__name__)

# Load trained models
try:
    rf_text_size = joblib.load('rf_text_size.pkl')
    rf_image_size = joblib.load('rf_image_size.pkl')
except FileNotFoundError:
    print("Error: Model files not found. Ensure 'rf_text_size.pkl' and 'rf_image_size.pkl' exist.")
    exit()
except Exception as e:
    print(f"Error loading models: {e}")
    exit()

USER_DATA_FILE = "users.json"

# Function to load users
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save users
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    course_modules = [
        "Math Fundamentals", "Python Basics", "Cybersecurity",
        "Machine Learning", "Data Science", "Web Development",
        "Networking", "Cloud Computing", "Ethical Hacking"
    ]

    text_size = 16  
    image_size = 250  
    users = load_users()
    error_message = None

    if request.method == 'POST':
        prototype = request.form.get('prototype')

        # Handle Prototype 2 (No username required)
        if prototype == "prototype2":
            return render_template('prototype.html', course_modules=course_modules, text_size=text_size, image_size=image_size, prototype=2)

        # Handle Prototype 1 (Requires user input)
        username = request.form.get('username', '').strip()
        if not username:
            error_message = "Error: Username is required for Prototype 1."
            return render_template('index.html', course_modules=course_modules, error=error_message)

        if username in users:
            error_message = "Error: Username already exists. Choose a different one."
            return render_template('index.html', course_modules=course_modules, error=error_message)

        try:
            # Extract all features correctly from the form
            age = int(request.form.get('age', 0))
            digital_challenges = int(request.form.get('digital_challenges', -1))  # -1 if not provided
            application_challenges = int(request.form.get('application_challenges', -1))  # -1 if not provided
            education_level = int(request.form.get('education_level', -1))  # -1 if not provided
            current_device = int(request.form.get('current_device', -1))  # -1 if not provided

            # Ensure valid inputs (Replace -1 with default mean values if missing)
            default_values = {"digital_challenges": 1, "application_challenges": 1, "education_level": 2, "current_device": 1}
            digital_challenges = digital_challenges if digital_challenges != -1 else default_values["digital_challenges"]
            application_challenges = application_challenges if application_challenges != -1 else default_values["application_challenges"]
            education_level = education_level if education_level != -1 else default_values["education_level"]
            current_device = current_device if current_device != -1 else default_values["current_device"]

            # Prepare input for model
            features = np.array([[age, digital_challenges, application_challenges, education_level, current_device]])

            # Make predictions
            text_size = rf_text_size.predict(features)[0]
            image_size = rf_image_size.predict(features)[0]

            # Save user data
            users[username] = {
                "prototype": 1,
                "age": age,
                "digital_challenges": digital_challenges,
                "application_challenges": application_challenges,
                "education_level": education_level,
                "current_device": current_device,
                "text_size": text_size,
                "image_size": image_size
            }
            save_users(users)

            return render_template('prototype.html', course_modules=course_modules, text_size=text_size, image_size=image_size, prototype=1, username=username)

        except ValueError:
            error_message = "Error: Invalid input. Please enter numerical values."
        except Exception as e:
            error_message = f"Error: {e}"

        return render_template('index.html', course_modules=course_modules, error=error_message)

    return render_template('index.html', course_modules=course_modules)

if __name__ == '__main__':
    app.run(debug=True)
