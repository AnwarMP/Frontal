from platform import processor
from flask import Flask, request, jsonify
import tensorflow as tf
import pandas as pd
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the TensorFlow model (replace 'path/to/model' with your model's actual path)
model = tf.keras.models.load_model('/Users/anwarmujeeb/Desktop/CS171/Frontal/Frontal/model102')

# Load the preprocessor using pickle
preprocessor = pickle.load(open('/Users/anwarmujeeb/Desktop/CS171/Frontal/Frontal/model/notebook/preprocessor.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract data from POST request
        data = request.get_json(force=True)

        # Extracting and converting the data
        subject = data['class']
        print("subject received " + str(subject))

       # Check if 'problems' is a string and convert if necessary
        problems = data['problems']
        if isinstance(problems, str):
            problems = float(problems) if '.' in problems else float(problems)
        problems = np.float64(problems)
        print("problems received " + str(problems))

        priority = data['priority']
        print("priority received " + str(priority))

        # Create a DataFrame with the converted values
        input_data = pd.DataFrame([[subject, problems, priority]], columns=['Subject', 'Problem Set', 'Priority'])


        # Preprocess the data as required by your model
        processed_data = preprocessor.transform(input_data)
        print(processed_data)

        # Make a prediction
        prediction = model.predict(processed_data)
        print(prediction)



        print("HARDCODED PREDICTION OF THE MODEL")
        input_data = pd.DataFrame([["Math42", 23, "High"]], columns=['Subject', 'Problem Set', 'Priority'])
        processed_input_data = preprocessor.transform(input_data)
        print(processed_input_data)
        print(model.predict(processed_input_data))
        model.summary()
        print(prediction.dtype)
        print(prediction.shape)
       

        # Return the prediction
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

# Rebuild the model with the weights
rebuilt_model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=[10]),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

rebuilt_model.compile(optimizer='adam', loss='mean_squared_error')

# rebuilt_model.load_weights('/Users/anwarmujeeb/Desktop/CS171/Frontal/Frontal/model/notebook/prelim_weights.h5')

@app.route('/newpredict', methods=['POST'])
def newpredict():
    try:
    #     # Extract data from POST request
    #     data = request.get_json(force=True)

    #     # Extracting and converting the data
    #     subject = data['class']
    #     print("subject received " + str(subject))

    #    # Check if 'problems' is a string and convert if necessary
    #     problems = data['problems']
    #     if isinstance(problems, str):
    #         problems = float(problems) if '.' in problems else float(problems)
    #     problems = np.float64(problems)
    #     print("problems received " + str(problems))

    #     priority = data['priority']
    #     print("priority received " + str(priority))

        # Create a DataFrame with the converted values
        input_data = pd.DataFrame([["Math42", 23, "High"]], columns=['Subject', 'Problem Set', 'Priority'])
        # Preprocess the data as required by your model
        processed_data = preprocessor.transform(input_data)
        print(processed_data)

        # Make a prediction
        prediction = rebuilt_model.predict(processed_data)
        print(prediction)    
        # Return the prediction
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
