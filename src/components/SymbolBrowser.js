// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useState, useEffect } from "react";
import symbolData from "../pages/blog/symbol_tags_organized.json";

const SymbolBrowser = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [expandedSymbol, setExpandedSymbol] = useState(null);
  const [filteredSymbols, setFilteredSymbols] = useState([]);

  // Get unique categories from the data
  const categories = ["all", ...Object.keys(symbolData)];

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

  return (
    <div className="symbol-browser">
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