from pathlib import Path
from services.vector_of_images import get_image_names
from services.burnt import burnt_score
from services.sharpness import calculate_sharpness_laplacian


def process_all_images(directory_path: str):

    images = get_image_names(directory_path)

    results = []

    for img in images:
        full_path = Path(directory_path) / img
        burntScore = burnt_score(str(full_path))
        sharpness_score = calculate_sharpness_laplacian(str(full_path))

        results.append([full_path, sharpness_score, burntScore])

    return results


if __name__ == "__main__":
    scores = process_all_images(r"O:\share\mb\test")
    print(scores)