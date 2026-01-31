import sys
import os
# Add the root directory to path so we can import engines
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.consistency import ConsistencyEngine

def test():
    engine = ConsistencyEngine()
    
    # YOU NEED AN IMAGE NAMED 'test.jpg' IN YOUR ROOT FOR THIS TO WORK
    image_path = "test.jpg"
    
    if not os.path.exists(image_path):
        print("❌ Error: Please place a file named 'test.jpg' in the root directory to test.")
        return

    # Test Case 1: Matching
    score1 = engine.get_similarity_score(image_path, "A photo representing the visual content")
    print(f"Test 1 (Matching): {score1}")

    # Test Case 2: Complete Mismatch
    score2 = engine.get_similarity_score(image_path, "A purple elephant eating a taco in space")
    print(f"Test 2 (Mismatch): {score2}")

    if isinstance(score1, float) and score1 > score2:
        print("🚀 Consistency Engine is WORKING CORRECTLY!")
    else:
        print("⚠️ Warning: Scores are suspicious. Check the model or test image.")

if __name__ == "__main__":
    test()