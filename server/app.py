import os
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


def download_file_from_gcs(url, local_path):
    r = requests.get(url)
    with open(local_path, 'wb') as f:
        f.write(r.content)

# URLs of the model and preprocessor in Google Cloud Storage
model_url = 'GCS_MODEL_URL'
preprocessor_url = 'GCS_PREPROCESSOR_URL'

# Download model and preprocessor
download_file_from_gcs(model_url, 'model.keras')
download_file_from_gcs(preprocessor_url, 'preprocessor.pkl')

# Load the model and preprocessor
model = tf.keras.models.load_model('model.keras')
preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from POST request
    data = request.get_json(force=True)

    # Extracting and converting the data
    subject = data['Subject']
    problems = float(data['Problem Set'])
    priority = data['Priority']

    # Create a DataFrame with the converted values
    input_data = pd.DataFrame([[subject, problems, priority]], columns=['Subject', 'Problem Set', 'Priority'])

    # Preprocess the data as required by your model
    processed_data = preprocessor.transform(input_data)

    # Make a prediction
    prediction = model.predict(processed_data)

    # Convert prediction to a list (or any other format suitable for JSON response)
    prediction_list = prediction.tolist()

    return jsonify(prediction_list)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
