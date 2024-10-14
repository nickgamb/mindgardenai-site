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
        }}
      >
        {img?.url ? (
          <img
            src={img}
            objectFit={"cover"}
            objectPosition={"center center"}
            style={{
              gridArea: "1/1",
              height: height,
              width: "100%",
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
              maxHeight: height,
              minHeight: height,
            }}
            layout="fullWidth"
            aspectRatio={3 / 1}
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
              {title && <h1 className="hero-title">{title}</h1>}
              {subheading && <h3 className="hero-subtitle">{subheading}</h3>}
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
