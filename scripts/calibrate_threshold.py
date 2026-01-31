import torch
import clip
from PIL import Image
import numpy as np
import os

# Configuration
REAL_DIR = "data/cosmos/real"      # Folder with 50 matching pairs
OOC_DIR = "data/cosmos/mismatched" # Folder with 50 OOC pairs
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=DEVICE)

def calculate_batch_scores(directory):
    scores = []
    # Assumes images and text are paired (e.g., img1.jpg and img1.txt)
    files = [f for f in os.listdir(directory) if f.endswith(('.jpg', '.png'))]
    
    for filename in files:
        try:
            img_path = os.path.join(directory, filename)
            txt_path = img_path.rsplit('.', 1)[0] + ".txt"
            
            with open(txt_path, 'r') as f:
                text = f.read().strip()
            
            image = preprocess(Image.open(img_path)).unsqueeze(0).to(DEVICE)
            text_tokens = clip.tokenize([text[:77]]).to(DEVICE) # CLIP limit
            
            with torch.no_grad():
                image_features = model.encode_image(image)
                text_features = model.encode_text(text_tokens)
                image_features /= image_features.norm(dim=-1, keepdim=True)
                text_features /= text_features.norm(dim=-1, keepdim=True)
                score = (image_features @ text_features.T).item()
                scores.append(score)
        except Exception as e:
            print(f"Skipping {filename}: {e}")
            
    return np.array(scores)

print("🧪 Starting Batch Calibration (50/50)...")
real_scores = calculate_batch_scores(REAL_DIR)
ooc_scores = calculate_batch_scores(OOC_DIR)

# --- STATISTICAL ANALYSIS ---
print("\n--- RESULTS ---")
print(f"✅ Real Pairs: Mean={np.mean(real_scores):.4f}, Std={np.std(real_scores):.4f}")
print(f"❌ OOC Pairs:  Mean={np.mean(ooc_scores):.4f}, Std={np.std(ooc_scores):.4f}")

# Calculate Golden Threshold (Intersection of two distributions)
golden_threshold = (np.mean(real_scores) + np.mean(ooc_scores)) / 2
print(f"\n🚀 RECOMMENDED THRESHOLD: {golden_threshold:.4f}")