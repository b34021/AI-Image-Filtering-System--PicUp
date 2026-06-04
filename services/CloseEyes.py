import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# טען את מודל ה-Face Landmarker
base_options = python.BaseOptions(model_asset_path="face_landmarker.task")
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1
)
detector = vision.FaceLandmarker.create_from_options(options)

# אינדקסים של העיניים לפי FaceLandmarker
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(landmarks, eye_indices):
    pts = np.array([[landmarks[i].x, landmarks[i].y] for i in eye_indices])
    A = np.linalg.norm(pts[1] - pts[5])
    B = np.linalg.norm(pts[2] - pts[4])
    C = np.linalg.norm(pts[0] - pts[3])
    return (A + B) / (2.0 * C)

def detect_closed_eyes(image_path, threshold=0.2):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("לא ניתן לטעון תמונה")

    mp_image = mp.Image.create_from_file(image_path)
    result = detector.detect(mp_image)

    if not result.face_landmarks:
        return False  # אין פנים

    landmarks = result.face_landmarks[0]

    left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
    right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)

    return left_ear < threshold and right_ear < threshold

# שימוש לדוגמה
if detect_closed_eyes(r"O:\share\project miri and brachy\images\yoav_0051.JPG"):
    print("עיניים סגורות")
else:
    print("עיניים פתוחות")