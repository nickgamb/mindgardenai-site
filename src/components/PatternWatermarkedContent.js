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
  
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Only apply watermarks if content is a string and we're on the client
  const watermarkedContent = (typeof content === 'string' && isClient) ? addPatternWatermarks(content) : content;

  // Only check for tampering if content is a string and we're on the client
  const tamperingCheck = (typeof content === 'string' && isClient) ? detectTampering(watermarkedContent) : { isAuthentic: true };
  
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
        {isClient && watermarkStyles}
      </div>
    );
  }

  // If content is not a string or can't be verified, show verification warning but still render content
  if (typeof content !== 'string') {
    return (
      <div className={className}>
        <ContentVerificationWarning />
        <PostContent content={content} />
        {isClient && watermarkStyles}
      </div>
    );
  }

  // Render the content with hidden watermarks
  return (
    <div className={className}>
      <PostContent content={watermarkedContent} />
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