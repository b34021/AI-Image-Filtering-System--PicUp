



import cv2
import numpy as np
class Sharpness:
     @staticmethod
     def  calculate_sharpness_laplacian(image_path):
        # Read the image in grayscale
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Apply the Laplacian operator
        laplacian = cv2.Laplacian(image, cv2.CV_64F)

        # Compute the variance of the Laplacian
        variance = laplacian.var()

        return variance



