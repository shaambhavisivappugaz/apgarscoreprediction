from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the trained machine learning model
xgb = joblib.load('xgb.joblib')
abc = joblib.load('abc.joblib')
meta_model = joblib.load('new_meta_model.joblib')

# Define a function to perform label encoding on the categorical variables
def encode_values(df, cols):
    le = LabelEncoder()
    for col in cols:
        df[col] = le.fit_transform(df[col])
    return df

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    # Get the values of the selected radio buttons
    result = request.get_json()
    sex = result['sex']
    mode_of_delivery = result['mode_of_delivery']
    muscle_tone = result['muscle_tone']
    respiratory_effort = result['respiratory_effort']
    color = result['color']
    reflex_irritability = result['reflex_irritability']
    heart_rate = result['heart_rate1']
    birth_weight = result['c_birth_weight_g2']
    mother_age = result['mothers_age_cat']
    gest_age = result['c_cat_ga']

    # Create a new DataFrame with the selected values
    input_data = pd.DataFrame({
        'sex': [sex],
        'c_mode_of_delivery': [mode_of_delivery],
        'muscle_tone1': [muscle_tone],
        'respiratory_effort1': [respiratory_effort],
        'color1': [color],
        'reflex_irritability1': [reflex_irritability],
        'heart_rate1': [int(heart_rate)],
        'c_birth_weight_g2':[int(birth_weight)],
        'mothers_age_cat':[int(mother_age)],
        'c_cat_ga':[int(gest_age)]
    })

    # Encode the categorical variables using LabelEncoder
    categorical_cols = ['sex', 'c_mode_of_delivery', 'muscle_tone1', 'respiratory_effort1', 'color1', 'reflex_irritability1']
    input_data = encode_values(input_data, categorical_cols)

    # Reorder the columns in the same order as the feature names of the meta model
    input_data = input_data[['c_mode_of_delivery', 'sex', 'muscle_tone1', 'respiratory_effort1', 'color1', 'reflex_irritability1', 'heart_rate1', 'c_birth_weight_g2', 'mothers_age_cat', 'c_cat_ga']]



    # Use the trained machine learning models to make a prediction
    xgb_preds = xgb.predict(input_data)[0]
    print(xgb_preds)
    abc_preds = abc.predict(input_data)[0]
    print(abc_preds)
    stacked_predictions = np.column_stack((xgb_preds, abc_preds))
    print(stacked_predictions)
    prediction = meta_model.predict(stacked_predictions)
    print(prediction)
    # Return the predicted Apgar score as a JSON response
    return jsonify({'predicted_value': str(prediction)})


if __name__ == '__main__':
    app.run(debug=True)
