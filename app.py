from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import joblib
import numpy as np
import json
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Good practice to use a secret key

# --- Constants ---
USER_DATA_FILE = "users.json"
MODULES_FILE = "course_modules.json"
MODEL_FILES = {
    'text_size': 'rf_text_size.pkl',
    'image_size': 'rf_image_size.pkl'
}

# --- Helper Functions ---

def hash_password(password, salt=None):
    """Simple hashing with salt."""
    if not salt:
        salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"  # Store salt and hash together

def verify_password(stored_password, provided_password):
    """Verify stored hash with provided password."""
    salt, hashed = stored_password.split("$")
    return hash_password(provided_password, salt) == stored_password

def load_data(file_path, default_value):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return default_value

def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def load_models(model_files):
    models = {}
    try:
        for model_name, file_name in model_files.items():
            models[model_name] = joblib.load(file_name)
    except FileNotFoundError:
        print(f"Error: Model files not found. Ensure these files exist: {', '.join(model_files.values())}")
        exit()
    except Exception as e:
        print(f"Error loading models: {e}")
        exit()
    return models

# --- Load Models and Data ---
models = load_models(MODEL_FILES)

# --- Routes ---

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

@app.route('/insights')
def insights():
    return render_template('insights.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_data(USER_DATA_FILE, {})

    # Get the intended next page from the URL parameter or session
    next_page = request.args.get('next', session.pop('next_page', 'index'))  

    if 'username' in session:
        return redirect(url_for(next_page))  # Redirect immediately if already logged in

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username not in users:
            return render_template('login.html', error="Username not found. Please register.")
        if not verify_password(users[username].get('password', ''), password):
            return render_template('login.html', error="Incorrect password.")

        session['username'] = username
        return redirect(url_for(next_page))  # Redirect to the correct page

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/try', methods=['GET', 'POST'])
def try_out():
    if 'username' not in session:
        session['next_page'] = 'try_out'
        return redirect(url_for('login'))
    return render_template('prototype.html', username=session['username'])

@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'username' not in session:
        session['next_page'] = 'test'
        return redirect(url_for('login'))
    return render_template('testin.html', username=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Ensure the user is redirected to the correct next page after registration
    next_page = request.args.get('next', session.pop('next_page', 'index'))  

    if request.method == 'POST':
        users = load_data(USER_DATA_FILE, {})
        username = request.form.get('username', '').strip()

        if username in users:
            return render_template('register.html', error="Username already exists. Please choose a different username.")

        password = hash_password(request.form.get('password', '').strip())
        user_data = {
            'password': password,
            'age': request.form.get('age', '').strip(),
            'digital_challenges': request.form.get('digital_challenges', '').strip(),
            'application_challenges': request.form.get('application_challenges', '').strip(),
            'education_level': request.form.get('education_level', '').strip(),
            'current_device': request.form.get('current_device', '').strip(),
            'bgcolor': '#fff',
            'hcolor': '#7A287E'
        }

        # Prepare input data for ML model
        try:
            input_data = np.array([[int(user_data['age']), int(user_data['digital_challenges']),
                                    int(user_data['application_challenges']), int(user_data['education_level']),
                                    int(user_data['current_device'])]])
            
            user_data['text_size'] = float(models['text_size'].predict(input_data)[0])
            user_data['image_size'] = float(models['image_size'].predict(input_data)[0])
        except Exception as e:
            return render_template('register.html', error=f"Error processing user data: {e}")

        users[username] = user_data
        save_data(USER_DATA_FILE, users)

        session['username'] = username
        return redirect(url_for(next_page))  # Redirect to the correct page

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
