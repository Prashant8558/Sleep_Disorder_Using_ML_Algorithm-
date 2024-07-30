from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
rf_model = joblib.load('rf_model.joblib')

# Function to transform categorical data to numerical
def transform_input(data):
    gender_mapping = {'Male': 1, 'Female': 0}
    occupation_mapping = {
        'Software Engineer': 1,
        'Doctor': 5,
        'Sales Representative': 3,
        # Add other occupations as needed
    }
    bmi_mapping = {
        'Underweight': 3,
        'Normal': 2,
        'Overweight': 0,
        'Obese': 1
    }

    gender = gender_mapping[data['gender']]
    occupation = occupation_mapping[data['occupation']]
    bmi_category = bmi_mapping[data['bmi_category']]

    sleep_duration = float(data['sleep_duration'])
    quality_of_sleep = int(data['quality_of_sleep'])
    physical_activity = int(data['physical_activity'])
    stress_level = int(data['stress_level'])
    heart_rate = int(data['heart_rate'])
    daily_steps = int(data['daily_steps'])

    # Split blood pressure into systolic and diastolic
    bp = data['blood_pressure'].split('/')
    systolic_bp = int(bp[0])
    diastolic_bp = int(bp[1])

    # Create the input array for the model
    input_array = np.array([[gender, data['age'], occupation, sleep_duration,
                             quality_of_sleep, physical_activity, stress_level,
                             bmi_category, heart_rate, daily_steps, systolic_bp, diastolic_bp]])

    return input_array

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    input_array = transform_input(data)

    # Make the prediction
    prediction = rf_model.predict(input_array)

    result = "Yes" if prediction[0] == 1 else "No"

    return render_template('index.html', prediction_text=f"Sleep Disorder: {result}")

if __name__ == "__main__":
    app.run(debug=True)
