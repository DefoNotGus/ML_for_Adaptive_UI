from flask import Flask, render_template, request
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
    course_modules = [
        "Math Fundamentals", "Python Basics", "Cybersecurity 101",
        "Machine Learning", "Data Science", "Web Development",
        "Networking", "Cloud Computing", "Ethical Hacking"
    ]

    # Default sizes for prototype 2 (static)
    text_size = 16  
    image_size = 265  

    if request.method == 'POST':
        prototype = request.form.get('prototype')

        if prototype == "prototype2":
            return render_template('prototype.html', course_modules=course_modules, text_size=text_size, image_size=image_size, prototype=2)

        elif prototype == "prototype1":
            try:
                # Extract user input
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

                return render_template('prototype.html', course_modules=course_modules, text_size=text_size, image_size=image_size, prototype=1)

            except ValueError:
                return "Error: Invalid input. Please enter numerical values."
            except Exception as e:
                return f"Error: {e}"

    return render_template('index.html', course_modules=course_modules)

if __name__ == '__main__':
    app.run(debug=True)
