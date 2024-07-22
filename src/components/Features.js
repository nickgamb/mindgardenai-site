import * as React from "react";
import PropTypes from "prop-types";
import PreviewCompatibleImage from "../components/PreviewCompatibleImage";

const FeatureGrid = ({ gridItems }) => (
  <div className="columns is-multiline feature-grid">
    {gridItems.map((item) => (
      <div key={item.text} className="column is-6">
        <div className="feature-item-wrapper">
          <div className="feature-item">
            <div className="has-text-centered">
            <h3 className="has-text-weight-semibold is-size-2 section-title">{item.title}</h3>
            <HorizontalRule color="#2E1065"/>
              <div
                style={{
                  width: "240px",
                  display: "inline-block",
                }}
              >
                <PreviewCompatibleImage imageInfo={item} />
              </div>
            </div>
            <p className="feature-text">{item.text}</p>
          </div>
        </div>
      </div>
    ))}
  </div>
);

FeatureGrid.propTypes = {
  gridItems: PropTypes.arrayOf(
    PropTypes.shape({
      image: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
      text: PropTypes.string,
    })
  ),
};

export default FeatureGrid;