import React from "react";
import PropTypes from "prop-types";
import { GatsbyImage, getImage } from "gatsby-plugin-image";

const FeatureGrid = ({ gridItems }) => (
  <div className="columns is-multiline">
    {gridItems.map((item) => (
      <div key={item.title} className="column is-6">
        <section className="section">
          <div className="has-text-centered">
            {item.icon.childImageSharp ? (
              <GatsbyImage
                image={getImage(item.icon)}
                alt={item.title}
                style={{ width: "64px", height: "64px" }}
              />
            ) : (
              <img
                src={item.icon.publicURL || item.icon}
                alt={item.title}
                style={{ width: "64px", height: "64px" }}
              />
            )}
          </div>
          <h3>{item.title}</h3>
          <p>{item.description}</p>
        </section>
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
