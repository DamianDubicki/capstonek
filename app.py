from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
from PIL import Image
from flask_cors import CORS
import tensorflow as tf

app = Flask(__name__)
CORS(app)

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Load the label encoders for both artwork and artist
label_encoder_artwork = joblib.load("title_encoder.pkl")
label_encoder_artist = joblib.load("artist_encoder.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']

    # Process the image
    pil_image = Image.open(file.stream).convert('RGB')
    pil_image = pil_image.resize((224, 224))
    
    # Convert the image to a numpy array and normalize it for TensorFlow model
    image_array = np.expand_dims(np.array(pil_image), axis=0)
    image_array = image_array.astype(np.float32) / 127.5 - 1  # Same preprocessing as training

    # Set up model inputs and outputs
    input_details = interpreter.get_input_details()  # Model input info
    output_details = interpreter.get_output_details()  # Model output info

    # Feed the image array into the model
    interpreter.set_tensor(input_details[0]['index'], image_array)
    interpreter.invoke()  # Run inference

    # Get predictions for both artwork and artist
    artwork_predictions = interpreter.get_tensor(output_details[0]['index'])
    artist_predictions = interpreter.get_tensor(output_details[1]['index'])

    # Find the index of the highest predicted artwork and artist
    predicted_artwork_index = np.argmax(artwork_predictions)
    predicted_artist_index = np.argmax(artist_predictions)

    # Get predicted artwork and artist names back from label encoders
    predicted_artwork = label_encoder_artwork.inverse_transform([predicted_artwork_index])[0]
    predicted_artist = label_encoder_artist.inverse_transform([predicted_artist_index])[0]

    # Return the prediction results as JSON
    return jsonify({'artwork': predicted_artwork, 'artist': predicted_artist})

if __name__ == '__main__':
    app.run()
