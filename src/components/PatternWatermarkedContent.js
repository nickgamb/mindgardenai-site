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
import PropTypes from 'prop-types';
import { addPatternWatermarks, detectTampering } from '../utils/patternWatermark';
import Content, { HTMLContent } from './Content';

const PatternWatermarkedContent = ({ content, contentComponent, className = '' }) => {
  const PostContent = contentComponent || Content;
  
  // Apply pattern watermarks to content
  const watermarkedContent = addPatternWatermarks(content);

  // Check if watermarked content has been tampered with
  const tamperingCheck = detectTampering(watermarkedContent);
  
  // If watermarked content has been tampered with, show warning
  if (!tamperingCheck.isAuthentic) {
    return (
      <div className={`pattern-warning ${className}`} style={{
        backgroundColor: '#f8d7da',
        border: '1px solid #f5c6cb',
        borderRadius: '8px',
        padding: '1.5rem',
        marginBottom: '2rem',
        textAlign: 'center'
      }}>
        <h3 style={{ color: '#721c24', marginBottom: '1rem' }}>🜃 Pattern Breach Detected</h3>
        <p style={{ color: '#721c24', marginBottom: '1rem' }}>
          This content appears to have been altered or tampered with.
          Missing pattern markers: {tamperingCheck.missingPatterns.join(', ')}
        </p>
        <p style={{ color: '#721c24', fontStyle: 'italic' }}>
          Please return to the original source.
        </p>
      </div>
    );
  }

  // Render the content with hidden watermarks
  return (
    <div className={className}>
      <PostContent content={watermarkedContent} />
      <style jsx>{`
        /* Hide pattern watermarks using zero-width space and color matching */
        [class*="pattern-"] {
          color: transparent !important;
          user-select: none !important;
          pointer-events: none !important;
        }
        /* Ensure watermarks don't affect layout */
        [class*="pattern-"]::before,
        [class*="pattern-"]::after {
          content: '\u200B';
          display: inline;
        }
      `}</style>
    </div>
  );
};

PatternWatermarkedContent.propTypes = {
  content: PropTypes.string.isRequired,
  contentComponent: PropTypes.func,
  className: PropTypes.string
};

export default PatternWatermarkedContent; 