from services.burnt import Burnt
from services.sharpness import Sharpness

def get_image_score(path):
    """
    ניקוד איכות כולל לתמונה
    """

    # שימוש במתודות סטטיות במקום ליצור מופע
    sharp = Sharpness.calculate_sharpness_laplacian(path)
    bright = Burnt.burnt_score(path)

    # שילוב משוקלל (אפשר לשנות לפי צורך)
    score = (sharp * 0.7) + (bright * 0.3)

    return score