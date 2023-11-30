import joblib
import numpy as np
import pickle
from flask import request
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.get_bucket("frontal_ai_model") # remember to change the bucket name
modelBlob = bucket.blob("model/models_2.pkl")
scalerBlob = bucket.blob("model/preprocessor.pkl")
modelBlob.download_to_filename("/tmp/models_2.pkl")
scalerBlob.download_to_filename("/tmp/preprocessor.pkl")    
model = joblib.load("/tmp/model_2.pkl")
preprocessor = pickle.load(open('/tmp/preprocessor.pkl', 'rb'))


def predict(request):
     # Extract data from request
    request_json = request.get_json()
    
    subject = request_json['class']
    print("subject received " + str(subject))

    problems = request_json['problems']
    print("problems received " + str(problems))

    priority = request_json['priority']
    print("priority received " + str(priority))

    row_values = [subject, problems, priority]
    print("creating numpy array")

    x_new = np.array(row_values).reshape(1,-1)

    # Preprocess the data
    processed_data = preprocessor.transform(x_new)

     # Make a prediction
    prediction = model.predict(processed_data)

    # Return the prediction
    return str(prediction)



