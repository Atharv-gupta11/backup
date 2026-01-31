import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart2, RefreshCw, Activity, Target, Zap, Shield } from 'lucide-react';

const KPICard = ({ title, value, icon: Icon, color }) => (
    <div style={{
        background: 'white',
        padding: '1.5rem',
        borderRadius: 'var(--radius-md)',
        boxShadow: 'var(--shadow-sm)',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem'
    }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            <Icon size={18} color={color} />
            <span>{title}</span>
        </div>
        <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            {(value * 100).toFixed(1)}%
        </div>
    </div>
);

const ProgressBar = ({ label, value, color, desc }) => (
    <div style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontWeight: 600 }}>{label}</span>
            <span style={{ fontWeight: 700, color: color }}>{(value * 100).toFixed(1)}%</span>
        </div>
        <div style={{ width: '100%', height: '12px', background: 'var(--bg-secondary)', borderRadius: '6px', overflow: 'hidden' }}>
            <div style={{ width: `${value * 100}%`, height: '100%', background: color, borderRadius: '6px', transition: 'width 1s ease-out' }}></div>
        </div>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>{desc}</p>
    </div>
);

const EvaluationView = () => {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Load cache on mount
        axios.get('http://localhost:8000/evaluate/cache')
            .then(res => { if (res.data) setMetrics(res.data); })
            .catch(err => console.error("Cache load failed", err));
    }, []);

    const runEvaluation = async () => {
        setLoading(true);
        try {
            const res = await axios.post('http://localhost:8000/evaluate');
            setMetrics(res.data);
        } catch (err) {
            alert("Evaluation failed. Check console.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (!metrics && !loading) {
        return (
            <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-secondary)' }}>
                <BarChart2 size={48} style={{ marginBottom: '1rem', opacity: 0.2 }} />
                <p>No metrics found. Run an evaluation to benchmark the model.</p>
                <button className="btn-primary" onClick={runEvaluation} style={{ marginTop: '1rem' }}>
                    Run Benchmark
                </button>
            </div>
        );
    }

    return (
        <div className="animate-fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: 700, margin: 0 }}>Model Performance</h2>
                    <p style={{ color: 'var(--text-secondary)', marginTop: '0.25rem' }}>Benchmarking on 'Cosmos' & 'Challenge' datasets</p>
                </div>
                <button
                    onClick={runEvaluation}
                    disabled={loading}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '0.6rem 1.2rem',
                        background: 'white',
                        border: '1px solid var(--text-primary)',
                        borderRadius: '8px',
                        cursor: loading ? 'wait' : 'pointer',
                        fontWeight: 600
                    }}
                >
                    <RefreshCw size={18} className={loading ? "spin" : ""} />
                    {loading ? "Benchmarking..." : "Re-run Evaluation"}
                </button>
            </div>

            {metrics && (
                <>
                    {/* KPI Grid */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2.5rem' }}>
                        <KPICard title="Accuracy" value={metrics.accuracy} icon={Target} color="#2196F3" />
                        <KPICard title="Precision" value={metrics.precision} icon={Activity} color="#9C27B0" />
                        <KPICard title="Recall" value={metrics.recall} icon={Zap} color="#FF9800" />
                        <KPICard title="F1 Score" value={metrics.f1_score} icon={Shield} color="#4CAF50" />
                    </div>

                    {/* Advanced Stats */}
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                        <div style={{ background: 'white', padding: '2rem', borderRadius: 'var(--radius-lg)', boxShadow: 'var(--shadow-sm)' }}>
                            <h3 style={{ fontSize: '1.1rem', marginBottom: '1.5rem' }}>🛡️ Robustness Analysis</h3>
                            <ProgressBar
                                label="Stability Score"
                                value={metrics.robustness}
                                color="#4CAF50"
                                desc="Resistance to noise, blur, and compression artifacts."
                            />
                        </div>

                        <div style={{ background: 'white', padding: '2rem', borderRadius: 'var(--radius-lg)', boxShadow: 'var(--shadow-sm)' }}>
                            <h3 style={{ fontSize: '1.1rem', marginBottom: '1.5rem' }}>📝 Explainability Quality</h3>
                            <ProgressBar
                                label="Report Quality"
                                value={metrics.explanation_quality}
                                color="#2196F3"
                                desc="Completeness and structural integrity of generated forensic reports."
                            />
                        </div>
                    </div>
                </>
            )}

            <style>{`
        .spin { animation: spin 1s linear infinite; }
        @keyframes spin { 100% { transform: rotate(360deg); } }
      `}</style>
        </div>
    );
};

export default EvaluationView;
