import cv2
import numpy as np

class RobustnessEngine:
    def __init__(self):
        print("✅ RobustnessEngine initialized (Defense Layer)")

    def purify_image(self, image_path):
        """
        Applies a Gaussian Blur and Resizing to 'wash out' 
        potential adversarial noise (perturbations).
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
                
            # 1. Apply slight Gaussian Blur to remove pixel-level noise
            purified = cv2.GaussianBlur(img, (3, 3), 0)
            
            # 2. Standardize size to break scale-dependent attacks
            purified = cv2.resize(purified, (224, 224))
            
            # Save back to a temporary 'clean' file
            clean_path = image_path.replace(".jpg", "_clean.jpg")
            cv2.imwrite(clean_path, purified)
            
            return clean_path
        except Exception as e:
            print(f"Purification error: {e}")
            return image_path # Fallback to original