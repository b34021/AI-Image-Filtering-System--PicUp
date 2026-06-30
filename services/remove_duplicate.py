import numpy as np
import cv2
from insightface.app import FaceAnalysis


def _to_numpy(img):
    """המרת תמונה לכל פורמט תקין ל-insightface"""
    if img is None:
        return None

    # PIL → numpy
    if hasattr(img, "convert"):
        img = np.array(img.convert("RGB"))

    # RGBA → RGB
    if len(img.shape) == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    return img


def remove_duplicate_faces(face_data, similarity_threshold=0.6):

    if not face_data:
        return []

    embeddings = []
    unique_faces = []

    for img, emb in face_data:

        emb = emb / np.linalg.norm(emb)

        is_duplicate = False

        for e in embeddings:
            if np.dot(emb, e) > similarity_threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            embeddings.append(emb)
            unique_faces.append(img)

    return unique_faces