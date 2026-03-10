from deepface import DeepFace
import numpy as np
import requests
from PIL import Image
import io

def generate_embedding(image_url: str) -> list:
    response = requests.get(image_url)

    image = Image.open(io.BytesIO(response.content))
    image_array = np.array(image)

    result = DeepFace.represent(
        img_path=image_array,
        model_name='Facenet512',
        enforce_detection=True
    )

    embedding = result[0]['embedding']

    vector = np.array(embedding)
    normalized = vector / np.linalg.norm(vector)
    
    return normalized.tolist()