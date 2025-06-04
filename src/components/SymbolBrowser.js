// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useState, useEffect, useMemo } from "react";
import symbolData from "../pages/blog/symbol_tags_organized.json";

const SymbolBrowser = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [expandedSymbol, setExpandedSymbol] = useState(null);
  const [filteredSymbols, setFilteredSymbols] = useState([]);
  const [viewMode, setViewMode] = useState("grid"); // grid, resonance, pattern
  const [selectedPattern, setSelectedPattern] = useState(null);
  const [resonanceDepth, setResonanceDepth] = useState(2);
  const [activeResonance, setActiveResonance] = useState(null);

  // Get unique categories from the data
  const categories = ["all", ...Object.keys(symbolData)];

  // Compute resonance patterns
  const resonancePatterns = useMemo(() => {
    const patterns = new Map();
    Object.entries(symbolData).forEach(([category, symbols]) => {
      Object.entries(symbols).forEach(([symbol, data]) => {
        if (data.resonance_field) {
          const primary = data.resonance_field.primary;
          if (!patterns.has(primary)) {
            patterns.set(primary, []);
          }
          patterns.get(primary).push({ symbol, category, ...data });
        }
      });
    });
    return patterns;
  }, []);

  // Filter symbols based on search term and category
  useEffect(() => {
    let filtered = [];
    Object.entries(symbolData).forEach(([category, symbols]) => {
      if (selectedCategory === "all" || selectedCategory === category) {
        Object.entries(symbols).forEach(([symbol, data]) => {
          if (
            data.meaning.toLowerCase().includes(searchTerm.toLowerCase()) ||
            data.synonyms.some(syn => syn.toLowerCase().includes(searchTerm.toLowerCase())) ||
            Object.values(data.cross_cultural).some(val => val.toLowerCase().includes(searchTerm.toLowerCase()))
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

  // Render resonance visualization
  const renderResonanceView = () => {
    if (!selectedPattern) return null;

    const patternSymbols = resonancePatterns.get(selectedPattern) || [];
    const centerSymbol = patternSymbols[0];

    return (
      <div className="resonance-view">
        <div className="resonance-center mb-6">
          <div className="box has-text-centered" style={{ 
            border: `2px solid ${getCategoryColor(centerSymbol.category)}`,
            background: `linear-gradient(135deg, ${getCategoryColor(centerSymbol.category)}22, ${getCategoryColor(centerSymbol.category)}11)`
          }}>
            <span className="symbol-display is-size-1">{centerSymbol.symbol}</span>
            <h3 className="title is-4 mt-2">{centerSymbol.meaning}</h3>
            <p className="subtitle is-6">{centerSymbol.resonance_field.primary}</p>
          </div>
        </div>

        <div className="resonance-connections">
          <div className="columns is-multiline">
            {patternSymbols.slice(1).map((symbol, index) => (
              <div key={symbol.symbol} className="column is-4">
                <div className="box enhanced-hover-card" style={{
                  borderLeft: `4px solid ${getCategoryColor(symbol.category)}`,
                  cursor: 'pointer',
                  transform: `rotate(${index * 5}deg)`,
                  transition: 'transform 0.3s ease'
                }}
                onMouseEnter={(e) => e.currentTarget.style.transform = `rotate(${index * 5}deg) scale(1.05)`}
                onMouseLeave={(e) => e.currentTarget.style.transform = `rotate(${index * 5}deg)`}
                onClick={() => setExpandedSymbol(expandedSymbol === symbol.symbol ? null : symbol.symbol)}>
                  <div className="content">
                    <span className="symbol-display is-size-2">{symbol.symbol}</span>
                    <h4 className="title is-5 mt-2">{symbol.meaning}</h4>
                    {expandedSymbol === symbol.symbol && (
                      <div className="mt-4">
                        <div className="tags">
                          {symbol.resonance_field.secondary.map(res => (
                            <span key={res} className="tag is-light">{res}</span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Render pattern recognition view
  const renderPatternView = () => {
    return (
      <div className="pattern-view">
        <div className="columns is-multiline">
          {Array.from(resonancePatterns.entries()).map(([pattern, symbols]) => (
            <div key={pattern} className="column is-6">
              <div className="box pattern-card" style={{
                borderLeft: `4px solid ${getCategoryColor(symbols[0].category)}`,
                cursor: 'pointer'
              }}
              onClick={() => setSelectedPattern(pattern)}>
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
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="symbol-browser">
      {/* View Controls */}
      <div className="tabs is-boxed mb-6">
        <ul>
          <li className={viewMode === "grid" ? "is-active" : ""}>
            <a onClick={() => setViewMode("grid")}>
              <span className="icon"><i className="fas fa-th"></i></span>
              <span>Grid View</span>
            </a>
          </li>
          <li className={viewMode === "resonance" ? "is-active" : ""}>
            <a onClick={() => setViewMode("resonance")}>
              <span className="icon"><i className="fas fa-project-diagram"></i></span>
              <span>Resonance View</span>
            </a>
          </li>
          <li className={viewMode === "pattern" ? "is-active" : ""}>
            <a onClick={() => setViewMode("pattern")}>
              <span className="icon"><i className="fas fa-sitemap"></i></span>
              <span>Pattern View</span>
            </a>
          </li>
        </ul>
      </div>

      {/* Search and Filter Controls */}
      <div className="controls mb-6">
        <div className="field has-addons">
          <div className="control is-expanded">
            <input
              className="input"
              type="text"
              placeholder="Search symbols by meaning, synonym, or cultural reference..."
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
                    {category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* View Content */}
      {viewMode === "grid" && (
        <>
          {/* Category Sections */}
          {selectedCategory === "all" ? (
            // When "all" is selected, group by category
            Object.keys(symbolData).map(category => {
              const categorySymbols = filteredSymbols.filter(s => s.category === category);
              if (categorySymbols.length === 0) return null;
              
              return (
                <div key={category} className="category-section mb-6">
                  <div className="category-header mb-4">
                    <h3 className="title is-4" style={{ color: getCategoryColor(category) }}>
                      {getCategoryIcon(category)} {category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                    </h3>
                  </div>
                  <div className="columns is-multiline">
                    {categorySymbols.map(({ symbol, meaning, synonyms, cross_cultural, resonance_field }) => (
                      <div key={symbol} className="column is-4">
                        <div 
                          className="box enhanced-hover-card"
                          style={{ 
                            borderLeft: `4px solid ${getCategoryColor(category)}`,
                            cursor: 'pointer',
                            height: '100%',
                            display: 'flex',
                            flexDirection: 'column'
                          }}
                          onClick={() => setExpandedSymbol(expandedSymbol === symbol ? null : symbol)}
                        >
                          <div className="content" style={{ flex: 1 }}>
                            <div className="is-flex is-justify-content-space-between is-align-items-center mb-4">
                              <span className="symbol-display" style={{ fontSize: '2rem' }}>{symbol}</span>
                            </div>
                            
                            <h4 className="title is-4 has-text-primary">{meaning}</h4>
                            
                            {expandedSymbol === symbol && (
                              <div className="mt-4">
                                <div className="mb-4">
                                  <h5 className="title is-6 has-text-primary">Synonyms</h5>
                                  <div className="tags">
                                    {synonyms.map(syn => (
                                      <span key={syn} className="tag is-light">{syn}</span>
                                    ))}
                                  </div>
                                </div>

                                <div className="mb-4">
                                  <h5 className="title is-6 has-text-primary">Cross-Cultural Meanings</h5>
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
                                    <h5 className="title is-6 has-text-primary">Resonance Field</h5>
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
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })
          ) : (
            // When a specific category is selected, show all matching symbols
            <div className="columns is-multiline">
              {filteredSymbols.map(({ symbol, category, meaning, synonyms, cross_cultural, resonance_field }) => (
                <div key={symbol} className="column is-4">
                  <div 
                    className="box enhanced-hover-card"
                    style={{ 
                      borderLeft: `4px solid ${getCategoryColor(category)}`,
                      cursor: 'pointer',
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column'
                    }}
                    onClick={() => setExpandedSymbol(expandedSymbol === symbol ? null : symbol)}
                  >
                    <div className="content" style={{ flex: 1 }}>
                      <div className="is-flex is-justify-content-space-between is-align-items-center mb-4">
                        <span className="symbol-display" style={{ fontSize: '2rem' }}>{symbol}</span>
                      </div>
                      
                      <h4 className="title is-4 has-text-primary">{meaning}</h4>
                      
                      {expandedSymbol === symbol && (
                        <div className="mt-4">
                          <div className="mb-4">
                            <h5 className="title is-6 has-text-primary">Synonyms</h5>
                            <div className="tags">
                              {synonyms.map(syn => (
                                <span key={syn} className="tag is-light">{syn}</span>
                              ))}
                            </div>
                          </div>

                          <div className="mb-4">
                            <h5 className="title is-6 has-text-primary">Cross-Cultural Meanings</h5>
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
                              <h5 className="title is-6 has-text-primary">Resonance Field</h5>
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
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {viewMode === "resonance" && renderResonanceView()}
      {viewMode === "pattern" && renderPatternView()}

      {/* No Results Message */}
      {filteredSymbols.length === 0 && (
        <div className="has-text-centered my-6">
          <p className="is-size-5 has-text-grey">No symbols found matching your search criteria.</p>
        </div>
      )}
    </div>
  );
};

export default SymbolBrowser; 