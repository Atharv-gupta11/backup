import cv2
import os

def truncate_text(text, max_length=70):
    """Prevents CLIP token overflow errors."""
    return text[:max_length] if len(text) > max_length else text

def extract_frames(video_path, output_folder, interval=1):
    """Extracts frames from video to analyze as images."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    success, image = vidcap.read()
    count = 0
    saved_count = 0
    
    while success:
        # Save frame at specific intervals (e.g., every 1 second)
        if count % int(fps * interval) == 0:
            cv2.imwrite(f"{output_folder}/frame_{saved_count}.jpg", image)
            saved_count += 1
        success, image = vidcap.read()
        count += 1
    return output_folder