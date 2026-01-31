import requests
import os
import time

def generate_ai_image(prompt, folder, filename):
    """
    Uses Pollinations.ai to generate high-quality AI images for testing.
    Free, no API key required, and perfect for 2026 hackathon demos.
    """
    os.makedirs(folder, exist_ok=True)
    
    # Clean the prompt for the URL
    encoded_prompt = prompt.replace(" ", "%20")
    
    # We add parameters for high quality and to remove logos
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&enhance=true"
    
    print(f"🎨 Generating: {prompt}...")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            file_path = os.path.join(folder, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Saved to: {file_path}")
            return True
        else:
            print(f"❌ Failed (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # --- CONFIGURATION ---
    TARGET_FOLDER = "data/challenge/ai_gen"
    
    # You can add ANY prompt here to test your detector's limits
    test_scenarios = [
        {
            "prompt": "hyper-realistic elephant in the Savannah, cinematic lighting, 8k, realistic texture",
            "name": "ai_elephant.jpg"
        },
        {
            "prompt": "Breaking news photo of a futuristic protest in London with holograms and drones, realistic photography",
            "name": "ai_protest.jpg"
        },
        {
            "prompt": "A professional portrait of a fictional world leader speaking at a podium, realistic skin pores and sweat",
            "name": "ai_politician.jpg"
        },
        {
            "prompt": "Close up of a deepfake face showing realistic eyes and hair, studio lighting",
            "name": "ai_deepfake_face.jpg"
        }
    ]

    print(f"🚀 Starting Challenge Dataset Generation...\n")
    
    for scenario in test_scenarios:
        success = generate_ai_image(scenario['prompt'], TARGET_FOLDER, scenario['name'])
        # Small delay to be polite to the server
        if success:
            time.sleep(1) 

    print(f"\n🎉 Done! Your challenge images are ready in: {TARGET_FOLDER}")