"""
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

"""
"""
#2-מחזיר 0-עיניים סגורות, 1-עיניים פתןחות
def detect_closed_eyes2(image_path, threshold=0.2):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("לא ניתן לטעון תמונה")

    mp_image = mp.Image.create_from_file(image_path)
    result = detector.detect(mp_image)

    if not result.face_landmarks:
        return 0  # אין פנים נחשבים כעיניים סגורות

    landmarks = result.face_landmarks[0]

    left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
    right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)

    # אם שתי העיניים מעל הסף, נחשבות פתוחות
    if left_ear >= threshold or right_ear >= threshold:
        return 1  # עיניים פתוחות
    else:
        return 0  # עיניים סגורות
#דוגמא לשימוש:
status = detect_closed_eyes2(r"O:\share\project miri and brachy\images\yoav_0051.JPG")

if status == 1:
    print("עיניים פתוחות")
else:
    print("עיניים סגורות")
"""

"""
"""
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class EyeOpennessDetector:
    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    def __init__(self, model_path: str):
        base_options = python.BaseOptions(model_asset_path=model_path)

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            num_faces=1
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)

    @staticmethod
    def _ear(landmarks, eye_indices):
        pts = np.array(
            [[landmarks[i].x, landmarks[i].y] for i in eye_indices],
            dtype=np.float32
        )

        vertical_1 = np.linalg.norm(pts[1] - pts[5])
        vertical_2 = np.linalg.norm(pts[2] - pts[4])
        horizontal = np.linalg.norm(pts[0] - pts[3])

        if horizontal < 1e-6:
            return 0.0

        return (vertical_1 + vertical_2) / (2.0 * horizontal)

    @staticmethod
    def _normalize_score(ear: float,
                         closed_threshold: float = 0.18,
                         open_threshold: float = 0.32) -> float:
        score = (ear - closed_threshold) / (
            open_threshold - closed_threshold
        )
        return float(np.clip(score, 0.0, 1.0))

    def detect_eye_openness(self, image_path: str) -> float:
        mp_image = mp.Image.create_from_file(image_path)

        result = self.detector.detect(mp_image)

        if not result.face_landmarks:
            return 0.0

        landmarks = result.face_landmarks[0]

        left_ear = self._ear(landmarks, self.LEFT_EYE)
        right_ear = self._ear(landmarks, self.RIGHT_EYE)

        avg_ear = (left_ear + right_ear) / 2.0

        return self._normalize_score(avg_ear)

    detector = EyeOpennessDetector(
        model_path=r"C:\models\face_landmarker.task"
    )

    score = detector.detect_eye_openness(
        r"O:\share\project miri and brachy\images\yoav_0051.JPG"
    )

    print(f"Eye openness score: {score:.3f}")

    if score < 0.3:
        print("Closed")
    elif score > 0.7:
        print("Open")
    else:
        print("Partially open")


