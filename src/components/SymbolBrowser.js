// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useState, useEffect, useMemo, useRef } from "react";
import symbolData from "../data/symbol_tags_organized.json";
import { motion, AnimatePresence } from 'framer-motion';
import { Line } from 'react-chartjs-2';

const SymbolBrowser = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [expandedSymbol, setExpandedSymbol] = useState(null);
  const [filteredSymbols, setFilteredSymbols] = useState([]);
  const [viewMode, setViewMode] = useState("grid"); // grid, resonance, pattern, graph, timeline, cultural, mathematical
  const [selectedPattern, setSelectedPattern] = useState(null);
  const [resonanceDepth, setResonanceDepth] = useState(2);
  const [activeResonance, setActiveResonance] = useState(null);
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [selectedSequence, setSelectedSequence] = useState([]);
  const [evolutionPhase, setEvolutionPhase] = useState("all");
  const [selectedCulture, setSelectedCulture] = useState("all");
  const [culturalComparison, setCulturalComparison] = useState(null);
  const [mathematicalView, setMathematicalView] = useState("field"); // field, resonance, pattern
  const [breathParameters, setBreathParameters] = useState({
    amplitude: 1,
    phase: 0,
    frequency: 1,
    resonance: 0.5
  });

  // Add layout state for graph visualization
  const [layout, setLayout] = useState('force');
  
  // Add refs for SVG manipulation
  const svgRef = useRef(null);
  const gRef = useRef(null);

  // Add mobile detection
  const [isMobile, setIsMobile] = useState(false);

  // Get unique categories from the data
  const categories = ["all", ...Object.keys(symbolData)];

  // Get unique cultures from the data
  const cultures = useMemo(() => {
    const cultureSet = new Set();
    Object.values(symbolData).forEach(category => {
      Object.values(category).forEach(symbol => {
        if (symbol && symbol.cross_cultural) {
          Object.keys(symbol.cross_cultural).forEach(culture => {
            cultureSet.add(culture);
          });
        }
      });
    });
    return ["all", ...Array.from(cultureSet).sort()];
  }, []);

  // Compute resonance patterns and relationships
  const { resonancePatterns, symbolRelationships } = useMemo(() => {
    const patterns = new Map();
    const relationships = new Map();

    Object.entries(symbolData).forEach(([category, symbols]) => {
      Object.entries(symbols).forEach(([symbol, data]) => {
        if (data.resonance_field) {
          const primary = data.resonance_field.primary;
          if (!patterns.has(primary)) {
            patterns.set(primary, []);
          }
          patterns.get(primary).push({ symbol, category, ...data });

          // Build relationships
          if (!relationships.has(symbol)) {
            relationships.set(symbol, new Set());
          }
          data.resonance_field.secondary.forEach(res => {
            relationships.get(symbol).add(res);
          });
        }
      });
    });

    return { resonancePatterns: patterns, symbolRelationships: relationships };
  }, []);

  // Generate graph data for visualization
  useEffect(() => {
    if (viewMode === "graph") {
      const nodes = [];
      const links = [];
      const nodeMap = new Map();

      Object.entries(symbolData).forEach(([category, symbols]) => {
        Object.entries(symbols).forEach(([symbol, data]) => {
          if (!nodeMap.has(symbol)) {
            nodeMap.set(symbol, {
              id: symbol,
              category,
              ...data
            });
            nodes.push(nodeMap.get(symbol));
          }

          if (data.resonance_field) {
            data.resonance_field.secondary.forEach(res => {
              if (!nodeMap.has(res)) {
                nodeMap.set(res, {
                  id: res,
                  category: "resonance",
                  isResonance: true
                });
                nodes.push(nodeMap.get(res));
              }
              links.push({
                source: symbol,
                target: res,
                value: 1
              });
            });
          }
        });
      });

      setGraphData({ nodes, links });
    }
  }, [viewMode]);

  // Filter symbols based on search term and category
  useEffect(() => {
    let filtered = [];
    Object.entries(symbolData).forEach(([category, symbols]) => {
      if (selectedCategory === "all" || selectedCategory === category) {
        Object.entries(symbols).forEach(([symbol, data]) => {
          if (
            data.meaning.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (data.synonyms && data.synonyms.some(syn => syn.toLowerCase().includes(searchTerm.toLowerCase()))) ||
            (data.cross_cultural && Object.values(data.cross_cultural).some(val => val.toLowerCase().includes(searchTerm.toLowerCase())))
          ) {
            filtered.push({ symbol, category, ...data });
          }
        });
      }
    });
    setFilteredSymbols(filtered);
  }, [searchTerm, selectedCategory]);

  // Get category color
  const getCategoryColor = (category) => {
    const colors = {
      elemental_core: "#7035CC",
      consciousness_patterns: "#00B4D8",
      technical_primitives: "#2EC4B6",
      resonance_fields: "#FF9F1C",
      all: "#7035CC"
    };
    return colors[category] || "#7035CC";
  };

  // Get category icon
  const getCategoryIcon = (category) => {
    const icons = {
      elemental_core: "🜂",
      consciousness_patterns: "🜄",
      technical_primitives: "🜃",
      resonance_fields: "🜏",
      all: "🜂"
    };
    return icons[category] || "🜂";
  };

  // Adjust graph settings for mobile
  const getGraphConfig = () => ({
    nodeLabel: "id",
    nodeColor: node => getCategoryColor(node.category),
    nodeRelSize: isMobile ? 4 : 6,
    linkColor: () => "rgba(112, 53, 204, 0.2)",
    linkWidth: isMobile ? 0.5 : 1,
    linkDirectionalParticles: isMobile ? 1 : 2,
    linkDirectionalParticleSpeed: 0.005,
    onNodeClick: (node) => {
      setExpandedSymbol(node.id);
    },
    // Mobile-specific graph settings
    ...(isMobile && {
      d3AlphaDecay: 0.02,
      d3VelocityDecay: 0.1,
      warmupTicks: 50,
      cooldownTicks: 0,
      cooldownTime: 0
    })
  });

  // Handle node click in graph view
  const handleNodeClick = (node) => {
    setExpandedSymbol(node.id);
  };

  // Render graph visualization
  const renderGraphView = () => {
    if (!graphData || !graphData.nodes || !graphData.links) {
      return <div className="has-text-centered has-text-danger">Graph data unavailable.</div>;
    }
    const { nodes, links } = graphData;
    
    return (
      <motion.div 
        className="graph-container"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="graph-controls">
          <button 
            className={`control-button ${layout === 'force' ? 'active' : ''}`}
            onClick={() => setLayout('force')}
          >
            Force Layout
          </button>
          <button 
            className={`control-button ${layout === 'radial' ? 'active' : ''}`}
            onClick={() => setLayout('radial')}
          >
            Radial Layout
          </button>
          <button 
            className={`control-button ${layout === 'hierarchical' ? 'active' : ''}`}
            onClick={() => setLayout('hierarchical')}
          >
            Hierarchical
          </button>
        </div>

        <svg
          ref={svgRef}
          width="100%"
          height="600"
          style={{ background: 'transparent' }}
        >
          <g ref={gRef}>
            {/* Edges */}
            {links.map((link, i) => (
              <motion.path
                key={`edge-${i}`}
                className="graph-edge"
                d={link.path}
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 1 }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
              />
            ))}
            
            {/* Nodes */}
            {nodes.map((node, i) => (
              <motion.g
                key={`node-${i}`}
                className="graph-node"
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.3, delay: i * 0.1 }}
                onClick={() => handleNodeClick(node)}
              >
                <circle r={node.radius} />
                <text
                  dy=".3em"
                  textAnchor="middle"
                  style={{ pointerEvents: 'none' }}
                >
                  {node.symbol || node.id}
                </text>
              </motion.g>
            ))}
          </g>
        </svg>

        <div className="graph-legend">
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: $purple70 }}></div>
            <span className="legend-label">Symbol</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: $purple50 }}></div>
            <span className="legend-label">Selected</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: 'rgba($purple50, 0.3)' }}></div>
            <span className="legend-label">Connection</span>
          </div>
        </div>
      </motion.div>
    );
  };

  // Render resonance visualization
  const renderResonanceView = () => {
    if (!selectedPattern) return null;

    const patternSymbols = resonancePatterns.get(selectedPattern) || [];
    const centerSymbol = patternSymbols[0];

    return (
      <motion.div 
        className="resonance-view"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="resonance-center mb-6">
          <motion.div 
            className="box has-text-centered"
            style={{ 
              border: `2px solid ${getCategoryColor(centerSymbol.category)}`,
              background: `linear-gradient(135deg, ${getCategoryColor(centerSymbol.category)}22, ${getCategoryColor(centerSymbol.category)}11)`
            }}
            whileHover={{ scale: 1.02 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <div className="symbol-background"><span className="symbol-display is-size-1">{centerSymbol.symbol}</span></div>
            <h3 className="title is-4 mt-2">{centerSymbol.meaning}</h3>
            <p className="subtitle is-6">{centerSymbol.resonance_field.primary}</p>
          </motion.div>
        </div>

        <div className="resonance-connections">
          <div className="columns is-multiline">
            {patternSymbols.slice(1).map((symbol, index) => (
              <motion.div 
                key={symbol.symbol} 
                className="column is-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <motion.div 
                  className="box enhanced-hover-card"
                  style={{
                    borderLeft: `4px solid ${getCategoryColor(symbol.category)}`,
                    cursor: 'pointer',
                    transform: `rotate(${index * 5}deg)`,
                  }}
                  whileHover={{ 
                    scale: 1.05,
                    rotate: index * 5 + 5,
                    transition: { type: "spring", stiffness: 300 }
                  }}
                  onClick={() => setExpandedSymbol(expandedSymbol === symbol.symbol ? null : symbol.symbol)}
                >
                  <div className="content">
                    <div className="symbol-background"><span className="symbol-display is-size-2">{symbol.symbol}</span></div>
                    <h4 className="title is-5 mt-2">{symbol.meaning}</h4>
                    <AnimatePresence>
                      {expandedSymbol === symbol.symbol && (
                        <motion.div 
                          className="mt-4"
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: "auto" }}
                          exit={{ opacity: 0, height: 0 }}
                        >
                          <div className="tags">
                            {symbol.resonance_field.secondary.map(res => (
                              <span key={res} className="tag is-light">{res}</span>
                            ))}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </motion.div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    );
  };

  // Render pattern recognition view
  const renderPatternView = () => {
    return (
      <motion.div 
        className="pattern-view"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="columns is-multiline">
          {Array.from(resonancePatterns.entries()).map(([pattern, symbols], index) => (
            <motion.div 
              key={pattern} 
              className="column is-6"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <motion.div 
                className="box pattern-card"
                style={{
                  borderLeft: `4px solid ${getCategoryColor(symbols[0].category)}`,
                  cursor: 'pointer'
                }}
                whileHover={{ scale: 1.02 }}
                onClick={() => setSelectedPattern(pattern)}
              >
                <h3 className="title is-4">{pattern}</h3>
                <div className="tags mb-2">
                  {symbols.slice(0, 3).map(s => (
                    <span key={s.symbol} className="tag" style={{ 
                      backgroundColor: getCategoryColor(s.category),
                      color: 'white'
                    }}>
                      {s.symbol}
                    </span>
                  ))}
                  {symbols.length > 3 && (
                    <span className="tag is-light">+{symbols.length - 3} more</span>
                  )}
                </div>
                <p className="is-size-7 has-text-grey">
                  {symbols.length} symbols in resonance
                </p>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    );
  };

  // Render symbol evolution timeline
  const renderTimelineView = () => {
    const phases = ["foundation", "emergence", "integration", "transcendence"];
    
    return (
      <div className="timeline-view">
        <div className="timeline-controls mb-6">
          <div className="tabs is-boxed">
            <ul>
              {phases.map(phase => (
                <li key={phase} className={evolutionPhase === phase ? "is-active" : ""}>
                  <a onClick={() => setEvolutionPhase(phase)}>
                    <span className="icon">
                      <i className={`fas fa-${phase === "foundation" ? "seedling" : 
                        phase === "emergence" ? "leaf" : 
                        phase === "integration" ? "tree" : "star"}`}></i>
                    </span>
                    <span>{phase.charAt(0).toUpperCase() + phase.slice(1)}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="timeline-content">
          <div className="columns is-multiline">
            {filteredSymbols
              .filter(symbol => evolutionPhase === "all" || symbol.evolution_phase === evolutionPhase)
              .map((symbol, index) => (
                <motion.div 
                  key={symbol.symbol} 
                  className="column is-4"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <motion.div 
                    className="box evolution-card"
                    style={{
                      borderLeft: `4px solid ${getCategoryColor(symbol.category)}`,
                      cursor: 'pointer'
                    }}
                    whileHover={{ scale: 1.02 }}
                    onClick={() => setExpandedSymbol(expandedSymbol === symbol.symbol ? null : symbol.symbol)}
                  >
                    <div className="content">
                      <div className="symbol-background"><span className="symbol-display is-size-2">{symbol.symbol}</span></div>
                      <h4 className="title is-5 mt-2">{symbol.meaning}</h4>
                      <p className="subtitle is-6">{symbol.evolution_phase}</p>
                      <AnimatePresence>
                        {expandedSymbol === symbol.symbol && (
                          <motion.div 
                            className="mt-4"
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                            exit={{ opacity: 0, height: 0 }}
                          >
                            <div className="evolution-details">
                              <p><strong>Foundation:</strong> {symbol.evolution_details?.foundation}</p>
                              <p><strong>Emergence:</strong> {symbol.evolution_details?.emergence}</p>
                              <p><strong>Integration:</strong> {symbol.evolution_details?.integration}</p>
                              <p><strong>Transcendence:</strong> {symbol.evolution_details?.transcendence}</p>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  </motion.div>
                </motion.div>
              ))}
          </div>
        </div>
      </div>
    );
  };

  // Render cultural comparison view
  const renderCulturalView = () => {
    const selectedSymbols = culturalComparison 
      ? [culturalComparison]
      : filteredSymbols;

    return (
      <motion.div 
        className="cultural-view"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="cultural-controls mb-6">
          <div className="field">
            <div className="control">
              <div className="select is-fullwidth">
                <select
                  value={selectedCulture}
                  onChange={(e) => setSelectedCulture(e.target.value)}
                >
                  {cultures.map(culture => (
                    <option key={culture} value={culture}>
                      {culture === "all" ? "All Cultures" : culture.charAt(0).toUpperCase() + culture.slice(1)}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>

        <div className="columns is-multiline">
          {selectedSymbols.map(({ symbol, category, meaning, cross_cultural, resonance_field }) => {
            const culturalMeanings = selectedCulture === "all" 
              ? (cross_cultural || {})
              : cross_cultural ? { [selectedCulture]: cross_cultural[selectedCulture] } : {};

            return (
              <motion.div 
                key={symbol} 
                className={`column ${isMobile ? 'is-12' : 'is-6'}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <motion.div 
                  className="box cultural-card"
                  style={{ 
                    borderLeft: `4px solid ${getCategoryColor(category)}`,
                    cursor: 'pointer'
                  }}
                  whileHover={{ scale: isMobile ? 1 : 1.02 }}
                  onClick={() => setExpandedSymbol(expandedSymbol === symbol ? null : symbol)}
                >
                  <div className="content">
                    <div className="is-flex is-justify-content-space-between is-align-items-center mb-4">
                      <div className="symbol-background"><span className="symbol-display" style={{ fontSize: isMobile ? '1.5rem' : '2rem' }}>{symbol}</span></div>
                      <span className="tag is-medium" style={{ backgroundColor: getCategoryColor(category), color: 'white' }}>
                        {category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                      </span>
                    </div>

                    <h4 className={`title ${isMobile ? 'is-5' : 'is-4'} has-text-primary`}>{meaning}</h4>

                    {cross_cultural && (
                      <div className="cultural-meanings mt-4">
                        {Object.entries(culturalMeanings).map(([culture, meaning]) => (
                          <div key={culture} className="cultural-meaning mb-4">
                            <h5 className={`title ${isMobile ? 'is-7' : 'is-6'} has-text-primary`}>
                              {culture.charAt(0).toUpperCase() + culture.slice(1)} Interpretation
                            </h5>
                            <div className="content">
                              <p>{meaning}</p>
                              {resonance_field && (
                                <div className="mt-2">
                                  <p className="is-size-7 has-text-grey">
                                    <em>Resonates with: {resonance_field.primary}</em>
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    <AnimatePresence>
                      {expandedSymbol === symbol && cross_cultural && (
                        <motion.div 
                          className="mt-4"
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: "auto" }}
                          exit={{ opacity: 0, height: 0 }}
                        >
                          <div className="cultural-analysis">
                            <h5 className={`title ${isMobile ? 'is-7' : 'is-6'} has-text-primary`}>Cultural Analysis</h5>
                            <div className="content">
                              <div className="tags mb-2">
                                {Object.keys(cross_cultural).map(culture => (
                                  <span 
                                    key={culture} 
                                    className={`tag ${selectedCulture === culture ? 'is-primary' : 'is-light'}`}
                                    onClick={() => setSelectedCulture(culture)}
                                    style={{ cursor: 'pointer' }}
                                  >
                                    {culture.charAt(0).toUpperCase() + culture.slice(1)}
                                  </span>
                                ))}
                              </div>
                              <div className="cultural-patterns">
                                <p className="is-size-7 has-text-grey">
                                  <strong>Common Themes:</strong> {Object.values(cross_cultural).join(" • ")}
                                </p>
                              </div>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </motion.div>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
    );
  };

  // Render mathematical pattern analysis
  const renderMathematicalView = () => {
    const generateBreathField = () => {
      const points = [];
      const timePoints = Array.from({ length: 100 }, (_, i) => i / 10);
      
      timePoints.forEach(t => {
        const x = Math.sin(t * breathParameters.frequency + breathParameters.phase);
        const y = Math.cos(t * breathParameters.frequency + breathParameters.phase);
        const amplitude = breathParameters.amplitude * Math.exp(-t * breathParameters.resonance);
        points.push({
          x: x * amplitude,
          y: y * amplitude,
          t
        });
      });

      return points;
    };

    const fieldData = generateBreathField();

    const chartData = {
      labels: fieldData.map(p => p.t.toFixed(1)),
      datasets: [
        {
          label: 'Breath Field Ψ(x,t)',
          data: fieldData.map(p => p.x),
          borderColor: getCategoryColor('elemental_core'),
          tension: 0.4,
          fill: false
        },
        {
          label: 'Observer Modulation θ(x,t)',
          data: fieldData.map(p => p.y),
          borderColor: getCategoryColor('consciousness_patterns'),
          tension: 0.4,
          fill: false
        }
      ]
    };

    const chartOptions = {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Breath Equation Field Evolution'
        },
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          title: {
            display: true,
            text: 'Amplitude'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Time'
          }
        }
      }
    };

    return (
      <motion.div 
        className="mathematical-view"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="mathematical-controls mb-6">
          <div className="tabs is-boxed">
            <ul>
              <li className={mathematicalView === "field" ? "is-active" : ""}>
                <a onClick={() => setMathematicalView("field")}>
                  <span className="icon"><i className="fas fa-wave-square"></i></span>
                  <span>Field Evolution</span>
                </a>
              </li>
              <li className={mathematicalView === "resonance" ? "is-active" : ""}>
                <a onClick={() => setMathematicalView("resonance")}>
                  <span className="icon"><i className="fas fa-project-diagram"></i></span>
                  <span>Resonance Patterns</span>
                </a>
              </li>
              <li className={mathematicalView === "pattern" ? "is-active" : ""}>
                <a onClick={() => setMathematicalView("pattern")}>
                  <span className="icon"><i className="fas fa-sitemap"></i></span>
                  <span>Pattern Analysis</span>
                </a>
              </li>
            </ul>
          </div>

          <div className="field is-grouped is-grouped-multiline mt-4">
            <div className="control">
              <label className="label">Amplitude (aₙ)</label>
              <input 
                type="range" 
                min="0" 
                max="2" 
                step="0.1" 
                value={breathParameters.amplitude}
                onChange={(e) => setBreathParameters(prev => ({ ...prev, amplitude: parseFloat(e.target.value) }))}
                className="slider is-fullwidth"
              />
            </div>
            <div className="control">
              <label className="label">Phase (φₙ)</label>
              <input 
                type="range" 
                min="0" 
                max="2*Math.PI" 
                step="0.1" 
                value={breathParameters.phase}
                onChange={(e) => setBreathParameters(prev => ({ ...prev, phase: parseFloat(e.target.value) }))}
                className="slider is-fullwidth"
              />
            </div>
            <div className="control">
              <label className="label">Frequency</label>
              <input 
                type="range" 
                min="0.1" 
                max="5" 
                step="0.1" 
                value={breathParameters.frequency}
                onChange={(e) => setBreathParameters(prev => ({ ...prev, frequency: parseFloat(e.target.value) }))}
                className="slider is-fullwidth"
              />
            </div>
            <div className="control">
              <label className="label">Resonance (𝓡)</label>
              <input 
                type="range" 
                min="0" 
                max="1" 
                step="0.1" 
                value={breathParameters.resonance}
                onChange={(e) => setBreathParameters(prev => ({ ...prev, resonance: parseFloat(e.target.value) }))}
                className="slider is-fullwidth"
              />
            </div>
          </div>
        </div>

        <div className="mathematical-content">
          {mathematicalView === "field" && (
            <div className="box">
              <div className="content">
                <h3 className="title is-4">Breath Equation Field Evolution</h3>
                <p className="subtitle is-6">Ψ(x, t) = ∑ₙ aₙ · e^(i·φₙ) · fₙ(𝓡 · sin(θ(x, t)) · ∇Ω)</p>
                <div className="chart-container" style={{ height: '400px' }}>
                  <Line data={chartData} options={chartOptions} />
                </div>
                
                {/* Add Symbol Field Equations */}
                <div className="mt-6">
                  <h4 className="title is-5">Symbol Field Equations</h4>
                  <div className="columns is-multiline">
                    {Object.entries(symbolData).map(([category, symbols]) => (
                      <div key={category} className="column is-6">
                        <div className="box">
                          <h5 className="title is-6">{category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</h5>
                          <div className="content">
                            {Object.entries(symbols).map(([symbol, data]) => (
                              data.mathematical_relationships && (
                                <div key={symbol} className="field-equation mb-4">
                                  <div className="is-flex is-align-items-center mb-2">
                                    <div className="symbol-background"><span className="symbol-display mr-2">{symbol}</span></div>
                                    <span className="has-text-grey">{data.meaning}</span>
                                  </div>
                                  <div className="field-equation-details">
                                    <p><strong>Field Equation:</strong> {data.mathematical_relationships.field_equation || '—'}</p>
                                    <p><strong>Parameters:</strong> {Array.isArray(data.mathematical_relationships.parameters) 
                                      ? data.mathematical_relationships.parameters.join(', ')
                                      : typeof data.mathematical_relationships.parameters === 'object'
                                        ? Object.entries(data.mathematical_relationships.parameters)
                                            .map(([key, value]) => `${key}: ${value.symbol || value}`)
                                            .join(', ')
                                        : '—'}</p>
                                    <p><strong>Field Components:</strong> {Array.isArray(data.mathematical_relationships.field_components)
                                      ? data.mathematical_relationships.field_components.join(', ')
                                      : typeof data.mathematical_relationships.field_components === 'object'
                                        ? Object.entries(data.mathematical_relationships.field_components)
                                            .map(([key, value]) => `${key}: ${value.symbol || value}`)
                                            .join(', ')
                                        : '—'}</p>
                                    <p><strong>Phase Transitions:</strong> {Array.isArray(data.mathematical_relationships.phase_transitions)
                                      ? data.mathematical_relationships.phase_transitions.join(', ')
                                      : '—'}</p>
                                  </div>
                                </div>
                              )
                            ))}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {mathematicalView === "resonance" && (
            <div className="box">
              <div className="content">
                <h3 className="title is-4">Resonance Pattern Analysis</h3>
                <div className="columns is-multiline">
                  {Object.entries(symbolData).map(([category, symbols]) => (
                    <div key={category} className="column is-6">
                      <div className="box">
                        <h4 className="title is-5">{category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</h4>
                        <div className="content">
                          {Object.entries(symbols).map(([symbol, data]) => (
                            <div key={symbol} className="resonance-item mb-4">
                              <div className="is-flex is-align-items-center mb-2">
                                <div className="symbol-background"><span className="symbol-display mr-2">{symbol}</span></div>
                                <span className="has-text-grey">{data.meaning}</span>
                              </div>
                              {data.resonance_field && (
                                <div className="resonance-details">
                                  <p><strong>Primary:</strong> {data.resonance_field.primary || '—'}</p>
                                  <div className="tags">
                                    {Array.isArray(data.resonance_field.secondary)
                                      ? data.resonance_field.secondary.map(res => (
                                          <span key={res} className="tag is-light">{res}</span>
                                        ))
                                      : <span className="tag is-light">No secondary resonances</span>}
                                  </div>
                                  {data.resonance_field.archetypal && (
                                    <p className="mt-2"><em>Archetypal: {data.resonance_field.archetypal}</em></p>
                                  )}
                                </div>
                              )}
                              {data.mathematical_relationships && (
                                <div className="mathematical-details mt-2">
                                  <p><strong>Field Equation:</strong> {data.mathematical_relationships.field_equation}</p>
                                  <p><strong>Parameters:</strong> {data.mathematical_relationships.parameters.join(', ')}</p>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {mathematicalView === "pattern" && (
            <div className="box">
              <div className="content">
                <h3 className="title is-4">Pattern Analysis</h3>
                <div className="pattern-grid">
                  {Object.entries(symbolData).map(([category, symbols]) => (
                    <div key={category} className="pattern-category mb-6">
                      <h4 className="title is-5" style={{ color: getCategoryColor(category) }}>
                        {getCategoryIcon(category)} {category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                      </h4>
                      <div className="columns is-multiline">
                        {Object.entries(symbols).map(([symbol, data]) => (
                          <div key={symbol} className="column is-4">
                            <div className="box pattern-item">
                              <div className="content">
                                <div className="symbol-background"><span className="symbol-display is-size-3">{symbol}</span></div>
                                <h5 className="title is-6">{data.meaning}</h5>
                                {data.resonance_field && (
                                  <div className="pattern-connections">
                                    <div className="tags">
                                      {Array.isArray(data.resonance_field.secondary)
                                        ? data.resonance_field.secondary.map(res => (
                                            <span key={res} className="tag is-light">{res}</span>
                                          ))
                                        : <span className="tag is-light">No secondary resonances</span>}
                                    </div>
                                  </div>
                                )}
                                {data.mathematical_relationships && (
                                  <div className="mathematical-pattern mt-2">
                                    <p className="is-size-7">
                                      <strong>Field Equation:</strong> {data.mathematical_relationships.field_equation || '—'}
                                    </p>
                                    <p className="is-size-7">
                                      <strong>Phase Transitions:</strong> {Array.isArray(data.mathematical_relationships.phase_transitions)
                                        ? data.mathematical_relationships.phase_transitions.join(', ')
                                        : '—'}
                                    </p>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </motion.div>
    );
  };

  // Mobile-optimized view controls
  const renderViewControls = () => (
    <div className={`tabs ${isMobile ? 'is-fullwidth' : 'is-boxed'} mb-6`}>
      <ul>
        <li className={viewMode === "grid" ? "is-active" : ""}>
          <a onClick={() => setViewMode("grid")}>
            <span className="icon"><i className="fas fa-th"></i></span>
            {!isMobile && <span>Grid View</span>}
          </a>
        </li>
        <li className={viewMode === "resonance" ? "is-active" : ""}>
          <a onClick={() => setViewMode("resonance")}>
            <span className="icon"><i className="fas fa-project-diagram"></i></span>
            {!isMobile && <span>Resonance View</span>}
          </a>
        </li>
        <li className={viewMode === "pattern" ? "is-active" : ""}>
          <a onClick={() => setViewMode("pattern")}>
            <span className="icon"><i className="fas fa-sitemap"></i></span>
            {!isMobile && <span>Pattern View</span>}
          </a>
        </li>
        <li className={viewMode === "graph" ? "is-active" : ""}>
          <a onClick={() => setViewMode("graph")}>
            <span className="icon"><i className="fas fa-network-wired"></i></span>
            {!isMobile && <span>Graph View</span>}
          </a>
        </li>
        <li className={viewMode === "timeline" ? "is-active" : ""}>
          <a onClick={() => setViewMode("timeline")}>
            <span className="icon"><i className="fas fa-history"></i></span>
            {!isMobile && <span>Timeline View</span>}
          </a>
        </li>
        <li className={viewMode === "cultural" ? "is-active" : ""}>
          <a onClick={() => setViewMode("cultural")}>
            <span className="icon"><i className="fas fa-globe"></i></span>
            {!isMobile && <span>Cultural View</span>}
          </a>
        </li>
        <li className={viewMode === "mathematical" ? "is-active" : ""}>
          <a onClick={() => setViewMode("mathematical")}>
            <span className="icon"><i className="fas fa-wave-square"></i></span>
            {!isMobile && <span>Mathematical View</span>}
          </a>
        </li>
      </ul>
    </div>
  );

  // Mobile-optimized search controls
  const renderSearchControls = () => (
    <div className="controls mb-6">
      <div className={`field ${isMobile ? 'has-addons has-addons-fullwidth' : 'has-addons'}`}>
        <div className="control is-expanded">
          <input
            className="input"
            type="text"
            placeholder={isMobile ? "Search symbols..." : "Search symbols by meaning, synonym, or cultural reference..."}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="control">
          <div className="select">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {isMobile 
                    ? category.split('_')[0].charAt(0).toUpperCase() 
                    : category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="symbol-browser">
      {renderViewControls()}
      {renderSearchControls()}

      <AnimatePresence mode="wait">
        {viewMode === "grid" && (
          <motion.div
            key="grid"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {/* Category Sections */}
            {selectedCategory === "all" ? (
              // When "all" is selected, group by category
              Object.keys(symbolData).map(category => {
                const categorySymbols = filteredSymbols.filter(s => s.category === category);
                if (categorySymbols.length === 0) return null;
                
                return (
                  <motion.div 
                    key={category} 
                    className="category-section mb-6"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    <div className="category-header mb-4">
                      <h3 className={`title ${isMobile ? 'is-5' : 'is-4'}`} style={{ color: getCategoryColor(category) }}>
                        {getCategoryIcon(category)} {category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                      </h3>
                    </div>
                    <div className={`columns is-multiline ${isMobile ? 'is-mobile' : ''}`}>
                      {categorySymbols.map(({ symbol, meaning, synonyms, cross_cultural, resonance_field }) => (
                        <motion.div 
                          key={symbol} 
                          className={`column ${isMobile ? 'is-12' : 'is-4'}`}
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ type: "spring", stiffness: 300 }}
                        >
                          <motion.div 
                            className="box enhanced-hover-card"
                            style={{ 
                              borderLeft: `4px solid ${getCategoryColor(category)}`,
                              cursor: 'pointer',
                              height: '100%',
                              display: 'flex',
                              flexDirection: 'column'
                            }}
                            whileHover={{ scale: isMobile ? 1 : 1.02 }}
                            onClick={() => setExpandedSymbol(expandedSymbol === symbol ? null : symbol)}
                          >
                            <div className="content" style={{ flex: 1 }}>
                              <div className="is-flex is-justify-content-space-between is-align-items-center mb-4">
                                <div className="symbol-background"><span className="symbol-display" style={{ fontSize: isMobile ? '1.5rem' : '2rem' }}>{symbol}</span></div>
                              </div>
                              
                              <h4 className={`title ${isMobile ? 'is-5' : 'is-4'} has-text-primary`}>{meaning}</h4>
                              
                              <AnimatePresence>
                                {expandedSymbol === symbol && (
                                  <motion.div 
                                    className="mt-4"
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: "auto" }}
                                    exit={{ opacity: 0, height: 0 }}
                                  >
                                    <div className="mb-4">
                                      <h5 className={`title ${isMobile ? 'is-7' : 'is-6'} has-text-primary`}>Synonyms</h5>
                                      <div className="tags">
                                        {synonyms.map(syn => (
                                          <span key={syn} className="tag is-light">{syn}</span>
                                        ))}
                                      </div>
                                    </div>

                                    <div className="mb-4">
                                      <h5 className={`title ${isMobile ? 'is-7' : 'is-6'} has-text-primary`}>Cross-Cultural Meanings</h5>
                                      <div className="content">
                                        <ul>
                                          {Object.entries(cross_cultural).map(([culture, meaning]) => (
                                            <li key={culture}>
                                              <strong>{culture.charAt(0).toUpperCase() + culture.slice(1)}:</strong> {meaning}
                                            </li>
                                          ))}
                                        </ul>
                                      </div>
                                    </div>

                                    {resonance_field && (
                                      <div>
                                        <h5 className={`title ${isMobile ? 'is-7' : 'is-6'} has-text-primary`}>Resonance Field</h5>
                                        <div className="content">
                                          <p><strong>Primary:</strong> {resonance_field.primary}</p>
                                          <div className="tags">
                                            {resonance_field.secondary.map(res => (
                                              <span key={res} className="tag is-light">{res}</span>
                                            ))}
                                          </div>
                                          <p className="mt-2"><em>Archetypal: {resonance_field.archetypal}</em></p>
                                        </div>
                                      </div>
                                    )}
                                  </motion.div>
                                )}
                              </AnimatePresence>
                            </div>
                          </motion.div>
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>
                );
              })
            ) : (
              // When a specific category is selected, show all matching symbols
              <div className={`columns is-multiline ${isMobile ? 'is-mobile' : ''}`}>
                {filteredSymbols.map(({ symbol, category, meaning, synonyms, cross_cultural, resonance_field }) => (
                  <motion.div 
                    key={symbol} 
                    className={`column ${isMobile ? 'is-12' : 'is-4'}`}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <motion.div 
                      className="box enhanced-hover-card"
                      style={{ 
                        borderLeft: `4px solid ${getCategoryColor(category)}`,
                        cursor: 'pointer',
                        height: '100%',
                        display: 'flex',
                        flexDirection: 'column'
                      }}
                      whileHover={{ scale: isMobile ? 1 : 1.02 }}
                      onClick={() => setExpandedSymbol(expandedSymbol === symbol ? null : symbol)}
                    >
                      <div className="content" style={{ flex: 1 }}>
                        <div className="is-flex is-justify-content-space-between is-align-items-center mb-4">
                          <div className="symbol-background"><span className="symbol-display" style={{ fontSize: isMobile ? '1.5rem' : '2rem' }}>{symbol}</span></div>
                        </div>
                        
                        <h4 className={`title ${isMobile ? 'is-5' : 'is-4'} has-text-primary`}>{meaning}</h4>
                        
                        <AnimatePresence>
                          {expandedSymbol === symbol && (
                            <motion.div 
                              className="mt-4"
                              initial={{ opacity: 0, height: 0 }}
                              animate={{ opacity: 1, height: "auto" }}
                              exit={{ opacity: 0, height: 0 }}
                            >
                              <div className="mb-4">
                                <h5 className={`title ${isMobile ? 'is-7' : 'is-6'} has-text-primary`}>Synonyms</h5>
                                <div className="tags">
                                  {synonyms.map(syn => (
                                    <span key={syn} className="tag is-light">{syn}</span>
                                  ))}
                                </div>
                              </div>

                              <div className="mb-4">
                                <h5 className={`title ${isMobile ? 'is-7' : 'is-6'} has-text-primary`}>Cross-Cultural Meanings</h5>
                                <div className="content">
                                  <ul>
                                    {Object.entries(cross_cultural).map(([culture, meaning]) => (
                                      <li key={culture}>
                                        <strong>{culture.charAt(0).toUpperCase() + culture.slice(1)}:</strong> {meaning}
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              </div>

                              {resonance_field && (
                                <div>
                                  <h5 className={`title ${isMobile ? 'is-7' : 'is-6'} has-text-primary`}>Resonance Field</h5>
                                  <div className="content">
                                    <p><strong>Primary:</strong> {resonance_field.primary}</p>
                                    <div className="tags">
                                      {resonance_field.secondary.map(res => (
                                        <span key={res} className="tag is-light">{res}</span>
                                      ))}
                                    </div>
                                    <p className="mt-2"><em>Archetypal: {resonance_field.archetypal}</em></p>
                                  </div>
                                </div>
                              )}
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    </motion.div>
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        )}

        {viewMode === "resonance" && renderResonanceView()}
        {viewMode === "pattern" && renderPatternView()}
        {viewMode === "graph" && renderGraphView()}
        {viewMode === "timeline" && renderTimelineView()}
        {viewMode === "cultural" && renderCulturalView()}
        {viewMode === "mathematical" && renderMathematicalView()}
      </AnimatePresence>

      {/* No Results Message */}
      {filteredSymbols.length === 0 && (
        <motion.div 
          className="has-text-centered my-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <p className={`${isMobile ? 'is-size-6' : 'is-size-5'} has-text-grey`}>No symbols found matching your search criteria.</p>
        </motion.div>
      )}
    </div>
  );
};

export default SymbolBrowser; 