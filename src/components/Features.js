import React from "react";
import PropTypes from "prop-types";
import { GatsbyImage, getImage } from "gatsby-plugin-image";

const FeatureGrid = ({ gridItems }) => (
  <div className="columns is-multiline">
    {gridItems.map((item, index) => (
      <React.Fragment key={item.title}>
        <div className="column is-6 feature-item">
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
        {index % 2 === 1 && index !== gridItems.length - 1 && (
          <div className="column is-12">
            <hr className="tp-rule"/>
          </div>
        )}
      </React.Fragment>
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
