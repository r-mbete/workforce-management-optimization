import joblib
import pandas as pd
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
    """
    # Ensure the model is loaded
    load_model()

    # Match feature names used during training
    feature_names = ['JobSatisfaction', 'WorkLifeBalance', 'YearsInCurrentRole', 'TotalWorkingYears']
    
    # Create a DataFrame with the appropriate feature names
    features = pd.DataFrame([employee_data], columns=feature_names)

    # Classify the performance using the model
    classification = model.predict(features)[0]  # Get the predicted numerical class
    confidence = model.predict_proba(features).max()  # Get the maximum confidence of the classification

    # Map numerical labels to descriptive labels
    label_mapping = {
        3: "Needs Improvement",
        4: "Fully Meets"
    }
    classification_label = label_mapping.get(classification, "Unknown")
    
    return classification_label, confidence



