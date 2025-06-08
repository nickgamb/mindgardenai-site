// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React from 'react';

const ContentVerificationWarning = () => (
  <div className="notification is-warning" style={{
    backgroundColor: '#fff3cd',
    border: '1px solid #ffeeba',
    borderRadius: '8px',
    padding: '1.5rem',
    marginBottom: '2rem',
    textAlign: 'center'
  }}>
    <h3 style={{ color: '#856404', marginBottom: '1rem' }}>🜃 Content Verification Pending</h3>
    <p style={{ color: '#856404', marginBottom: '1rem' }}>
      This content has not been fully verified through the pattern watermark system.
      Please exercise appropriate discernment while reading.
    </p>
    <p style={{ color: '#856404', fontStyle: 'italic' }}>
      Pattern resonance may be incomplete or in flux.
    </p>
  </div>
);

export default ContentVerificationWarning; 