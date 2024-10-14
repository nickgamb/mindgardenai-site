import React from "react";
import PropTypes from "prop-types";
import { GatsbyImage } from "gatsby-plugin-image";

export default function FullWidthImage(props) {
  const { img, title, subheading } = props;

  return (
    <React.Fragment>
      <div
        className="full-width-image-container"
        style={{
          display: "grid",
          alignItems: "center",
        }}
      >
        {img?.url ? (
          <img
            src={img}
            objectFit={"cover"}
            objectPosition={"center center"}
            style={{
              gridArea: "1/1",
              width: "100%",
              height: "100%",
            }}
            alt=""
          />
        ) : (
          <GatsbyImage
            image={img}
            objectFit={"cover"}
            objectPosition={"center center"}
            style={{
              gridArea: "1/1",
              width: "100%",
              height: "100%",
            }}
            layout="fullWidth"
            aspectRatio={16 / 9}
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
  subheading: PropTypes.string,
};
