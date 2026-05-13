#שיטות לבדיקת חדות


#שיטה מס' 1
import cv2
import numpy as np

def calculate_sharpness_laplacian(image_path):
    # Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply the Laplacian operator
    laplacian = cv2.Laplacian(image, cv2.CV_64F)

    # Compute the variance of the Laplacian
    variance = laplacian.var()

    return variance

# Example usage:
image_path_n1 = r'C:\Users\fisherm\Desktop\b.jpg'
image_path_n2 = r"C:\Users\fisherm\Desktop\b.jpg"
sharpness1 = calculate_sharpness_laplacian(image_path_n1)
sharpness2 = calculate_sharpness_laplacian(image_path_n2)
print("שיטה מס 1")
print(f"רמת חדות 1: {sharpness1}")
print(f"רמת חדות 2: {sharpness2}")


#שיטה מס' 2

def calculate_sharpness_sobel(image_path):
    # Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Sobel operator in both X and Y directions
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    # Compute the gradient magnitude
    sobel_magnitude = cv2.magnitude(sobel_x, sobel_y)

    # Compute the sharpness based on the magnitude
    sharpness = np.mean(sobel_magnitude)

    return sharpness
image_path_n1 = r'C:\Users\fisherm\Desktop\b.jpg'
image_path_n2 = r"C:\Users\fisherm\Desktop\b1.jpg"
sharpness1 = calculate_sharpness_sobel(image_path_n1)
sharpness2 = calculate_sharpness_sobel(image_path_n2)
print("שיטה מס 2")
print(f"רמת חדות 1: {sharpness1}")
print(f"רמת חדות 2: {sharpness2}")


#שיטה מס 3
import cv2
import numpy as np


def calculate_sharpness_fft(image_path):
    # Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply FFT (Fast Fourier Transform)
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)

    # Calculate the magnitude spectrum
    magnitude_spectrum = np.abs(fshift)

    # Calculate the sharpness based on the high-frequency content
    sharpness = np.sum(np.log(1 + magnitude_spectrum))  # Sum of high frequencies

    return sharpness
image_path_n1 = r'C:\Users\fisherm\Desktop\b.jpg'
image_path_n2 = r"C:\Users\fisherm\Desktop\b1.jpg"
sharpness1 = calculate_sharpness_fft(image_path_n1)
sharpness2 = calculate_sharpness_fft(image_path_n2)
print("שיטה מס 3")
print(f"רמת חדות 1: {sharpness1}")
print(f"רמת חדות 2: {sharpness2}")
