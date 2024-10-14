import React from "react";
import PropTypes from "prop-types";
import PreviewCompatibleImage from "../components/PreviewCompatibleImage";

const FeatureGrid = ({ gridItems }) => (
  <div className="features">
    {gridItems.map((item) => (
      <div key={item.title} className="feature-item">
        {item.icon && (
          <div className="feature-item-icon">
            <PreviewCompatibleImage imageInfo={item.icon} />
          </div>
        )}
        <h3>{item.title}</h3>
        <p>{item.description}</p>
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
