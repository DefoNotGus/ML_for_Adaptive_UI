# ML_for_Adaptive_UI: Adaptive UI Prediction Model Training

This project develops machine learning models to predict optimal UI text and image sizes based on user characteristics, encompassing data processing, model training, and deployment.

## Requirements

This project utilizes the following libraries for data processing, machine learning, and web application deployment:

-   **pandas:** Used for data manipulation, cleaning, and reading/writing CSV files in `data_processor.py` and `mlmodel.py`.
-   **numpy:** Employed for numerical operations, array manipulation, and data preprocessing in `mlmodel.py` and `app.py`.
-   **scikit-learn:** Provides machine learning models (`RandomForestRegressor`), data splitting (`train_test_split`), and evaluation metrics (`RMSE`, `R^2`) in `mlmodel.py`.
-   **joblib:** Used for model persistence, saving and loading trained machine learning models in `.pkl` format in `mlmodel.py` and `app.py`.
-   **Flask:** A web framework used in `app.py` to create the web application for deploying the machine learning models and providing a user interface.

## Setup

1.  **Create a Virtual Environment (Recommended):**

    * Navigate to the project directory in your terminal.
    * Run:
        ```bash
        python3 -m venv .venv
        ```
    * Or run:
        ```bash
        python -m venv .venv
        ```
    * Verify a `.venv` has been created
    * Add `.venv/` to your `.gitignore` file:
        ```bash
        echo ".venv/" >> .gitignore
        ```
    * Activate the virtual environment:
        * On macOS/Linux:
            ```bash
            source .venv/bin/activate
            ```
        * On Windows:
            ```bash
            .venv\Scripts\activate
            ```

2.  **Install Dependencies:**
    * With the virtual environment activated, run (recommended):
        ```bash
        pip install -r requirements.txt
        ```

    * Or you can run pip for using newer versions:
        ```bash
        pip install Flask joblib pandas scikit-learn numpy
        ```

3.  **Run the AUI Application:**
    
    this will initiate the the flask server locally and deploy the website prototype.
    * Execute the `app.py` script:
        ```bash
        python app.py
        ```

    * Open your web browser and navigate to the address displayed in the terminal.

## Project Files

* `app.py`: The main Flask application.
* `data_processor.py`: Data processing logic.
* `mlmodel.py`: Machine learning model logic.
* `data.csv`, `form1.csv`: Data files.
* `rf_image_size.pkl`, `rf_text_size.pkl`: Pre-trained machine learning models.
* `📁static`: Contains static files (CSS, JavaScript, images).
* `📁templates`: Contains HTML templates.
* `requirements.txt`: Lists the project's Python dependencies.

# Prototype:
## 1. Data Processing: Transforming Survey Data (`form1.csv` to `data.csv`)

### Overview

Transforms survey data for ML readiness, using a simple python called `data_processor.py`:

-   Reads `form1.csv`. Data colected from the [survey](www.gustavoelprofe.com/honours/form1.html).
-   Selects only key columns.
-   Maps categories to numbers.
-   Handles multiple-choice answers.
-   Convert all data to interger.
-   Saves this dataframe to `data.csv`.

### Step-by-Step Explanation

1.  **Read CSV:**
    ```python
    import pandas as pd
    df = pd.read_csv('form1.csv')
    ```

2.  **Select Columns:**
    ```python
    columns_to_keep = ['Text_Size', 'Image_Size', 'Digital_Challenges', ...]
    processed_df = df[columns_to_keep]
    ```

3.  **Mapping Dictionaries:**
    ```python
    digital_challenges_mapping = {'Vision difficulties': 1, ...}
    ```

4.  **Multiple-Choice Conversion:**
    ```python
    def convert_multiple_choices(x, mapping): ...
    processed_df['Digital_Challenges'] = processed_df['Digital_Challenges'].apply(...)
    ```

5.  **Single-Choice Mapping:**
    ```python
    processed_df['Education_Level'] = processed_df['Education_Level'].map(...)
    ```

6.  **Numeric Conversion:**
    ```python
    processed_df['Text_Size'] = pd.to_numeric(..., errors='coerce')
    ```

7.  **Binary Conversion:**
    ```python
    processed_df['Student_Status'] = processed_df['Student_Status'].map({'Yes': 1, 'No': 0})
    ```

8.  **Save to CSV:**
    ```python
    processed_df.to_csv('data.csv', index=False)
    ```

### Summary

-   Cleans and prepares survey data.
-   Converts categories to numerical format.
-   Handles multiple-choice responses.
-   Saves processed data for ML.

## 2. Model Training and Evaluation: Predicting UI Element Sizes

### Overview

We trained and evaluated Random Forest Regression models to predict optimal UI text and image sizes. This involved:

-   Loading `data.csv`.
-   Performing minimal preprocessing to ensure data compatibility with the model.
-   Training `RandomForestRegressor` models, selected for their:
    -   Ability to model non-linear relationships.
    -   Robustness against overfitting.
    -   Effectiveness with limited datasets.
-   Evaluating model performance using appropriate metrics.
-   Saving the trained models as `.pkl` files for efficient deployment.

We chose Random Forest Regressor because it effectively handles the complexities of predicting UI element sizes based on user characteristics. Saving the models enables rapid deployment and inference, crucial for real-time adaptive UI adjustments in diverse user environments.

### Step-by-Step Explanation

1.  **Data Loading:**
    ```python
    data = pd.read_csv('data.csv')
    ```

2.  **Preprocessing:**
    -   `fillna()` for missing values.
    -   `count_list_elements()` for challenge counts.
    -   Feature/target definition: `FEATURES`, `TARGETS`.
    -   Data splitting: `train_test_split()`.

3.  **Model Training:**
    ```python
    rf_text_size = RandomForestRegressor(...)
    rf_text_size.fit(X_train, y_train_text)
    ```

4.  **Predictions and Evaluation:**
    ```python
    y_pred_text = rf_text_size.predict(X_test)
    evaluate_model(y_test_text, y_pred_text, "Font Size") # RMSE, R^2
    ```

5.  **Model Saving:**
    ```python
    joblib.dump(rf_text_size, 'rf_text_size.pkl')
    ```

### Deployment

Saved models (`.pkl`) are ready for use in a web app to predict UI element sizes hosted in flask.

## 3. ML Deployment: Flask Web Application

### Overview

This section details the deployment of our trained machine learning models using a Flask web application. The application provides a user interface for inputting user characteristics, predicts optimal text and image sizes, and displays the results.

### Code Explanation (`app.py`)

1.  **Model Loading:**
    ```python
    try:
        rf_text_size = joblib.load('rf_text_size.pkl')
        rf_image_size = joblib.load('rf_image_size.pkl')
    except FileNotFoundError:
        print("Error: Model files not found.")
        exit()
    except Exception as e:
        print(f"Error loading models: {e}")
        exit()
    ```
    -   The application loads the trained `RandomForestRegressor` models from their `.pkl` files using `joblib.load()`.
    -   Error handling is implemented to gracefully manage scenarios where the model files are missing or corrupted.

2.  **`/` Route - Input and Prediction:**
    ```python
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            try:
                # Get form data
                age = int(request.form.get('age', 0))
                digital_challenges = int(request.form.get('Digital_Challenges', 0))
                # ... (other input fields) ...

                # Prepare input for model
                features = np.array([[age, digital_challenges, ...]])

                # Make predictions
                text_size = rf_text_size.predict(features)[0]
                image_size = rf_image_size.predict(features)[0]

                return render_template('result.html', text_size=text_size, image_size=image_size)
            except ValueError:
                return "Error: Invalid input."
            except Exception as e:
                return f"Error: {e}"
        return render_template('index.html')
    ```
    -   This route handles both GET and POST requests.
    -   Upon a POST request (form submission), it retrieves user inputs, prepares them as a NumPy array, and uses the loaded models to predict `text_size` and `image_size`.
    -   The predictions are then passed to `result.html` for display.
    -   Error handling is included to manage invalid input or prediction failures.
    -   A GET request renders `index.html`, which contains the input form.

3.  **`/moodle` Route - Mock Platform:**
    ```python
    @app.route('/moodle')
    def moodle():
        return render_template('moodle.html')
    ```
    -   This route serves a static mock educational platform page (`moodle.html`) without adaptive UI features, providing a baseline for comparison.

4.  **Application Execution:**
    ```python
    if __name__ == '__main__':
        app.run(debug=True)
    ```
    -   The Flask application is run in debug mode, enabling easier development and debugging.
