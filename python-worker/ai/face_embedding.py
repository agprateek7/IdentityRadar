from deepface import DeepFace
import numpy as np
import requests
from PIL import Image
import io

def generate_embedding(image_url: str) -> list:
    response = requests.get(image_url)
    # print("Status code:", response.status_code)
    # print("Content type:", response.headers.get('content-type'))
    # print("Content length:", len(response.content))

    image = Image.open(io.BytesIO(response.content))
    image_array = np.array(image)

    try:
        result = DeepFace.represent(
            img_path=image_array,
            model_name='Facenet512',
            enforce_detection=True
        )
    except FaceNotDetected:
          raise ValueError("No face detected in the image. Please upload a clear face photo.")

    embedding = result[0]['embedding']

    vector = np.array(embedding)
    normalized = vector / np.linalg.norm(vector)
    
    return normalized.tolist()