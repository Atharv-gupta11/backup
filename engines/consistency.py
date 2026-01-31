import torch
import clip
from PIL import Image

class ConsistencyEngine:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        print(f"✅ ConsistencyEngine initialized on {self.device}")

    def compute_consistency(self, image_path, text_claim):
        try:
            # 1. Preprocess Image
            image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
            
            # 2. ENHANCED: Prompt Templating (Generalization for PS 2)
            # We check the claim against several templates to find the best match
            templates = [
                f"a photo of {text_claim}",
                f"a picture showing {text_claim}",
                f"an image of {text_claim}",
                text_claim
            ]
            
            text_inputs = clip.tokenize(templates).to(self.device)

            # 3. Compute Features
            with torch.no_grad():
                image_features = self.model.encode_image(image)
                text_features = self.model.encode_text(text_inputs)

                # Normalize features
                image_features /= image_features.norm(dim=-1, keepdim=True)
                text_features /= text_features.norm(dim=-1, keepdim=True)

                # 4. Calculate Maximum Similarity across all templates
                similarity = (image_features @ text_features.T).max().item()
            
            # 5. Calibration: Scale the score to a 0-1 range that's easier to threshold
            # Raw CLIP scores are often low (0.2-0.3); we boost it for usability
            calibrated_score = min(max((similarity - 0.15) / (0.45 - 0.15), 0.0), 1.0)
            
            return round(float(calibrated_score), 4)

        except Exception as e:
            print(f"Consistency Error: {e}")
            return 0.0