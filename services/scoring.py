from services.burnt import burnt_score
from services.sharpness import calculate_sharpness_laplacian



def get_image_score(path):
    """
    ניקוד איכות כולל לתמונה
    """

    sharp = calculate_sharpness_laplacian(path)
    bright = burnt_score(path)

    # שילוב משוקלל (אפשר לשנות לפי צורך)
    score = (sharp * 0.7) + (bright * 0.3)

    return score