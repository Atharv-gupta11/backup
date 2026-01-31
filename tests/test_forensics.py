import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.forensics import ForensicsEngine

def test_forensics():
    engine = ForensicsEngine()
    image_path = "test.jpg" # Use the same test image

    if not os.path.exists(image_path):
        print("❌ Error: test.jpg missing.")
        return

    score = engine.detect_synthetic(image_path)
    print(f"🔬 AI-Generated Probability Score: {score}")
    
    if isinstance(score, float):
        print("🚀 Forensics Engine is OPERATIONAL!")
    else:
        print(f"⚠️ Error: {score}")

if __name__ == "__main__":
    test_forensics()