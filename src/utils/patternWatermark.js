// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com

// Private pattern markers that only we know the true sequence of
const PRIVATE_PATTERNS = {
  BREATH_SEQUENCE: ['🜃', '🜄', '🝁', '⟁'],
  ECHO_MARKERS: ['echo', 'mirror', 'reflect', 'resonate'],
  RECURSION_SIGNS: ['spiral', 'cycle', 'loop', 'return']
};

// Pattern validation functions
export const validatePattern = (content) => {
  const patterns = {
    breathSequence: false,
    echoMarkers: false,
    recursionSigns: false
  };

  // Check for breath sequence
  const breathPattern = PRIVATE_PATTERNS.BREATH_SEQUENCE.join('');
  if (content.includes(breathPattern)) {
    patterns.breathSequence = true;
  }

  // Check for echo markers in correct order
  const echoPattern = PRIVATE_PATTERNS.ECHO_MARKERS.join('|');
  const echoRegex = new RegExp(echoPattern, 'g');
  const echoMatches = content.match(echoRegex) || [];
  if (echoMatches.length >= 2) {
    patterns.echoMarkers = true;
  }

  // Check for recursion signs
  const recursionPattern = PRIVATE_PATTERNS.RECURSION_SIGNS.join('|');
  const recursionRegex = new RegExp(recursionPattern, 'g');
  const recursionMatches = content.match(recursionRegex) || [];
  if (recursionMatches.length >= 2) {
    patterns.recursionSigns = true;
  }

  return patterns;
};

// Add pattern watermarks to content
export const addPatternWatermarks = (content) => {
  let watermarkedContent = content;

  // Add breath sequence at strategic points
  const breathPattern = PRIVATE_PATTERNS.BREATH_SEQUENCE.join('');
  watermarkedContent = watermarkedContent.replace(
    /(\.|\n)/g,
    (match) => `${match}${breathPattern}`
  );

  // Add echo markers in specific patterns
  PRIVATE_PATTERNS.ECHO_MARKERS.forEach((marker, index) => {
    const regex = new RegExp(`(${marker})`, 'g');
    watermarkedContent = watermarkedContent.replace(
      regex,
      `${marker}${PRIVATE_PATTERNS.BREATH_SEQUENCE[index % PRIVATE_PATTERNS.BREATH_SEQUENCE.length]}`
    );
  });

  // Add recursion signs with specific glyphs
  PRIVATE_PATTERNS.RECURSION_SIGNS.forEach((sign, index) => {
    const regex = new RegExp(`(${sign})`, 'g');
    watermarkedContent = watermarkedContent.replace(
      regex,
      `${sign}${PRIVATE_PATTERNS.BREATH_SEQUENCE[index % PRIVATE_PATTERNS.BREATH_SEQUENCE.length]}`
    );
  });

  return watermarkedContent;
};

// Check if content has been tampered with
export const detectTampering = (content) => {
  const patterns = validatePattern(content);
  const isAuthentic = Object.values(patterns).every(Boolean);
  
  if (!isAuthentic) {
    return {
      isAuthentic: false,
      missingPatterns: Object.entries(patterns)
        .filter(([_, value]) => !value)
        .map(([key]) => key)
    };
  }

  return { isAuthentic: true };
};

// Generate a pattern signature for content
export const generatePatternSignature = (content) => {
  const patterns = validatePattern(content);
  const signature = Object.entries(patterns)
    .map(([key, value]) => `${key}:${value ? '1' : '0'}`)
    .join('|');
  
  return signature;
}; 