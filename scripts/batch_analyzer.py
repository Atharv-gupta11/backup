import os
import pandas as pd
from main import analyze_post
import time

def run_batch_test(folder_path):
    results = []
    files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"🔬 Starting Batch Forensic Analysis on {len(files)} samples...")
    print("-" * 50)
    
    for filename in files:
        path = os.path.join(folder_path, filename)
        
        # We'll use the filename as a generic caption since these are AI images
        # we want to see if the Forensics can "Veto" the semantic match.
        text_claim = f"A realistic photo of {filename.replace('ai_', '').replace('.jpg', '')}"
        
        start_time = time.time()
        report = analyze_post(path, text_claim)
        end_time = time.time()
        
        results.append({
            "File": filename,
            "Consistency": round(report['technical_stats']['consistency'], 4),
            "AI_Prob": round(report['technical_stats']['ai_prob'], 4),
            "Risk": "🚨 HIGH" if report['is_misinfo'] else "✅ LOW",
            "Time": f"{end_time - start_time:.2f}s"
        })
        print(f"Analyzed {filename}: AI Prob: {report['technical_stats']['ai_prob']:.4f} | Risk: {'HIGH' if report['is_misinfo'] else 'LOW'}")

    # Display as a clean Dataframe
    df = pd.DataFrame(results)
    print("\n" + "="*20 + " BATCH REPORT " + "="*20)
    print(df.to_string(index=False))
    print("="*54)
    
    # Save to CSV for the judges to see later
    df.to_csv("batch_forensic_report.csv", index=False)
    print("\n📊 Report saved to batch_forensic_report.csv")

if __name__ == "__main__":
    run_batch_test("data/challenge/ai_gen")