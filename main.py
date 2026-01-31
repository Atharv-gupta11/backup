import json
import os
import cv2
import numpy as np
from engines.consistency import ConsistencyEngine
from engines.forensics import ForensicsEngine
from engines.search import SearchEngine
from engines.robustness import RobustnessEngine
from utils.explainer import Explainer

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def analyze_post(image_path, text, use_defense=True):
    # 1. Load Settings and Initialize Engines
    config = load_config()
    t = config['thresholds']
    
    re = RobustnessEngine()
    ce = ConsistencyEngine()
    fe = ForensicsEngine()
    se = SearchEngine()
    ex = Explainer()

    # 2. Check if the file is a video
    is_video = image_path.lower().endswith(('.mp4', '.mov', '.avi'))
    
    if is_video:
        # VIDEO LOGIC: Extract 3 key frames
        cap = cv2.VideoCapture(image_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = [0, total_frames // 2, max(0, total_frames - 1)] if total_frames > 0 else [0]
        
        f_scores = []
        c_scores = []
        
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                temp_path = f"temp_frame_{idx}.jpg"
                cv2.imwrite(temp_path, frame)
                
                # Analyze frame
                f_scores.append(fe.detect_synthetic(temp_path))
                # FIX 1: Updated method name here
                c_scores.append(ce.compute_consistency(temp_path, text))
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        cap.release()
        f_score = max(f_scores) if f_scores else 0.0
        c_score = sum(c_scores) / len(c_scores) if c_scores else 0.0
        analysis_path = image_path 
        search_context = se.check_context(text)
    
    else:
        # IMAGE LOGIC
        analysis_path = re.purify_image(image_path) if use_defense else image_path
        # FIX 2: Updated method name here
        c_score = ce.compute_consistency(analysis_path, text)
        f_score = fe.detect_synthetic(analysis_path)
        search_context = se.check_context(text)

    # 3. ADVANCED DECISION LOGIC
    consistency_fail = c_score < t['consistency_min']
    ai_generated = f_score > t['ai_prob_max']
    is_misinfo = consistency_fail or ai_generated

    # Before sending to explainer, truncate the search results
    short_context = str(search_context)[:800] # Limit to 800 characters

    # 4. Generate Verdict
    explanation = ex.generate_verdict(
        analysis_path, c_score, f_score, short_context, text 
    )

    return {
        "is_misinfo": is_misinfo,
        "explanation": explanation,
        "technical_stats": {
            "consistency": round(c_score, 4),
            "ai_prob": round(f_score, 4),
            "verdict_type": "Synthetic" if ai_generated else "OOC" if consistency_fail else "Clear"
        }
    }
def general_decision_logic(f_score, c_score, search_data, claim):
    # Thresholds (Tuned for 2026 Generalization)
    AI_THRESH = 0.50
    MATCH_THRESH = 0.35

    # Case 1: Synthetic Media (Digital DNA Failure)
    if f_score > AI_THRESH:
        return "RISK", "SYNTHETIC", "System detected artificial pixel patterns typical of AI generation."

    # Case 2: Out-of-Context (Semantic-Context Failure)
    # If image matches the text (c_score is high) but search says it's from a different year/place
    is_ooc = detect_entity_mismatch(claim, search_data) 
    if is_ooc or c_score < MATCH_THRESH:
        return "RISK", "OOC", "Media is likely authentic but contradicts verified context or narrative."

    # Case 3: Authentic
    return "SAFE", "CLEAR", "Media and narrative are semantically consistent and digitally authentic."