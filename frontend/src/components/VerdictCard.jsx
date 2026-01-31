import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react';
import { Radar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
);

const VerdictCard = ({ result }) => {
    const [expanded, setExpanded] = useState(false);

    if (!result) return null;

    const { is_misinfo, technical_stats, explanation } = result;

    // Design Logic
    const theme = is_misinfo
        ? { bg: 'var(--risk-bg)', color: 'var(--risk-red)', icon: AlertTriangle, title: 'HIGH RISK DETECTED' }
        : { bg: 'var(--safe-bg)', color: 'var(--safe-green)', icon: CheckCircle, title: 'LIKELY AUTHENTIC' };

    // Radar Data
    const radarData = {
        labels: ['Digital DNA', 'Semantic Alignment', 'Factual Grounding'],
        datasets: [
            {
                label: 'Confidence Signals',
                data: [
                    technical_stats.ai_prob * 100,
                    technical_stats.consistency * 100,
                    is_misinfo ? 20 : 90 // Heuristic for Factual Grounding based on verdict
                ],
                backgroundColor: is_misinfo ? 'rgba(220, 53, 69, 0.2)' : 'rgba(40, 167, 69, 0.2)',
                borderColor: is_misinfo ? '#dc3545' : '#28a745',
                borderWidth: 2,
            },
        ],
    };

    const radarOptions = {
        scales: {
            r: {
                beginAtZero: true,
                max: 100,
                ticks: { display: false },
                grid: { color: '#e9ecef' }
            }
        },
        plugins: { legend: { display: false } }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            style={{
                background: 'white',
                borderRadius: 'var(--radius-lg)',
                boxShadow: 'var(--shadow-md)',
                overflow: 'hidden'
            }}
        >
            {/* 1. Verdict Header */}
            <div style={{
                padding: '2rem',
                background: theme.bg,
                borderBottom: `1px solid ${is_misinfo ? '#f5c6cb' : '#c3e6cb'}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <theme.icon size={32} color={theme.color} />
                    <div>
                        <h2 style={{ margin: 0, color: theme.color, fontSize: '1.5rem' }}>{theme.title}</h2>
                        <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                            Confidence Score: <b>{is_misinfo ? (technical_stats.ai_prob * 100).toFixed(1) : (technical_stats.consistency * 100).toFixed(1)}%</b>
                        </p>
                    </div>
                </div>
            </div>

            {/* 2. Visual Data Section */}
            <div style={{ padding: '2rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                <div>
                    <h4 style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>Forensic Signal Radar</h4>
                    <div style={{ height: '200px' }}>
                        <Radar data={radarData} options={radarOptions} />
                    </div>
                </div>

                <div>
                    <h4 style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>Analysis Pipeline</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {['Ingestion', 'Purification', 'Sensor Analysis', 'Logic Fusion'].map((step, i) => (
                            <div key={step} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-black)' }}></div>
                                <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>{step}</span>
                                {i === 3 && <span style={{ marginLeft: 'auto', fontSize: '0.8rem', color: 'var(--safe-green)' }}>COMPLETED</span>}
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* 3. Deep Dive Accordion */}
            <div style={{ borderTop: '1px solid var(--border-light)' }}>
                <button
                    onClick={() => setExpanded(!expanded)}
                    style={{
                        width: '100%',
                        padding: '1.5rem 2rem',
                        background: 'none',
                        border: 'none',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        cursor: 'pointer',
                        fontWeight: 600
                    }}
                >
                    <span>📄 View Evidence Report</span>
                    {expanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </button>

                {expanded && (
                    <motion.div
                        initial={{ height: 0 }}
                        animate={{ height: 'auto' }}
                        style={{ padding: '0 2rem 2rem', color: '#444', lineHeight: '1.6', overflow: 'hidden' }}
                    >
                        <div style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: '8px' }}>
                            {explanation.split('\n').map((line, i) => (
                                <p key={i} style={{ marginBottom: '0.5rem' }}>{line}</p>
                            ))}
                        </div>
                    </motion.div>
                )}
            </div>
        </motion.div>
    );
};

export default VerdictCard;
