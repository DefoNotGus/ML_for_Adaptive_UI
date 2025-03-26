from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response
import joblib
import numpy as np
import json
import os
import hashlib
from urllib.parse import unquote

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- Constants ---
USER_DATA_FILE = "data/users.json"
MODULES_FILE = "data/course_modules.json"
MODEL_FILES = {
    'text_size': 'models/rf_text_size.pkl',
    'image_size': 'models/rf_image_size.pkl'
}

# --- Helper Functions ---

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(stored_password, provided_password):
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
        print("Error: Model files not found.")
        exit()
    except Exception as e:
        print(f"Error loading models: {e}")
        exit()
    return models

# --- Load Models ---
models = load_models(MODEL_FILES)

# --- Routes ---

@app.route('/')
def index():
    print(MODULES_FILE)  # Debugging
    print(type(MODULES_FILE))
    return render_template('index.html', username=session.get('username'))

@app.route('/prototype')
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    users = load_data(USER_DATA_FILE, {})
    username = session.get("username", "guest")
    user_data = users.get(username, {"text_size": 16, "image_size": 100, "bgcolor": "#fff", "hcolor": "#7A287E"})
    courses = load_data(MODULES_FILE, [])

    response = render_template("prototype.html", course_modules=courses, **user_data)
    
    # Prevent caching
    response = app.make_response(response)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

@app.route('/module/<module_name>')
def module_page(module_name):
    """Handles module page rendering with session validation and cache prevention."""
    if "username" not in session:
        return redirect(url_for("login"))

    users = load_data(USER_DATA_FILE, {})
    username = session.get("username", "guest")
    user_data = users.get(username, {"text_size": 16, "image_size": 100, "bgcolor": "#fff", "hcolor": "#7A287E"})

    modules_data = load_data(MODULES_FILE, {}).get("modules", [])

    # Decode and normalize the module_name from the URL
    decoded_module_name = unquote(module_name).strip().lower()

    # Find the matching module
    selected_module = next(
        (module for module in modules_data if module["name"].strip().lower() == decoded_module_name),
        None
    )

    if not selected_module:
        return "Module not found", 404

    response = render_template("module.html", module=selected_module, **user_data)

    # Prevent caching
    response = app.make_response(response)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

@app.route('/insight')
def insight():
    response = render_template("insight.html")

    # Prevent caching
    response = app.make_response(response)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_data(USER_DATA_FILE, {})
    next_page = request.args.get('next', 'prototype')  # Default to 'prototype' if not provided

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username not in users or not verify_password(users[username].get('password', ''), password):
            return render_template('login.html', error="Invalid credentials.")

        session['username'] = username
        return redirect(f'/{next_page}')  # Redirects correctly to the intended path

    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()  # Clears session data
    response = make_response(redirect(url_for("index")))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_data(USER_DATA_FILE, {})
        username = request.form.get('username', '').strip()
        if username in users:
            return render_template('register.html', error="Username already exists.")
        password = hash_password(request.form.get('password', '').strip())
        user_data = {
            'password': password,
            'age': request.form.get('age', ''),
            'digital_challenges': request.form.get('digital_challenges', ''),
            'application_challenges': request.form.get('application_challenges', ''),
            'education_level': request.form.get('education_level', ''),
            'current_device': request.form.get('current_device', ''),
            'bgcolor': '#f4f4f4',
            'hcolor': '#800080'
        }
        input_data = np.array([[int(user_data[k]) for k in ['age', 'digital_challenges', 'application_challenges', 'education_level', 'current_device']]])
        user_data['text_size'] = float(models['text_size'].predict(input_data)[0])
        user_data['image_size'] = float(models['image_size'].predict(input_data)[0])
        users[username] = user_data
        save_data(USER_DATA_FILE, users)
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route("/save_preferences", methods=["POST"])
def save_preferences():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 403

    print("Received data:", request.json)  # Debugging line

    users = load_data(USER_DATA_FILE, {})
    users[session["username"]].update(request.json)
    save_data(USER_DATA_FILE, users)

    return jsonify({"message": "Changes saved successfully!"})


@app.route("/recalculate_ui", methods=["POST"])
def recalculate_ui():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 403
    users = load_data(USER_DATA_FILE, {})
    username = session["username"]
    user_data = users.get(username, {})
    input_data = np.array([[int(user_data[k]) for k in ['age', 'digital_challenges', 'application_challenges', 'education_level', 'current_device']]])
    users[username]['text_size'] = float(models['text_size'].predict(input_data)[0])
    users[username]['image_size'] = float(models['image_size'].predict(input_data)[0])
    save_data(USER_DATA_FILE, users)
    return jsonify({"text_size": users[username]['text_size'], "image_size": users[username]['image_size']})

@app.route("/change_password", methods=["POST"])
def change_password():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 403
    data = request.json
    new_password = data.get("new_password")
    users = load_data(USER_DATA_FILE, {})
    users[session["username"]]["password"] = hash_password(new_password)
    save_data(USER_DATA_FILE, users)
    return jsonify({"message": "Password changed successfully!"})

@app.route("/delete_account", methods=["POST"])
def delete_account():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 403
    users = load_data(USER_DATA_FILE, {})
    users.pop(session["username"], None)
    save_data(USER_DATA_FILE, users)
    session.pop("username", None)
    return jsonify({"message": "Account deleted successfully!"})

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    app.run(debug=True)
