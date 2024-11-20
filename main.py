# Import necessary libraries
import pandas as pd
from flask import Flask, render_template, request
import pickle
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load data and model
data = pd.read_csv("Data/Cleaned_Bengaluru_House_Data.csv")
pipe = pickle.load(open("Model/RidgeModel.pkl", 'rb'))

@app.route('/')
def index():
    # Get unique options for dropdowns
    locations = sorted(data['location'].unique())
    area_types = sorted(data['area_type'].unique())
    availabilities = sorted(data['availability'].unique())
    return render_template('index.html', locations=locations, area_types=area_types, availabilities=availabilities)

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve form inputs
    location = request.form.get('location')
    bhk = request.form.get('bhk')
    bathroom = request.form.get('bathroom')
    sqft = request.form.get('sqft')
    area_type = request.form.get('area_type')
    balcony = request.form.get('balcony')

    # Log inputs for debugging  
    print(location, bhk, bathroom, sqft, area_type, balcony)

    # Create input DataFrame
    input_df = pd.DataFrame([[location, sqft, bathroom, bhk, area_type,balcony]], 
                            columns=['location', 'total_sqft', 'bath', 'size(BHK)', 'area_type','balcony',])

    # Make prediction and format output
    prediction = pipe.predict(input_df)[0] * 1e5
    return str(np.round(prediction, 2))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5001)
