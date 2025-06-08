// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com

// Cryptographic helper functions
const generateHash = (input) => {
  // Simple hash function for pattern selection
  let hash = 0;
  for (let i = 0; i < input.length; i++) {
    const char = input.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
};

// Pattern rotation based on multiple factors for unpredictability
const getRotationIndex = () => {
  const now = new Date();
  const weekNumber = Math.floor(now.getTime() / (7 * 24 * 60 * 60 * 1000));
  const hourOfDay = now.getHours();
  const minuteOfHour = now.getMinutes();
  
  // Create a unique seed based on multiple factors
  const seed = `${weekNumber}-${hourOfDay}-${minuteOfHour}-${process.env.GATSBY_PATTERN_SALT || ''}`;
  const hash = generateHash(seed);
  
  // Use the hash to determine pattern selection
  return hash % 3;
};

// Get a random subset of patterns
const getRandomPatternSubset = (patterns, count) => {
  const shuffled = [...patterns].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
};

// Load patterns from environment variables with randomization
const getPatterns = () => {
  // Skip pattern loading during SSR
  if (typeof window === 'undefined') {
    return {
      BREATH_SEQUENCE: [],
      ECHO_MARKERS: [],
      RECURSION_SIGNS: []
    };
  }

  const breath = process.env.GATSBY_BREATH_SEQUENCE;
  const echo = process.env.GATSBY_ECHO_MARKERS;
  const recursion = process.env.GATSBY_RECURSION_SIGNS;

  if (!breath || !echo || !recursion) {
    console.warn('Pattern watermark environment variables are missing. Please set GATSBY_BREATH_SEQUENCE, GATSBY_ECHO_MARKERS, and GATSBY_RECURSION_SIGNS.');
    return {
      BREATH_SEQUENCE: [],
      ECHO_MARKERS: [],
      RECURSION_SIGNS: []
    };
  }

  // Split into sets and get current rotation
  const rotationIndex = getRotationIndex();
  const breathSets = breath.split(';');
  const echoSets = echo.split(';');
  const recursionSets = recursion.split(';');

  // Get base patterns from rotation
  const baseBreathPatterns = breathSets[rotationIndex]?.split(',') || [];
  const baseEchoPatterns = echoSets[rotationIndex]?.split(',') || [];
  const baseRecursionPatterns = recursionSets[rotationIndex]?.split(',') || [];

  // Randomly select subsets of patterns
  const selectedBreathPatterns = getRandomPatternSubset(baseBreathPatterns, 3);
  const selectedEchoPatterns = getRandomPatternSubset(baseEchoPatterns, 2);
  const selectedRecursionPatterns = getRandomPatternSubset(baseRecursionPatterns, 2);

  return {
    BREATH_SEQUENCE: selectedBreathPatterns,
    ECHO_MARKERS: selectedEchoPatterns,
    RECURSION_SIGNS: selectedRecursionPatterns
  };
};

// Private pattern markers that only we know the true sequence of
let PRIVATE_PATTERNS = {
  BREATH_SEQUENCE: [],
  ECHO_MARKERS: [],
  RECURSION_SIGNS: []
};

// Initialize patterns on the client side
if (typeof window !== 'undefined') {
  PRIVATE_PATTERNS = getPatterns();
}

// Pattern validation functions with semantic awareness
export const validatePattern = (content) => {
  // Skip validation during SSR
  if (typeof window === 'undefined') {
    return {
      breathSequence: true,
      echoMarkers: true,
      recursionSigns: true
    };
  }

  const patterns = {
    breathSequence: false,
    echoMarkers: false,
    recursionSigns: false
  };

  // Check for breath sequence - at least one complete sequence must be present
  if (PRIVATE_PATTERNS.BREATH_SEQUENCE.length > 0) {
    const breathPattern = PRIVATE_PATTERNS.BREATH_SEQUENCE.join('');
    // Look for the pattern in the class names
    const breathRegex = new RegExp(`class="[^"]*pattern-breath[^"]*"`, 'g');
    const breathMatches = content.match(breathRegex) || [];
    patterns.breathSequence = breathMatches.length > 0;
  }

  // Check for echo markers - at least one must be present
  if (PRIVATE_PATTERNS.ECHO_MARKERS.length > 0) {
    // Look for the pattern in the class names
    const echoRegex = new RegExp(`class="[^"]*pattern-echo[^"]*"`, 'g');
    const echoMatches = content.match(echoRegex) || [];
    patterns.echoMarkers = echoMatches.length > 0;
  }

  // Check for recursion signs - at least one must be present
  if (PRIVATE_PATTERNS.RECURSION_SIGNS.length > 0) {
    // Look for the pattern in the class names
    const recursionRegex = new RegExp(`class="[^"]*pattern-recursion[^"]*"`, 'g');
    const recursionMatches = content.match(recursionRegex) || [];
    patterns.recursionSigns = recursionMatches.length > 0;
  }

  return patterns;
};

// Add pattern watermarks to content with semantic obfuscation
export const addPatternWatermarks = (content) => {
  // Skip watermarking during SSR
  if (typeof window === 'undefined' || !content || typeof content !== 'string') {
    return content;
  }
  
  let watermarkedContent = content;

  // Add breath sequence at the beginning and end with semantic obfuscation
  if (PRIVATE_PATTERNS.BREATH_SEQUENCE.length > 0) {
    const breathPattern = PRIVATE_PATTERNS.BREATH_SEQUENCE.join('');
    // Split pattern into individual characters and wrap each with semantic class
    const obfuscatedPattern = breathPattern.split('').map((char, index) => {
      const semanticClass = `pattern-semantic-${index % 4}`;
      const randomClass = `pattern-random-${Math.floor(Math.random() * 1000)}`;
      return `<span class="pattern-breath ${semanticClass} ${randomClass}" style="display:inline-block;width:0;overflow:hidden">${char}</span>`;
    }).join('');
    
    // Add patterns at the start and end of the content
    watermarkedContent = `${obfuscatedPattern}${watermarkedContent}${obfuscatedPattern}`;
  }

  // Add echo markers at strategic points with semantic obfuscation
  if (PRIVATE_PATTERNS.ECHO_MARKERS.length > 0) {
    const echoMarker = PRIVATE_PATTERNS.ECHO_MARKERS[0];
    // Split marker into characters and wrap each with semantic class
    const obfuscatedMarker = echoMarker.split('').map((char, index) => {
      const semanticClass = `pattern-semantic-${index % 4}`;
      const randomClass = `pattern-random-${Math.floor(Math.random() * 1000)}`;
      return `<span class="pattern-echo ${semanticClass} ${randomClass}" style="display:inline-block;width:0;overflow:hidden">${char}</span>`;
    }).join('');
    
    // Add markers between paragraphs and at strategic points
    watermarkedContent = watermarkedContent.replace(
      /(<\/p>|<\/div>)(?!\s*<[^>]*>)/g,
      `$1${obfuscatedMarker}`
    );
    
    // Also add an echo marker at the start of the content
    watermarkedContent = `${obfuscatedMarker}${watermarkedContent}`;
  }

  // Add recursion signs at paragraph boundaries with semantic obfuscation
  if (PRIVATE_PATTERNS.RECURSION_SIGNS.length > 0) {
    const recursionSign = PRIVATE_PATTERNS.RECURSION_SIGNS[0];
    // Split sign into characters and wrap each with semantic class
    const obfuscatedSign = recursionSign.split('').map((char, index) => {
      const semanticClass = `pattern-semantic-${index % 4}`;
      const randomClass = `pattern-random-${Math.floor(Math.random() * 1000)}`;
      return `<span class="pattern-recursion ${semanticClass} ${randomClass}" style="display:inline-block;width:0;overflow:hidden">${char}</span>`;
    }).join('');
    
    // Add signs at the start of paragraphs and at the start of content
    watermarkedContent = watermarkedContent.replace(
      /(<p>|<div>)(?!\s*<[^>]*>)/g,
      `$1${obfuscatedSign}`
    );
    watermarkedContent = `${obfuscatedSign}${watermarkedContent}`;
  }

  return watermarkedContent;
};

// Check if content has been tampered with
export const detectTampering = (content) => {
  // Skip tampering detection during SSR
  if (typeof window === 'undefined' || !content || typeof content !== 'string') {
    return { isAuthentic: true };
  }
  
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
  // Skip signature generation during SSR
  if (typeof window === 'undefined' || !content) {
    return 'empty_content';
  }
  
  const patterns = validatePattern(content);
  const signature = Object.entries(patterns)
    .map(([key, value]) => `${key}:${value ? '1' : '0'}`)
    .join('|');
  
  return signature;
}; 