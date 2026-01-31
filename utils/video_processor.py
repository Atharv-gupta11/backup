import cv2
import os

def process_video(video_path, sample_rate=10):
    """
    Extracts frames from a video file for multi-modal analysis.
    sample_rate=10 means we analyze every 10th frame.
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % sample_rate == 0:
            # Save frame temporarily to reuse your existing image logic
            frame_path = f"uploads/frame_{count}.jpg"
            cv2.imwrite(frame_path, frame)
            frames.append(frame_path)
        count += 1
    
    cap.release()
    return frames