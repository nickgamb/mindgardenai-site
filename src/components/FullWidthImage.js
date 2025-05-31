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
import { GatsbyImage } from "gatsby-plugin-image";

export default function FullWidthImage(props) {
  const { height = 400, img, title, subheading } = props;

  return (
    <React.Fragment>
      <div
        className="margin-top-0"
        style={{
          display: "grid",
          alignItems: "center",
          width: "100%",
          height: height,
          overflow: "hidden",
          position: "relative"
        }}
      >
        {img?.url ? (
          <img
            src={img.url}
            style={{
              gridArea: "1/1",
              height: "100%",
              width: "100%",
              objectFit: "cover",
              objectPosition: "center center",
              display: "block"
            }}
            alt=""
          />
        ) : typeof img === 'string' ? (
          <img
            src={img}
            style={{
              gridArea: "1/1",
              height: "100%",
              width: "100%",
              objectFit: "cover",
              objectPosition: "center center",
              display: "block"
            }}
            alt=""
          />
        ) : (
          <GatsbyImage
            image={img}
            style={{
              gridArea: "1/1",
              height: "100%",
              width: "100%",
              objectFit: "cover",
              objectPosition: "center center"
            }}
            alt=""
            formats={["auto", "webp", "avif"]}
          />
        )}
        {(title || subheading) && (
          <div
            style={{
              gridArea: "1/1",
              position: "relative",
              placeItems: "center",
              display: "grid",
              zIndex: 2,
              width: "100%",
              height: "100%"
            }}
          >
            <div className="hero-content">
              {title && (
                <h1 className="hero-title">
                  {title}
                </h1>
              )}
              {subheading && (
                <h3 className="hero-subtitle">
                  {subheading}
                </h3>
              )}
            </div>
          </div>
        )}
      </div>
    </React.Fragment>
  );
}

FullWidthImage.propTypes = {
  img: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
  title: PropTypes.string,
  height: PropTypes.number,
  subheading: PropTypes.string,
};


