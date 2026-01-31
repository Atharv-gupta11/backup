import logging
from transformers import pipeline
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepfakeDetector:
    """
    Detects AI-generated media using a pre-trained Vision Transformer (ViT).
    Model: dima806/deepfake_vs_real_image_detection
    """
    
    def __init__(self):
        self.pipe = None
        try:
            logger.info("⏳ Loading Deepfake Detection Model (ViT)...")
            # Uses a robust pre-trained model from Hugging Face
            self.pipe = pipeline("image-classification", model="dima806/deepfake_vs_real_image_detection")
            logger.info("✅ Deepfake Model Loaded Successfully")
        except Exception as e:
            logger.error(f"Failed to load Deepfake Model: {e}")

    def detect_deepfake(self, image: Image.Image):
        """
        Returns dictionary with:
        - fake_probability: 0.0 to 1.0
        - label: 'fake' or 'real'
        """
        results = {'fake_probability': 0.0, 'method': 'ViT-B/16'}
        
        if not self.pipe:
            return self._heuristic_fallback(image)

        try:
            # The pipeline returns a list of labels/scores
            # Example: [{'label': 'fake', 'score': 0.99}, {'label': 'real', 'score': 0.01}]
            preds = self.pipe(image)
            
            fake_score = 0.0
            for p in preds:
                label = p['label'].lower()
                if 'fake' in label or 'ai' in label:
                    fake_score = p['score']
                elif 'real' in label:
                    # If label is real, fake_score is (1 - real_score)
                    # But usually we just look for the fake label directly
                    pass
            
            # If the model only gave 'real' score, infer fake
            if fake_score == 0.0:
                 for p in preds:
                    if 'real' in p['label'].lower():
                        fake_score = 1.0 - p['score']

            results['fake_probability'] = round(float(fake_score), 4)

        except Exception as e:
            logger.error(f"Inference Error: {e}")
            return self._heuristic_fallback(image)
            
        return results

    def _heuristic_fallback(self, image):
        # ... (keep existing simple fallback)
        return {'fake_probability': 0.4, 'method': 'heuristic_fallback'}
