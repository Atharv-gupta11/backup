import React from 'react';
import { ShieldCheck, Activity, Cpu } from 'lucide-react';

const Header = () => {
  return (
    <header style={{ 
      borderBottom: '1px solid var(--border-light)', 
      padding: '1.25rem 0',
      marginBottom: '2rem'
    }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <ShieldCheck size={32} color="var(--accent-black)" />
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, margin: 0 }}>ShieldAI</h1>
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.9rem', color: 'var(--safe-green)' }}>
            <Activity size={16} />
            <span style={{ fontWeight: 600 }}>API: Online</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            <Cpu size={16} />
            <span>Model: v2.5 (Groq/Llama 3.3)</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
