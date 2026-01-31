import os
import requests
from PIL import Image
from io import BytesIO

def download_placeholder_images(folder, limit=50, start_id=0):
    os.makedirs(folder, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    
    print(f"🚀 Downloading {limit} images to: {folder}...")
    
    for i in range(limit):
        try:
            # We use Picsum's specific ID system to ensure 100 UNIQUE images
            image_id = start_id + i
            url = f"https://picsum.photos/id/{image_id}/800/600"
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img_path = os.path.join(folder, f"sample_{i}.jpg")
                img.save(img_path, "JPEG")
                
                # Create matching .txt file
                txt_path = os.path.join(folder, f"sample_{i}.txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    if "real" in folder:
                        # For "Real", we provide a generic but plausible caption
                        f.write(f"A professional photograph of a scene (ID: {image_id}).")
                    else:
                        # For "Mismatched", we provide a CLEARLY wrong caption (Out of Context)
                        f.write("Breaking: This image shows a rare weather phenomenon captured on another planet.")
                
                if (i+1) % 10 == 0:
                    print(f"✅ Progress: {i+1}/{limit}")
            else:
                print(f"⚠️ Skipping ID {image_id}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Error on ID {image_id}: {e}")

if __name__ == "__main__":
    # 50 Real-logic samples (ID 1-50)
    download_placeholder_images("data/cosmos/real", 50, start_id=10)
    # 50 Mismatched-logic samples (ID 51-100)
    download_placeholder_images("data/cosmos/mismatched", 50, start_id=60)
    
    print("\n🎉 Dataset successfully generated using Lorem Picsum!")
    print("Run: python -m scripts.calibrate_threshold")