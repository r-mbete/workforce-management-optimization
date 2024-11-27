# Optimizing Workforce Management Through Machine Learning Employee Classification

## Project Overview

This project aims to optimize workforce management by using machine learning algorithms to classify employees based on various features. The goal is to develop a model that aids in improving workforce management decisions by predicting employee performance and behavior. The project currently focuses on two algorithms for classification: Decision Tree and AdaBoost.

## Algorithms Used

- **Decision Tree Classifier**: Used to create a model based on decision rules derived from the training data.
- **AdaBoost Classifier**: An ensemble method that combines multiple weak classifiers to create a strong classifier.

## Goal

The goal of this project is to classify employees effectively based on a variety of attributes, such as age, tenure, role, and performance ratings. We aim to achieve high classification accuracy, ensuring that the model can assist in making data-driven decisions regarding workforce management.

## Dataset

The dataset includes employee features such as:

- Age
- Tenure
- Role
- Department
- Other employee attributes (e.g., performance ratings)

The target variable is **Performance Rating**, which classifies employees into categories like "Exceeds," "Fully Meets," and "Needs Improvement."

## Getting Started

To run this project locally, follow the steps below:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/r-mbete/workforce-management-optimization.git
    ```

2. **Install Dependencies:**

    Install the necessary libraries and dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

    Alternatively, you can manually install the dependencies:

    ```bash
    pip install matplotlib seaborn pandas numpy lazypredict scikit-learn imbalanced-learn xgboost joblib
    ```

3. **Run the Jupyter Notebook:**

    To explore and run the model training and evaluation steps:

    ```bash
    jupyter notebook
    ```

    The main notebook `code.ipynb` contains all the preprocessing, modeling, and evaluation code.

4. **Backend Setup (Optional):**

    To set up and run the backend API:

    Navigate to the backend folder:

    ```bash
    cd backend
    ```

    Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

    Run the backend server:

    ```bash
    python app.py
    ```

    The backend is set up with a Flask app that can interact with the machine learning models and provide predictions via an API.

5. **Frontend Setup (Optional):**

    To set up and run the frontend:

    Navigate to the frontend folder.

    Install required dependencies:

    ```bash
    npm install
    ```

    Run the frontend:

    ```bash
    npm start
    ```

    The frontend allows users to input employee data and get predictions using the machine learning model.

## Code Structure

- `code.ipynb`: Jupyter notebook for data preprocessing, model training, and evaluation.
- `frontend/`: React-based frontend for the workforce management system.
- `backend/`: Flask-based backend API for serving machine learning models.

## Key Features in the Jupyter Notebook

- **Data Preprocessing:**
  - Duplicate value checks
  - Missing value treatment
  - Outlier checks using box plots
  - Feature engineering (if needed)

- **Model Building:**
  - Decision Tree Classifier for classification tasks.
  - AdaBoost Classifier for ensemble learning.

- **Model Evaluation:**
  - Performance metrics such as accuracy, precision, recall, F1-score, and confusion matrix are calculated for each model.
  - Visualization of performance using confusion matrix heatmaps.

- **Hyperparameter Tuning:**
  - Exploration of hyperparameters using techniques like RandomizedSearchCV.

## Issues and Assistance Needed

Currently, I am working on:

- Tuning the hyperparameters of the models for better performance.
- Ensuring the models generalize well to unseen data.
- Addressing potential issues with class imbalance using techniques like SMOTE (Synthetic Minority Over-sampling Technique).
- Connecting the frontend and backend efficiently.

Any suggestions, contributions, or feedback on improving the models or setting up the backend/frontend are greatly appreciated!
