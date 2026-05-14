from pathlib import Path
from services.vector_of_images import get_image_names
from services.burnt import burnt_score


def process_all_images(directory_path: str):

    images = get_image_names(directory_path)

    results = []

    for img in images:
        full_path = Path(directory_path) / img
        score = burnt_score(str(full_path))
        results.append(score)

    return results


if __name__ == "__main__":
    scores = process_all_images(r"Y:\ברכי ומירי1\‏‏תיקיה חדשה")
    print(scores)