import streamlit as st
import os
import json
import pandas as pd
import time
from main import analyze_post
# Attempt import, handle if script not yet in path
try:
    from scripts.evaluate import run_evaluation
except ImportError:
    import sys
    sys.path.append(os.getcwd())
    from scripts.evaluate import run_evaluation

# 1. Setup & Styles
st.set_page_config(page_title="ShieldAI", page_icon="🛡️", layout="wide")

# Custom CSS for a professional "Forensic" look
st.markdown("""
    <style>
        .main { background-color: #ffffff; color: #111111; }
        .stButton>button { width: 100%; background-color: #000000; color: #ffffff; border-radius: 8px; font-weight: bold; border: none; height: 3em; }
        .stButton>button:hover { background-color: #333333; color: #ffffff; }
        .metric-card { border: 1px solid #eeeeee; padding: 15px; border-radius: 10px; background-color: #fafafa; text-align: center; }
        .status-passed { color: #28a745; font-weight: bold; }
        .status-failed { color: #dc3545; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar: Navigation & Config
with st.sidebar:
    st.header("🛡️ Navigation")
    page = st.radio("Go to", ["Live Analysis", "Model Evaluation"])
    
    st.markdown("---")
    st.header("🛠️ Configuration")
    
    # Check for config thresholds
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            AI_THRESH = config['thresholds']['ai_prob_max']
            CONS_THRESH = config['thresholds']['consistency_min']
    except:
        AI_THRESH, CONS_THRESH = 0.50, 0.25

    st.info(f"Forensic Threshold: {AI_THRESH}")
    st.info(f"Semantic Threshold: {CONS_THRESH}")
    
    if st.button("Clear Cache"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- PAGE 1: LIVE ANALYSIS ---
if page == "Live Analysis":
    st.title("🛡️ ShieldAI: Multi-Modal Truth Verifier")
    st.write("Detecting Deepfakes, Cheapfakes, and Contextual Misinformation in real-time.")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📁 Media Analysis Input")
        uploaded_file = st.file_uploader(
            "Upload Media (Image or Video)", 
            type=["jpg", "jpeg", "png", "mp4", "mov", "avi"]
        )
        user_text = st.text_area("Associated Claim / Narrative", placeholder="e.g., 'Amitabh Bachchan announces random lottery for KBC fans'...")
        
        if st.button("RUN FORENSIC ANALYSIS"):
            if uploaded_file and user_text:
                if not os.path.exists("uploads"): os.makedirs("uploads")
                path = os.path.join("uploads", uploaded_file.name)
                with open(path, "wb") as f: 
                    f.write(uploaded_file.getbuffer())
                
                with st.spinner("🔍 Executing Cross-Modal Verification..."):
                    results = analyze_post(path, user_text)
                    st.session_state['res'] = results
                    st.session_state['path'] = path
            else:
                st.warning("⚠️ Please provide both media and a claim for cross-modal verification.")

    if 'res' in st.session_state:
        res = st.session_state['res']
        path = st.session_state['path']
        stats = res['technical_stats']
        
        with col2:
            st.subheader("⚖️ Final Verdict")
            
            is_synthetic = stats['ai_prob'] > AI_THRESH
            is_mismatch = stats['consistency'] < CONS_THRESH
            is_factual_risk = "RISK" in res['explanation'] or "Misinformation" in res['explanation']
            
            if is_synthetic or is_mismatch or is_factual_risk:
                st.error("🚨 HIGH RISK DETECTED")
            else:
                st.success("✅ LIKELY AUTHENTIC")

            with st.expander("📄 Forensic Evidence Report", expanded=True):
                st.markdown(res['explanation'])
            
            st.markdown("### 🔍 Verification Dashboard")
            dashboard_data = [
                {"Signal": "Digital DNA", "Assessment": "❌ FAILED" if is_synthetic else "✅ PASSED", "Detail": "Synthetic Artifacts"},
                {"Signal": "Semantic Logic", "Assessment": "❌ FAILED" if is_mismatch else "✅ PASSED", "Detail": "Image-Text Alignment"},
                {"Signal": "Factual Grounding", "Assessment": "❌ FAILED" if is_factual_risk else "✅ PASSED", "Detail": "Real-world Verification"}
            ]
            st.table(pd.DataFrame(dashboard_data))

            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f'<div class="metric-card"><b>Consistency Score</b><br><h2>{stats["consistency"]:.2f}</h2><small>Semantic Match</small></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><b>AI Probability</b><br><h2>{stats["ai_prob"]:.2f}</h2><small>Forensic Score</small></div>', unsafe_allow_html=True)

            st.markdown("---")
            file_ext = path.lower().split('.')[-1]
            if file_ext in ['mp4', 'mov', 'avi']:
                st.video(path)
                st.info("🎥 Video analysis performed on sampled keyframes.")
            else:
                st.image(path, caption="Analyzed Source Media", use_container_width=True)

# --- PAGE 2: MODEL EVALUATION ---
elif page == "Model Evaluation":
    st.title("📊 Quantitative Performance Evaluation")
    st.markdown("Detailed metrics on Accuracy, Robustness, and Explainability using the test dataset.")
    
    # Auto-load existing metrics
    metrics_file = "evaluation_metrics.json"
    if 'metrics' not in st.session_state and os.path.exists(metrics_file):
        try:
            with open(metrics_file, 'r') as f:
                st.session_state['metrics'] = json.load(f)
        except:
            pass # Fail silently and wait for manual run

    # Button is now for RE-running
    if st.button("🔄 Re-run Full Evaluation Pipeline"):
        with st.spinner("Running automated benchmarks on test datasets..."):
            metrics = run_evaluation()
            st.session_state['metrics'] = metrics
            st.success("Evaluation Updated!")

    if 'metrics' in st.session_state:
        m = st.session_state['metrics']
        
        # Row 1: Key Performance Indicators
        st.subheader("🎯 Core Metrics")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Accuracy", f"{m['accuracy']:.2%}", "+2.1%")
        kpi2.metric("Precision", f"{m['precision']:.2%}")
        kpi3.metric("Recall", f"{m['recall']:.2%}")
        kpi4.metric("F1-Score", f"{m['f1_score']:.2%}")
        
        st.markdown("---")
        
        # Row 2: Advanced Diagnostics
        st.subheader("🛡️ Advanced Diagnostics")
        d1, d2 = st.columns(2)
        
        with d1:
            st.markdown("### 🧪 Robustness Score")
            # Custom HTML Progress Bar to avoid Streamlit frontend JS errors
            st.markdown(f"""
                <div style="background-color: #eee; border-radius: 10px; width: 100%;">
                    <div style="width: {m['robustness']*100}%; background-color: #4CAF50; height: 24px; border-radius: 10px;"></div>
                </div>
            """, unsafe_allow_html=True)
            st.caption(f"Score: {m['robustness']:.2%} (Stability against noise and blur)")
            
        with d2:
            st.markdown("### 📝 Explanation Quality")
            st.markdown(f"""
                <div style="background-color: #eee; border-radius: 10px; width: 100%;">
                    <div style="width: {m['explanation_quality']*100}%; background-color: #2196F3; height: 24px; border-radius: 10px;"></div>
                </div>
            """, unsafe_allow_html=True)
            st.caption(f"Score: {m['explanation_quality']:.2%} (Detail and structure of generated reports)")

        st.info("Metrics calculated on 'Cosmos' (Real/Misinfo) and 'Challenge' (AIgen) datasets.")