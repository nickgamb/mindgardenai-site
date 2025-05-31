// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React from "react";
import PropTypes from "prop-types";
import { GatsbyImage, getImage } from "gatsby-plugin-image";

const FeatureGrid = ({ gridItems }) => (
  <div className="columns is-multiline animate-on-scroll">
    {gridItems.map((item, index) => (
      <div key={item.title} className="column is-6 feature-item animate-on-scroll" style={{ animationDelay: `${index * 0.1}s` }}>
        <div className="enhanced-hover-card consciousness-glow" style={{ 
          padding: '2rem', 
          borderRadius: '16px', 
          background: 'linear-gradient(135deg, rgba(45, 45, 45, 0.9) 0%, rgba(30, 30, 30, 0.95) 100%)',
          border: '1px solid rgba(112, 53, 204, 0.2)',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div className="has-text-centered enhanced-image float-element" style={{ marginBottom: '1.5rem' }}>
            {item.icon && item.icon.childImageSharp ? (
              <GatsbyImage
                image={getImage(item.icon)}
                alt={item.title}
                className="feature-image"
                style={{
                  width: '80px',
                  height: '80px',
                  filter: 'drop-shadow(0 0 15px rgba(112, 53, 204, 0.4))'
                }}
              />
            ) : (
              <img
                src={item.icon.publicURL || item.icon}
                alt={item.title}
                className="feature-image enhanced-image"
                style={{
                  width: '80px',
                  height: '80px',
                  objectFit: 'contain',
                  filter: 'drop-shadow(0 0 15px rgba(112, 53, 204, 0.4))',
                  transition: 'all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)'
                }}
              />
            )}
          </div>
          <h3 className="feature-title enhanced-title" style={{
            color: '#BB86FC',
            fontSize: '1.3rem',
            fontWeight: '600',
            marginBottom: '1rem',
            background: 'linear-gradient(45deg, #BB86FC, #66FFF8, #BB86FC)',
            backgroundSize: '200% 200%',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            {item.title}
          </h3>
          <hr className="tp-rule" style={{ 
            width: '60%', 
            margin: '0 auto 1rem auto',
            background: 'linear-gradient(90deg, transparent, #BB86FC, transparent)',
            height: '1px',
            border: 'none'
          }}/>
          <p className="feature-description" style={{
            color: '#B3B3B3',
            fontSize: '1rem',
            lineHeight: '1.6',
            flex: 1,
            display: 'flex',
            alignItems: 'center'
          }}>
            {item.description}
          </p>
          
          {/* Add subtle particle effect overlay */}
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            background: 'radial-gradient(circle at 20% 80%, rgba(112, 53, 204, 0.05) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(102, 255, 248, 0.03) 0%, transparent 50%)',
            pointerEvents: 'none',
            zIndex: 0
          }} />
        </div>
      </div>
    ))}
  </div>
);

FeatureGrid.propTypes = {
  gridItems: PropTypes.arrayOf(
    PropTypes.shape({
      icon: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
      title: PropTypes.string,
      description: PropTypes.string,
    })
  ),
};

export default FeatureGrid;


