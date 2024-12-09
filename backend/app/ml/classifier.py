import joblib
import numpy as np
import os

# Global variable to hold the model
model = None

def load_model():
    """
    Loads the pre-trained classification model from the file system.
    This function will be called once during the app's startup.
    """
    global model
    if model is None:  # Only load the model if it's not already loaded
        model_path = os.getenv('MODEL_PATH', 'app/ml/classifier.joblib')  # Get the model path from the environment variable
        if not model_path:
            raise ValueError("MODEL_PATH environment variable not set or model file not found.")
        
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")

def classify_performance(employee_data):
    """
    Classifies the employee's performance based on input features.
    
    Args:
        employee_data (dict): Employee data including features like age, years of experience, and education level.
        
    Returns:
        str: Classification result (e.g., 'Exceeds', 'Fully Meets', 'Needs Improvement')
        float: Confidence of the classification
    """
    # Ensure the model is loaded
    load_model()

    # Ensure features match the model's expected input format
    features = np.array([[employee_data['age'], employee_data['years_experience'], employee_data['education_level']]])

    # Classify the performance using the model
    classification = model.predict(features)
    confidence = model.predict_proba(features).max()  # Get the maximum confidence of the classification

    # Assuming the classification labels are 'Exceeds', 'Fully Meets', 'Needs Improvement'
    classification_label = ['Exceeds', 'Fully Meets', 'Needs Improvement'][classification[0]]
    
    return classification_label, confidence
