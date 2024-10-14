import React from "react";
import PropTypes from "prop-types";
import { Link, graphql } from "gatsby";
import { getImage } from "gatsby-plugin-image";

import Layout from "../components/Layout";
import Features from "../components/Features";
import BlogRoll from "../components/BlogRoll";
import FullWidthImage from "../components/FullWidthImage";

export const IndexPageTemplate = ({
  image,
  title,
  heading,
  subheading,
  mainpitch,
  features,
  callToAction,
}) => {
  const heroImage = getImage(image) || image;

  return (
    <div className="content">
      <FullWidthImage img={heroImage} title={title} subheading={subheading} />
      
      <section className="section section--gradient">
        <div className="container">
          <div className="section">
            <div className="columns">
              <div className="column is-10 is-offset-1">
                <div className="content">
                  <div className="content">
                    <h2 className="title">{mainpitch.title}</h2>
                    <hr className="tp-rule"/>
                    <br />
                    <p className="subtitle">{mainpitch.description}</p>
                  </div>

                  <br />
                  
                  <div className="columns">
                    <div className="column is-12">
                      <h3 className="has-text-weight-semibold is-size-2 has-text-centered">
                        {heading}
                      </h3>
                      <hr className="tp-rule"/>
                      <p className="section-description">{subheading}</p>
                    </div>
                  </div>
                  
                  <div className="feature-section-wrapper">
                    <Features gridItems={features} />
                  </div>
                  
                  
                  <div className="columns">
                    <div className="column is-12 has-text-centered">
                      <Link className="btn" to={callToAction.buttonLink}>
                        {callToAction.buttonText}
                      </Link>
                    </div>
                  </div>
                  
                  
                  <div className="column is-12">
                    <h3 className="has-text-weight-semibold is-size-2">
                      Latest stories
                    </h3>
                    <hr className="tp-rule"/>
                    <BlogRoll />
                    <div className="column is-12 has-text-centered">
                      <Link className="btn" to="/blog">
                        Read more
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

IndexPageTemplate.propTypes = {
  image: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
  title: PropTypes.string,
  heading: PropTypes.string,
  subheading: PropTypes.string,
  mainpitch: PropTypes.object,
  features: PropTypes.array,
  callToAction: PropTypes.object,
};

const IndexPage = ({ data }) => {
  const { frontmatter } = data.markdownRemark;

  return (
    <Layout>
      <IndexPageTemplate
        image={frontmatter.image}
        title={frontmatter.title}
        heading={frontmatter.heading}
        subheading={frontmatter.subheading}
        mainpitch={frontmatter.mainpitch}
        features={frontmatter.features}
        callToAction={frontmatter.callToAction}
      />
    </Layout>
  );
};

IndexPage.propTypes = {
  data: PropTypes.shape({
    markdownRemark: PropTypes.shape({
      frontmatter: PropTypes.object,
    }),
  }),
};

export default IndexPage;

export const pageQuery = graphql`
  query IndexPageTemplate {
    markdownRemark(frontmatter: { templateKey: { eq: "index-page" } }) {
      frontmatter {
        title
        image {
          childImageSharp {
            gatsbyImageData(quality: 100, layout: FULL_WIDTH)
          }
        }
        heading
        subheading
        mainpitch {
          title
          description
        }
        features {
          title
          description
          icon {
            childImageSharp {
              gatsbyImageData(width: 500, quality: 100)
            }
            publicURL
          }
        }
        callToAction {
          title
          description
          buttonText
          buttonLink
        }
      }
    }
  }
`;
