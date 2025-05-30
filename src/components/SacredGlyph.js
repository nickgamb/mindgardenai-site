// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Sacred symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React from "react";

const SacredGlyph = ({ 
  size = "60px", 
  glyph = "spiral", 
  animate = true, 
  opacity = 0.6,
  color = "#7035CC" 
}) => {
  
  const glyphImages = {
    spiral: "/img/glyph_sacred_spiral_ether__static.png",
    vow: "/img/glyph_vow_seal.png",
    anchor: "/img/glyph_anchor_point.png",
    thread: "/img/glyph_thread_spiral.png",
    echo: "/img/glyph_echo_return.png",
    renewal: "/img/glyph_renewal_cycle.png",
    overlay: "/img/glyph_overlay_pattern.png",
    triangle: "/img/glyph_vow_triangle.png",
    recursive: "/img/glyph_recursive_function.png"
  };

  const animationStyle = animate ? {
    animation: "sacredPulse 6s ease-in-out infinite",
    transformOrigin: "center"
  } : {};

  return (
    <div style={{ 
      display: 'inline-block', 
      position: 'relative',
      ...animationStyle
    }}>
      <style jsx>{`
        @keyframes sacredPulse {
          0%, 100% { 
            transform: scale(1) rotate(0deg);
            opacity: ${opacity};
          }
          25% { 
            transform: scale(1.05) rotate(0.5deg);
            opacity: ${opacity * 1.2};
          }
          50% { 
            transform: scale(1.02) rotate(0deg);
            opacity: ${opacity * 0.8};
          }
          75% { 
            transform: scale(1.05) rotate(-0.5deg);
            opacity: ${opacity * 1.1};
          }
        }
        
        .sacred-glyph:hover {
          transform: scale(1.1);
          transition: transform 0.3s ease;
        }
      `}</style>
      
      <img
        src={glyphImages[glyph] || glyphImages.spiral}
        alt={`Sacred ${glyph} glyph`}
        className="sacred-glyph"
        style={{
          width: size,
          height: size,
          opacity: opacity,
          filter: `hue-rotate(${color === "#7035CC" ? "0deg" : "45deg"})`,
          transition: "all 0.3s ease"
        }}
      />
    </div>
  );
};

export default SacredGlyph; 