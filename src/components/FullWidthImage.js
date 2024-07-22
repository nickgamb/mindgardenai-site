import React from "react";
import PropTypes from "prop-types";
import { GatsbyImage } from "gatsby-plugin-image";

export default function FullWidthImage(props) {
  const {
    height = 400,
    img,
    title,
    subheading,
    imgPosition = "center",
  } = props;

  return (
    <div
      className="full-width-image-container"
      style={{
        display: "grid",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {img?.url ? (
        <img
          src={img}
          style={{
            gridArea: "1/1",
            height: "100%",
            width: "100%",
            objectFit: "cover",
            objectPosition: imgPosition,
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
            objectPosition: imgPosition,
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
            display: "grid",
            placeItems: "center",
            textAlign: "center",
          }}
        >
          {title && (
            <h1
              className="has-text-weight-bold is-size-3-mobile is-size-2-tablet is-size-1-widescreen"
              style={{
                boxShadow: "#7035cc1a 0.5rem -5px 0px",
                backgroundColor: "#7035cc9c",
                color: "white",
                lineHeight: "1",
                padding: "0.25em",
                margin: "0",
              }}
            >
              {title}
            </h1>
          )}
          {subheading && (
            <h3
              className="has-text-weight-bold is-size-5-mobile is-size-5-tablet is-size-4-widescreen"
              style={{
                boxShadow: "#7035cc1a 0.5rem -5px 0px",
                backgroundColor: "#7035cc9c",
                color: "white",
                lineHeight: "1",
                padding: "0.25rem",
                marginTop: "0.5rem",
              }}
            >
              {subheading}
            </h3>
          )}
        </div>
      )}
    </div>
  );
}

FullWidthImage.propTypes = {
  img: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
  title: PropTypes.string,
  height: PropTypes.number,
  subheading: PropTypes.string,
};