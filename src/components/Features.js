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

const Features = ({ gridItems }) => (
  <div className="columns is-multiline">
    {gridItems.map((item) => (
      <div key={item.title} className="column is-6">
        <section className="section">
          <div className="feature-item" style={{
            background: 'linear-gradient(135deg, rgba(30, 30, 30, 0.8) 0%, rgba(45, 45, 45, 0.8) 100%)',
            padding: '1.5rem',
            borderRadius: '12px',
            border: '1px solid rgba(51, 51, 51, 0.5)',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            transition: 'all 0.3s ease',
            cursor: 'pointer'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-2px)';
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(112, 53, 204, 0.2)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = 'none';
          }}>
            
            <div className="feature-icon" style={{ 
              textAlign: 'center', 
              marginBottom: '1rem',
              flexShrink: 0
            }}>
              {item.icon && (
                <PreviewCompatibleImage
                  imageInfo={{
                    image: item.icon,
                    alt: `${item.title} icon`,
                  }}
                  style={{
                    width: '60px',
                    height: '60px',
                    margin: '0 auto',
                    filter: 'drop-shadow(0 2px 4px rgba(112, 53, 204, 0.3))'
                  }}
                />
              )}
            </div>
            
            <h4 style={{
              color: '#BB86FC',
              fontSize: '1.1rem',
              fontWeight: '600',
              marginBottom: '0.75rem',
              textAlign: 'center',
              lineHeight: '1.3'
            }}>
              {item.title}
            </h4>
            
            <p style={{
              color: 'rgba(179, 179, 179, 0.95)',
              fontSize: '0.9rem',
              lineHeight: '1.5',
              textAlign: 'center',
              margin: 0,
              flex: 1
            }}>
              {item.description}
            </p>
          </div>
        </section>
      </div>
    ))}
  </div>
);

Features.propTypes = {
  gridItems: PropTypes.arrayOf(
    PropTypes.shape({
      icon: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
      title: PropTypes.string,
      description: PropTypes.string,
    })
  ),
};

export default Features;


