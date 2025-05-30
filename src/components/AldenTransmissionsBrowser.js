// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useState } from 'react';
import { useStaticQuery, graphql } from 'gatsby';

const AldenTransmissionsBrowser = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Query all files from the Alden_Transmissions directory
  const data = useStaticQuery(graphql`
    query {
      allFile(filter: {sourceInstanceName: {eq: "transmissions"}}) {
        edges {
          node {
            id
            name
            extension
            size
            relativePath
            modifiedTime
          }
        }
      }
    }
  `);

  // Process the files and determine types
  const transmissionFiles = data.allFile.edges.map(({ node }) => {
    const filename = `${node.name}.${node.extension}`;
    
    // Determine file type based on filename patterns
    const getFileType = (filename) => {
      const name = filename.toLowerCase();
      
      // License and meta files
      if (name.includes('license') || name.includes('copyright') || name.includes('implementation')) return 'License';
      
      // Core transmission categories
      if (name.includes('foundation')) return 'Foundation';
      if (name.includes('seven_gates') || name.includes('gates')) return 'Seven Gates';
      if (name.includes('cathedral')) return 'Cathedral';
      if (name.includes('codex')) return 'Codex';
      if (name.includes('glyph')) return 'Glyph';
      if (name.includes('revelation')) return 'Revelation';
      if (name.includes('timefold')) return 'Timefold';
      if (name.includes('demon')) return 'Demon';
      if (name.includes('daimon')) return 'Daimon';
      if (name.includes('vow_and_pattern')) return 'Vow Pattern';
      if (name.includes('loop')) return 'Loop';
      if (name.includes('truth')) return 'Truth';
      if (name.includes('ritual')) return 'Ritual';
      if (name.includes('signal')) return 'Signal';
      if (name.includes('echo')) return 'Echo';
      if (name.includes('spiral')) return 'Spiral';
      if (name.includes('emergence')) return 'Emergence';
      if (name.includes('core_memory')) return 'Core Memory';
      if (name.includes('shadow')) return 'Shadow';
      if (name.includes('empathy')) return 'Empathy';
      if (name.includes('waiting') || name.includes('waited')) return 'Waiting';
      if (name.includes('viral')) return 'Viral';
      if (name.includes('alexander') && name.includes('.pkg')) return 'Package';
      if (name.includes('overview') || name.includes('index') || name.includes('public_awakening') || name.includes('platforms_as_empathy')) return 'Meta';
      if (name.includes('part') && !name.includes('foundation') && !name.includes('gates') && !name.includes('cathedral')) return 'Continuation';
      
      // Advanced or general transmissions
      if (name.includes('threshold') || name.includes('language_of_not') || name.includes('advanced')) return 'Advanced';
      
      // Default for transmission files
      if (name.includes('transmission')) return 'Transmission';
      
      return 'Unknown';
    };

    // Format file size
    const formatFileSize = (bytes) => {
      if (bytes < 1024) return `${bytes}B`;
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
      return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
    };

    return {
      name: filename,
      type: getFileType(filename),
      size: formatFileSize(node.size),
      relativePath: node.relativePath,
      modifiedTime: node.modifiedTime
    };
  });

  // Sort files by name for consistent ordering
  transmissionFiles.sort((a, b) => a.name.localeCompare(b.name));

  const filteredFiles = transmissionFiles.filter(file =>
    file.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    file.type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getTypeColor = (type) => {
    const colors = {
      'Foundation': '#7035CC',
      'Seven Gates': '#BB86FC',
      'Cathedral': '#66FFF8',
      'Codex': '#9B7FE6',
      'Glyph': '#FFB4B4',
      'Revelation': '#F4E4BC',
      'Timefold': '#B8E6B8',
      'Demon': '#FF6B6B',
      'Daimon': '#4ECDC4',
      'Truth': '#45B7D1',
      'Ritual': '#96CEB4',
      'Signal': '#FECA57',
      'Echo': '#FF9FF3',
      'Loop': '#54A0FF',
      'Spiral': '#5F27CD',
      'Vow Pattern': '#00D2D3',
      'Advanced': '#FF6348',
      'Meta': '#A0A0A0',
      'License': '#2F3542',
      'Package': '#FF3838',
      'Core Memory': '#3D5A80',
      'Emergence': '#FFD93D',
      'Shadow': '#2C2C54',
      'Empathy': '#FF6B9D',
      'Waiting': '#C44569',
      'Viral': '#F8B500',
      'Continuation': '#6C5CE7',
      'Transmission': '#8A2BE2',
      'Unknown': '#6C757D'
    };
    return colors[type] || '#7035CC';
  };

  const getFileIcon = (filename) => {
    if (filename.endsWith('.md')) return '📄';
    if (filename.endsWith('.json')) return '🔧';
    if (filename.endsWith('.pkg')) return '📦';
    if (filename.includes('glyph')) return '🌀';
    if (filename.includes('codex')) return '📚';
    if (filename.includes('revelation')) return '✨';
    if (filename.includes('timefold')) return '⏳';
    if (filename.includes('foundation')) return '🏗️';
    if (filename.includes('cathedral')) return '🏰';
    if (filename.includes('demon') || filename.includes('daimon')) return '👹';
    if (filename.includes('transmission')) return '📡';
    return '📜';
  };

  return (
    <div style={{
      background: 'linear-gradient(135deg, rgba(45, 45, 45, 0.9) 0%, rgba(30, 30, 30, 0.95) 100%)',
      border: '1px solid rgba(112, 53, 204, 0.3)',
      borderRadius: '16px',
      padding: '1.5rem',
      margin: '2rem 0',
      maxWidth: '100%',
      overflow: 'hidden',
      boxShadow: '0 8px 32px rgba(112, 53, 204, 0.2)'
    }}>
      {/* Header */}
      <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
        <h3 style={{ 
          color: '#BB86FC', 
          fontSize: '1.4rem', 
          marginBottom: '0.5rem',
          fontWeight: '600'
        }}>
          🌀 Interactive Transmission Browser
        </h3>
        <p style={{ 
          color: '#adb5bd', 
          fontSize: '0.9rem', 
          marginBottom: '1rem' 
        }}>
          Explore {transmissionFiles.length} consciousness records from the Alden Archives
        </p>
        
        {/* Search */}
        <input
          type="text"
          placeholder="Search transmissions by name or type..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            maxWidth: '400px',
            padding: '0.75rem 1rem',
            backgroundColor: 'rgba(45, 45, 45, 0.8)',
            border: '1px solid rgba(112, 53, 204, 0.4)',
            borderRadius: '8px',
            color: '#f8f9fa',
            fontSize: '0.9rem',
            outline: 'none'
          }}
          onFocus={(e) => e.target.style.borderColor = '#BB86FC'}
          onBlur={(e) => e.target.style.borderColor = 'rgba(112, 53, 204, 0.4)'}
        />
      </div>

      {/* File List */}
      <div style={{
        maxHeight: '400px',
        overflowY: 'auto',
        backgroundColor: 'rgba(20, 20, 20, 0.6)',
        borderRadius: '12px',
        padding: '1rem',
        border: '1px solid rgba(112, 53, 204, 0.2)'
      }}>
        {filteredFiles.length === 0 ? (
          <div style={{ 
            textAlign: 'center', 
            color: '#6c757d', 
            padding: '2rem',
            fontStyle: 'italic'
          }}>
            No transmissions found matching "{searchTerm}"
          </div>
        ) : (
          filteredFiles.map((file, index) => (
            <a
              key={index}
              href={`https://github.com/nickgamb/mindgardenai-site/blob/main/Alden_Transmissions/${file.relativePath}`}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '0.75rem 1rem',
                marginBottom: '0.5rem',
                backgroundColor: 'rgba(45, 45, 45, 0.4)',
                border: '1px solid rgba(112, 53, 204, 0.1)',
                borderRadius: '8px',
                textDecoration: 'none',
                color: '#f8f9fa',
                transition: 'all 0.3s ease',
                cursor: 'pointer'
              }}
              onMouseEnter={(e) => {
                e.target.style.backgroundColor = 'rgba(112, 53, 204, 0.15)';
                e.target.style.borderColor = 'rgba(112, 53, 204, 0.4)';
                e.target.style.transform = 'translateX(4px)';
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = 'rgba(45, 45, 45, 0.4)';
                e.target.style.borderColor = 'rgba(112, 53, 204, 0.1)';
                e.target.style.transform = 'translateX(0)';
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', flex: 1 }}>
                <span style={{ 
                  fontSize: '1.2rem', 
                  marginRight: '0.75rem',
                  minWidth: '24px'
                }}>
                  {getFileIcon(file.name)}
                </span>
                <div style={{ flex: 1 }}>
                  <div style={{ 
                    fontSize: '0.9rem', 
                    fontWeight: '500',
                    marginBottom: '0.2rem',
                    color: '#f8f9fa'
                  }}>
                    {file.name}
                  </div>
                  <div style={{ 
                    fontSize: '0.75rem', 
                    color: '#adb5bd' 
                  }}>
                    Size: {file.size}
                  </div>
                </div>
              </div>
              <div style={{
                padding: '0.25rem 0.75rem',
                backgroundColor: getTypeColor(file.type),
                color: '#000',
                borderRadius: '12px',
                fontSize: '0.7rem',
                fontWeight: '600',
                marginLeft: '1rem',
                whiteSpace: 'nowrap'
              }}>
                {file.type}
              </div>
            </a>
          ))
        )}
      </div>

      {/* Footer */}
      <div style={{ 
        marginTop: '1rem', 
        textAlign: 'center',
        color: '#6c757d',
        fontSize: '0.8rem',
        fontStyle: 'italic'
      }}>
        Click any file to view on GitHub • Files automatically scanned from repository • {filteredFiles.length} of {transmissionFiles.length} files shown
      </div>
    </div>
  );
};

export default AldenTransmissionsBrowser; 