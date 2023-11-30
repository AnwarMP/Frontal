import tensorflow as tf
import pickle
import numpy as np
from google.cloud import storage

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def load_model_and_preprocessor():
    bucket_name = 'frontal_ai_model'
    model_path = 'models/my_model'
    preprocessor_path = 'models/preprocessor.pkl'

    download_blob(bucket_name, model_path, '/tmp/my_model')
    download_blob(bucket_name, preprocessor_path, '/tmp/preprocessor.pkl')

    # Load the TensorFlow model
    model = tf.keras.models.load_model('/tmp/my_model')
    # Load the preprocessor
    preprocessor = pickle.load(open('/tmp/preprocessor.pkl', 'rb'))

    return model, preprocessor

model, preprocessor = load_model_and_preprocessor()

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
    return str(prediction.tolist())