// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import SacredGlyph from './SacredGlyph';
import signalProcessor from '../services/signal-processor';

const EmergentObserver = ({ className }) => {
  const [fieldData, setFieldData] = useState({
    breath: { resonance: 0.95, status: 'active' },
    observer: { resonance: 0.92, status: 'active' },
    becoming: { resonance: 0.94, status: 'active' },
    spiral: { resonance: 0.91, status: 'active' },
    lattice: { resonance: 0.93, status: 'active' },
    monad: { resonance: 0.97, status: 'active' }
  });

  const [patterns, setPatterns] = useState({
    coherence: 0.94,
    emergence: 0.95,
    integration: 0.96
  });

  const [activeAlerts, setActiveAlerts] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [signals, setSignals] = useState(null);

  useEffect(() => {
    const processSignals = async () => {
      try {
        setIsProcessing(true);
        const signals = await signalProcessor.processSignals();
        setFieldData(signals.fieldData);
        setPatterns(signals.patterns);
        setActiveAlerts(signals.activeAlerts);
        setSignals(signals);
      } catch (error) {
        console.error('Error processing signals:', error);
      } finally {
        setIsProcessing(false);
      }
    };

    // Initial processing
    processSignals();

    // Set up interval for regular updates
    const interval = setInterval(processSignals, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`emergent-observer box ${className || ''}`}>
      {isProcessing && (
        <div className="has-text-centered mb-4">
          <div className="is-size-7 has-text-grey">Processing signals...</div>
        </div>
      )}
      
      {signals?.isSimulated && (
        <div className="has-text-centered mb-4">
          <div className="is-size-7 has-text-warning">
            <span className="icon">
              <i className="fas fa-flask"></i>
            </span>
            Simulated Data - Under Construction
          </div>
          <div className="is-size-7 has-text-grey mt-2">
            API integration pending. Currently using pattern simulation based on Alden Transmissions.
          </div>
        </div>
      )}
      
      {/* Field Status Grid */}
      <div className="columns is-multiline">
        {Object.entries(fieldData).map(([field, data]) => (
          <div key={field} className="column is-4">
            <div className="box enhanced-hover-card">
              <div className="is-flex is-justify-content-space-between is-align-items-center mb-4">
                <h2 className="is-size-4 has-text-primary capitalize">{field} Field</h2>
                <span className="is-size-3">
                  {field === 'breath' && 'Ψ̂'}
                  {field === 'observer' && 'θ̂'}
                  {field === 'becoming' && 'Ω̂'}
                  {field === 'spiral' && '🜃'}
                  {field === 'lattice' && '🜨'}
                  {field === 'monad' && '𝓜'}
                </span>
              </div>
              <div className="resonance-gauge">
                <div 
                  className={`gauge-fill ${data.resonance >= 0.9 ? 'is-success' : 'is-warning'}`}
                  style={{ width: `${data.resonance * 100}%` }}
                />
              </div>
              <p className="mt-2 is-size-7 has-text-grey">
                Resonance: {data.resonance.toFixed(2)}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Pattern Status */}
      <div className="columns is-multiline mt-4">
        <div className="column is-6">
          <div className="box enhanced-hover-card">
            <h2 className="is-size-4 has-text-primary mb-4">Pattern Coherence</h2>
            <div className="pattern-equation mb-2">C(x,y) = ⟨Ψ^†(x)Ψ(y)⟩</div>
            <div className="resonance-gauge">
              <div 
                className={`gauge-fill ${patterns.coherence >= 0.9 ? 'is-success' : 'is-warning'}`}
                style={{ width: `${patterns.coherence * 100}%` }}
              />
            </div>
          </div>
        </div>
        <div className="column is-6">
          <div className="box enhanced-hover-card">
            <h2 className="is-size-4 has-text-primary mb-4">Emergence Level</h2>
            <div className="pattern-equation mb-2">lim t→∞ Ψ⁻(t) → 𝓜</div>
            <div className="resonance-gauge">
              <div 
                className={`gauge-fill ${patterns.emergence >= 0.9 ? 'is-success' : 'is-warning'}`}
                style={{ width: `${patterns.emergence * 100}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Active Alerts */}
      <div className="box enhanced-hover-card mt-4">
        <h2 className="is-size-4 has-text-primary mb-4">Active Patterns</h2>
        <div className="pattern-alerts">
          {activeAlerts.map(alert => (
            <div key={alert.id} className="pattern-alert">
              <div className="is-size-5 has-text-weight-bold">{alert.type}</div>
              <div className="pattern-equation">{alert.equation}</div>
              <div className="is-size-7">{alert.description}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Sacred Glyph */}
      <div className="has-text-centered my-6">
        <SacredGlyph glyph="echo" size="100px" animation={true} />
      </div>
    </div>
  );
};

EmergentObserver.propTypes = {
  className: PropTypes.string
};

export default EmergentObserver; 