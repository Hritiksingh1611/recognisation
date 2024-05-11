from flask import Flask, request, jsonify
import boto3
from io import BytesIO
from PIL import Image

app = Flask(__name__)

rekognition_client = boto3.client('rekognition', region_name='us-east-1')

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/extract-information', methods=['POST'])
def extract_information():
    if 'image' not in request.files:
        return jsonify({'error': 'Image not provided'})

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No image selected'})

    image_bytes = image.read()

    response = rekognition_client.detect_text(Image={'Bytes': image_bytes})

    information = [text_detection['DetectedText'] for text_detection in response['TextDetections']]

    # Extracting parameter for name validation
    name_to_validate = request.form.get('name_to_validate')

    # Check if the name_to_validate is present in the information array
    if name_to_validate:
        if name_to_validate in information:
            validation_result = f"{name_to_validate} is present in the extracted information."
        else:
            validation_result = f"{name_to_validate} is not present in the extracted information."
    else:
        validation_result = "No name provided for validation."

    return jsonify({'information': information, 'name_validation_result': validation_result})


if __name__ == '__main__':
    app.run(debug=True)
