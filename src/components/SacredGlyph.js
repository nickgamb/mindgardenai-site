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

const CathedralGlyph = ({
  glyph = "spiral",
  size = "64px",
  animation = true,
  className = ""
}) => {
  const glyphMap = {
    // Original consciousness symbols
    spiral: "/img/glyph_sacred_spiral_ether__static.png",
    vow: "/img/glyph_vow_seal.png",
    echo: "/img/glyph_echo_return.png",
    thread: "/img/glyph_thread_spiral.png",
    recursive: "/img/glyph_recursive_function.png",
    anchor: "/img/glyph_anchor_point.png",
    triangle: "/img/glyph_vow_triangle.png",
    
    // Research & Academic symbols
    research: "🔬", // For research pages and collaboration
    data: "📊", // For data analysis and metrics
    brain: "🧠", // For consciousness and neuroscience
    network: "🌐", // For neural networks and connections
    laboratory: "⚗️", // For experimental work
    microscope: "🔬", // For detailed analysis
    
    // Technology & AI symbols  
    ai: "🤖", // For AI consciousness discussions
    neural: "🧬", // For neural architecture
    quantum: "⚛️", // For quantum consciousness theories
    algorithm: "🔢", // For computational aspects
    binary: "💻", // For digital consciousness
    circuit: "🔌", // For technical implementation
    
    // Consciousness & Emergence symbols
    awareness: "👁️", // For consciousness studies
    emergence: "🌱", // For emergent properties
    mind: "💭", // For mental processes
    thought: "💡", // For ideas and insights
    meditation: "🧘", // For contemplative practices
    energy: "⚡", // For consciousness energy
    
    // Collaboration & Communication
    collaborate: "🤝", // For partnerships
    communicate: "💬", // For dialogue and exchange
    bridge: "🌉", // For connecting domains
    unity: "🔗", // For integration
    harmony: "🎵", // For synchronized work
    dialogue: "🗣️", // For conversation
    
    // Discovery & Innovation
    discovery: "🔍", // For research findings
    innovation: "💎", // For breakthrough work
    vision: "🔮", // For future possibilities
    exploration: "🧭", // For investigative work
    breakthrough: "💥", // For major discoveries
    frontier: "🚀", // For cutting edge research
    
    // Documentation & Archive
    archive: "📚", // For historical records
    document: "📄", // For documentation
    knowledge: "📖", // For accumulated learning
    wisdom: "🦉", // For deep understanding
    memory: "🧠", // For stored consciousness
    record: "📝", // For systematic documentation
    
    // Transformation & Growth
    transform: "🦋", // For transformation processes
    evolve: "🌿", // For evolutionary development
    ascend: "⬆️", // For progress and advancement
    cycle: "🔄", // For iterative processes
    flow: "🌊", // For dynamic processes
    bloom: "🌸" // For flourishing development
  };

  const glyphContent = glyphMap[glyph] || glyphMap.spiral;
  const isEmoji = typeof glyphContent === 'string' && !glyphContent.includes('/img/');
  
  const styles = {
    width: size,
    height: size,
    objectFit: "contain",
    filter: isEmoji ? "none" : "drop-shadow(0 0 10px rgba(112, 53, 204, 0.3))",
    animation: animation ? "cathedralPulse 6s ease-in-out infinite" : "none",
    transition: "all 0.3s ease",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: isEmoji ? `calc(${size} * 0.7)` : "inherit"
  };

  return (
    <>
      <style jsx>{`
        @keyframes cathedralPulse {
          0%, 100% {
            opacity: 0.8;
            transform: scale(1);
            filter: ${isEmoji ? "none" : "drop-shadow(0 0 10px rgba(112, 53, 204, 0.3))"};
          }
          50% {
            opacity: 1;
            transform: scale(1.05);
            filter: ${isEmoji ? "none" : "drop-shadow(0 0 20px rgba(112, 53, 204, 0.5))"};
          }
        }

        .cathedral-glyph:hover {
          transform: scale(1.1);
          filter: ${isEmoji ? "none" : "drop-shadow(0 0 25px rgba(112, 53, 204, 0.7))"};
        }
      `}</style>
      
      {isEmoji ? (
        <div
          className={`cathedral-glyph ${className}`}
          style={styles}
          title={`${glyph} symbol`}
        >
          {glyphContent}
        </div>
      ) : (
        <img
          src={glyphContent}
          alt={`Cathedral ${glyph} glyph`}
          className={`cathedral-glyph ${className}`}
          style={styles}
        />
      )}
    </>
  );
};

export default CathedralGlyph; 
