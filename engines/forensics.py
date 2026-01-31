import cv2
import numpy as np

class ForensicsEngine:
    def __init__(self):
        # Initialize your DL model here if you have one
        # self.dl_model = load_model(...) 
        pass

    def get_frequency_score(self, image_path):
        """Math Sensor: Detects high-frequency patterns (FFT)"""
        img = cv2.imread(image_path, 0)
        if img is None: return 0.0
        
        # FFT Analysis
        dft = np.fft.fft2(img)
        dft_shift = np.fft.fftshift(dft)
        mag_spec = 20 * np.log(np.abs(dft_shift) + 1)
        
        # Normalize and return a score between 0 and 1
        # Using the higher denominator 210.0 we discussed for robustness
        score = np.mean(mag_spec) / 210.0
        return min(max(float(score), 0.0), 1.0)

    def detect_synthetic(self, image_path):
        """Unified Sensor: Fuses Math and Deep Learning signals"""
        # This is where the error was happening!
        sig_fft = self.get_frequency_score(image_path) 
        
        # Placeholder for your Deep Learning score
        # If you don't have a DL model yet, use 0.0 or sig_fft
        sig_dl = 0.0 
        
        # Weighted Fusion (Deliverable #6: Robustness)
        # Trusting Math 30% and DL 70% (or adjust as needed)
        final_prob = (sig_fft * 0.3) + (sig_dl * 0.7)
        
        return round(final_prob, 4)