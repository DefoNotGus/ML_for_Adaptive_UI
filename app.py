from flask import Flask, render_template, request, url_for
import joblib
import numpy as np

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get form data
            age = int(request.form.get('age', 0))
            digital_challenges = int(request.form.get('Digital_Challenges', 0))
            application_challenges = int(request.form.get('Application_Challenges', 0))
            education_level = int(request.form.get('Education_Level', 0))
            current_device = int(request.form.get('Current_Device', 0))

            # Prepare input for model
            features = np.array([[age, digital_challenges, application_challenges, education_level, current_device]])

            # Make predictions
            text_size = rf_text_size.predict(features)[0]
            image_size = rf_image_size.predict(features)[0]

            return render_template('result.html', text_size=text_size, image_size=image_size)
        except ValueError:
            return "Error: Invalid input. Please enter numerical values."
        except Exception as e:
            return f"Error: {e}"

    return render_template('index.html')

@app.route('/moodle')
def moodle():
    return render_template('moodle.html') #This is meant to be a mock of an educational PLatform without text suggestion options.

if __name__ == '__main__':
    app.run(debug=True)