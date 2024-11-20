import joblib
import numpy as np

# Load pre-trained model (update the path to your actual model file)
model = joblib.load('path/to/your/model.joblib')

def predict_performance(employee_data):
    # Assuming the model takes a list of features like: [age, years_experience, etc.]
    features = np.array([[employee_data['age'], employee_data['years_experience'], employee_data['education_level']]])
    prediction = model.predict(features)
    confidence = model.predict_proba(features).max()  # Get the confidence of prediction
    return prediction[0], confidence
