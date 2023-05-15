import tensorflow as tf
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
import tensorflow_hub as tfhub

app = Flask(__name__)

# Load the machine learning model from TensorFlow Hub
model_url = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
hub_module = tfhub.load(model_url)


@app.route('/predict', methods=['POST'])
def predict():
    # Get the user's drawing from the request
    drawing = request.json['drawing']
    
    # Convert the drawing to a PIL image
    drawing = np.array(drawing)
    image = Image.fromarray(drawing)

    # Resize the image to 256x256 pixels
    image = image.resize((256, 256))

    # Convert the image to a TensorFlow tensor
    image_tensor = tf.keras.preprocessing.image.img_to_array(image)
    image_tensor = tf.expand_dims(image_tensor, axis=0)
    image_tensor /= 255.0  # normalize the pixel values to [0, 1]


    # Stylize the image using the machine learning model
    stylized_image = hub_module(tf.constant(image_tensor))[0]


    # Convert the stylized image back to a PIL image
    stylized_image = np.array(stylized_image)
    stylized_image = np.uint8(255 * stylized_image)
    stylized_image = Image.fromarray(stylized_image)

    # Return the stylized image as a response
    return jsonify({'result': 'success', 'image': stylized_image})


if __name__ == '__main__':
    app.run(debug=True)

# Path: front-end\src\App.js

