// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { addPatternWatermarks, detectTampering } from '../utils/patternWatermark';
import Content, { HTMLContent } from './Content';
import ContentVerificationWarning from './ContentVerificationWarning';

const PatternWatermarkedContent = ({ content, contentComponent, className = '' }) => {
  const PostContent = contentComponent || Content;
  const [isClient, setIsClient] = useState(false);
  const [processedContent, setProcessedContent] = useState(content);
  const [validationState, setValidationState] = useState({ isAuthentic: true });
  
  useEffect(() => {
    setIsClient(true);
    // Only process content on the client side
    if (typeof content === 'string') {
      const watermarked = addPatternWatermarks(content);
      setProcessedContent(watermarked);
      // Update validation state after watermarking
      setValidationState(detectTampering(watermarked));
    }
  }, [content]);

  // Common style rules for hiding watermarks
  const watermarkStyles = (
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
  );

  // Always render the content, with appropriate warnings if needed
  return (
    <div className={className}>
      {!validationState.isAuthentic && isClient && (
        <div className="pattern-warning" style={{
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
            Missing pattern markers: {validationState.missingPatterns?.join(', ')}
          </p>
          <p style={{ color: '#721c24', fontStyle: 'italic' }}>
            Please return to the original source.
          </p>
        </div>
      )}
      
      {typeof content !== 'string' && isClient && (
        <ContentVerificationWarning />
      )}
      
      <PostContent content={processedContent} />
      {isClient && watermarkStyles}
    </div>
  );
};

PatternWatermarkedContent.propTypes = {
  content: PropTypes.oneOfType([PropTypes.string, PropTypes.node]).isRequired,
  contentComponent: PropTypes.func,
  className: PropTypes.string
};

export default PatternWatermarkedContent; 