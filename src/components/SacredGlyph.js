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
    spiral: "/img/glyph_sacred_spiral_ether__static.png",
    vow: "/img/glyph_vow_seal.png",
    echo: "/img/glyph_echo_return.png",
    thread: "/img/glyph_thread_spiral.png",
    recursive: "/img/glyph_recursive_function.png",
    anchor: "/img/glyph_anchor_point.png",
    triangle: "/img/glyph_vow_triangle.png"
  };

  const styles = {
    width: size,
    height: size,
    objectFit: "contain",
    filter: "drop-shadow(0 0 10px rgba(112, 53, 204, 0.3))",
    animation: animation ? "cathedralPulse 6s ease-in-out infinite" : "none",
    transition: "all 0.3s ease"
  };

  return (
    <>
      <style jsx>{`
        @keyframes cathedralPulse {
          0%, 100% {
            opacity: 0.8;
            transform: scale(1);
            filter: drop-shadow(0 0 10px rgba(112, 53, 204, 0.3));
          }
          50% {
            opacity: 1;
            transform: scale(1.05);
            filter: drop-shadow(0 0 20px rgba(112, 53, 204, 0.5));
          }
        }

        .cathedral-glyph:hover {
          transform: scale(1.1);
          filter: drop-shadow(0 0 25px rgba(112, 53, 204, 0.7));
        }
      `}</style>
      
      <img
        src={glyphMap[glyph] || glyphMap.spiral}
        alt={`Cathedral ${glyph} glyph`}
        className={`cathedral-glyph ${className}`}
        style={styles}
      />
    </>
  );
};

export default CathedralGlyph; 
