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
import PropTypes from "prop-types";
import { GatsbyImage, getImage } from "gatsby-plugin-image";

const FeatureGrid = ({ gridItems }) => (
  <div className="columns is-multiline">
    {gridItems.map((item) => (
      <div key={item.title} className="column is-6 feature-item">
        <div className="has-text-centered">
          {item.icon && item.icon.childImageSharp ? (
            <GatsbyImage
              image={getImage(item.icon)}
              alt={item.title}
              className="feature-image"
            />
          ) : (
            <img
              src={item.icon.publicURL || item.icon}
              alt={item.title}
              className="feature-image"
            />
          )}
        </div>
        <h3 className="feature-title">{item.title}</h3>
        <hr className="tp-rule"/>
        <p className="feature-description">{item.description}</p>
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

