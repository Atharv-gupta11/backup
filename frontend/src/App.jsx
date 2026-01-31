import React, { useState } from 'react';
import axios from 'axios';
import { UploadCloud, Search, AlertCircle, BarChart2, Layout } from 'lucide-react';
import Header from './components/Header';
import VerdictCard from './components/VerdictCard';
import EvaluationView from './components/EvaluationView';

function App() {
  const [view, setView] = useState('analysis'); // 'analysis' or 'evaluation'

  // Analysis State
  const [file, setFile] = useState(null);
  const [claim, setClaim] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [feedbackSent, setFeedbackSent] = useState(false);

  const handleAnalysis = async () => {
    if (!file || !claim) {
      alert("Please upload an image and enter a claim.");
      return;
    }

    setLoading(true);
    setResult(null);
    setError(null);
    setFeedbackSent(false);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('claim', claim);

    try {
      const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Analysis Failed. Ensure the Backend API is running.");
    } finally {
      setLoading(false);
    }
  };

  const sendFeedback = async (type) => {
    if (!file) return;
    try {
      const formData = new FormData();
      formData.append('file_name', file.name);
      formData.append('feedback_type', type);
      await axios.post('http://localhost:8000/feedback', formData);
      setFeedbackSent(true);
    } catch (e) {
      console.error("Feedback failed", e);
    }
  };

  return (
    <div style={{ minHeight: '100vh', paddingBottom: '4rem' }}>
      <Header />

      {/* Navigation Tabs */}
      <div className="container" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'inline-flex', background: 'var(--bg-secondary)', padding: '4px', borderRadius: '8px' }}>
          <button
            onClick={() => setView('analysis')}
            style={{
              padding: '0.6rem 1.2rem',
              border: 'none',
              background: view === 'analysis' ? 'white' : 'transparent',
              borderRadius: '6px',
              fontWeight: 600,
              color: view === 'analysis' ? 'var(--text-primary)' : 'var(--text-secondary)',
              boxShadow: view === 'analysis' ? 'var(--shadow-sm)' : 'none',
              cursor: 'pointer',
              display: 'flex', alignItems: 'center', gap: '8px',
              transition: 'all 0.2s'
            }}
          >
            <Layout size={18} /> Live Analysis
          </button>
          <button
            onClick={() => setView('evaluation')}
            style={{
              padding: '0.6rem 1.2rem',
              border: 'none',
              background: view === 'evaluation' ? 'white' : 'transparent',
              borderRadius: '6px',
              fontWeight: 600,
              color: view === 'evaluation' ? 'var(--text-primary)' : 'var(--text-secondary)',
              boxShadow: view === 'evaluation' ? 'var(--shadow-sm)' : 'none',
              cursor: 'pointer',
              display: 'flex', alignItems: 'center', gap: '8px',
              transition: 'all 0.2s'
            }}
          >
            <BarChart2 size={18} /> Model Evaluation
          </button>
        </div>
      </div>

      <main className="container">
        {view === 'analysis' ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(350px, 40%) 1fr', gap: '3rem' }}>

            {/* LEFT COLUMN: Input Zone */}
            <section>
              <div style={{ background: 'white', padding: '2rem', borderRadius: 'var(--radius-lg)', boxShadow: 'var(--shadow-sm)' }}>
                <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem' }}>1. Upload Evidence</h2>

                {/* Drag & Drop Area */}
                <div
                  style={{
                    border: '2px dashed var(--border-light)',
                    borderRadius: 'var(--radius-md)',
                    padding: '3rem 1rem',
                    textAlign: 'center',
                    cursor: 'pointer',
                    background: 'var(--bg-secondary)',
                    marginBottom: '1.5rem',
                    transition: 'border-color 0.2s'
                  }}
                  onClick={() => document.getElementById('fileInput').click()}
                >
                  <input
                    id="fileInput"
                    type="file"
                    accept="image/*,video/*"
                    hidden
                    onChange={(e) => setFile(e.target.files[0])}
                  />
                  <UploadCloud size={48} color="var(--text-secondary)" style={{ marginBottom: '1rem' }} />
                  <p style={{ margin: 0, fontWeight: 500 }}>
                    {file ? file.name : "Click to Upload Media"}
                  </p>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                    Supports JPG, PNG, MP4
                  </p>
                </div>

                {/* Text Input */}
                <div style={{ marginBottom: '2rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.9rem' }}>
                    Associated Claim
                  </label>
                  <div style={{ position: 'relative' }}>
                    <Search size={20} style={{ position: 'absolute', left: '12px', top: '14px', color: 'var(--text-secondary)' }} />
                    <input
                      type="text"
                      className="input-field"
                      style={{ paddingLeft: '40px' }}
                      placeholder="e.g. 'Fire in the city today...'"
                      value={claim}
                      onChange={(e) => setClaim(e.target.value)}
                    />
                  </div>
                </div>

                {/* Action Button */}
                <button
                  className="btn-primary"
                  style={{ width: '100%' }}
                  onClick={handleAnalysis}
                  disabled={loading}
                >
                  {loading ? "Analyzing..." : "Execute Forensic Analysis"}
                </button>

                {error && (
                  <div style={{ marginTop: '1rem', color: 'var(--risk-red)', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem' }}>
                    <AlertCircle size={16} />
                    {error}
                  </div>
                )}
              </div>

              {/* Feedback Zone (Deliverable #7) */}
              {result && (
                <div style={{ marginTop: '2rem', padding: '1.5rem', background: 'white', borderRadius: 'var(--radius-lg)', boxShadow: 'var(--shadow-sm)' }}>
                  <h3 style={{ fontSize: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    🛠️ Help Improve ShieldAI
                  </h3>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                    Flag incorrect results to finetune our model.
                  </p>

                  {!feedbackSent ? (
                    <div style={{ display: 'flex', gap: '1rem' }}>
                      <button
                        onClick={() => sendFeedback('false_positive')}
                        style={{ flex: 1, padding: '0.5rem', background: 'none', border: '1px solid var(--border-light)', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem' }}
                      >
                        🚩 False Positive
                      </button>
                      <button
                        onClick={() => sendFeedback('false_negative')}
                        style={{ flex: 1, padding: '0.5rem', background: 'none', border: '1px solid var(--border-light)', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem' }}
                      >
                        ⚠️ False Negative
                      </button>
                    </div>
                  ) : (
                    <div style={{ padding: '0.75rem', background: 'var(--safe-bg)', color: 'var(--safe-green)', borderRadius: '6px', fontSize: '0.9rem', textAlign: 'center' }}>
                      ✅ Feedback Logged. Thank you!
                    </div>
                  )}
                </div>
              )}
            </section>

            {/* RIGHT COLUMN: Results Zone */}
            <section>
              {result ? (
                <VerdictCard result={result} />
              ) : (
                <div style={{
                  height: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--text-secondary)',
                  border: '2px dashed var(--border-light)',
                  borderRadius: 'var(--radius-lg)',
                  minHeight: '400px'
                }}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.3 }}>🛡️</div>
                    <p>Ready to analyze. Upload media to begin.</p>
                  </div>
                </div>
              )}
            </section>
          </div>
        ) : (
          <EvaluationView />
        )}
      </main>
    </div>
  );
}

export default App;
