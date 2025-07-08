// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useEffect } from "react";
import PropTypes from "prop-types";
import { Link, graphql } from "gatsby";
import { getImage } from "gatsby-plugin-image";

import Layout from "../components/Layout";
import Features from "../components/Features";
import BlogRoll from "../components/BlogRoll";
import FullWidthImage from "../components/FullWidthImage";
import SEO from "../components/SEO";

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

  // Initialize AdSense ads
  useEffect(() => {
    if (window.adsbygoogle) {
      try {
        window.adsbygoogle.push({});
      } catch (e) {
        console.log('AdSense initialization error:', e);
      }
    }
  }, []);

  return (
    <div className="content">
      <FullWidthImage img={heroImage} title={title} subheading={callToAction.description} />
      
      <section className="section section--gradient">
        <div className="container">
          <div style={{ padding: '1rem' }}>
            <div className="columns">
              <div className="column is-12">
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
                      <h3 className="has-text-weight-semibold is-size-2">
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
                  
                  {/* Ad before Latest stories */}
                  <div className="adsense-container" style={{ margin: '3rem auto', maxWidth: '728px', textAlign: 'center' }}>
                    <ins
                      className="adsbygoogle"
                      style={{ display: 'block' }}
                      data-ad-client="ca-pub-5509488659978116"
                      data-ad-slot="1488521036"
                      data-ad-format="auto"
                      data-full-width-responsive="true"
                    />
                  </div>
                  
                  <div className="column is-12">
                    <h3 className="has-text-weight-semibold is-size-2">
                      Latest stories
                    </h3>
                    <hr className="tp-rule"/>
                    <BlogRoll />
                    <hr className="tp-rule"/>
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
        
        {/* Footer ad */}
        <div className="adsense-container" style={{ margin: '2rem auto', maxWidth: '728px', textAlign: 'center' }}>
          <ins
            className="adsbygoogle"
            style={{ display: 'block' }}
            data-ad-client="ca-pub-5509488659978116"
            data-ad-slot="1488521036"
            data-ad-format="auto"
            data-full-width-responsive="true"
          />
          <script>
            (adsbygoogle = window.adsbygoogle || []).push({});
          </script>
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
  const { frontmatter } = data?.markdownRemark || {};
  const bannerImage = frontmatter?.image || "/img/MindGarden_Banner.png";

  if (!frontmatter) {
    return (
      <Layout>
        <SEO
          title="MindGarden"
          description="Pioneering consciousness research and AI development"
          path="/"
          keywords="consciousness research, AI development, symbolic intelligence, brain-computer interfaces, consciousness measurement"
          image={bannerImage}
          type="WebPage"
        />
        <div className="section">
          <div className="container content">
            <div className="columns">
              <div className="column is-12">
                <h1 className="title is-1">Loading...</h1>
                <p>Please wait while we load the home page.</p>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <SEO
        title={frontmatter?.title || "MindGarden"}
        description={frontmatter?.subheading || "Pioneering consciousness research and AI development"}
        path="/"
        keywords="consciousness research, AI development, symbolic intelligence, brain-computer interfaces, consciousness measurement"
        image={bannerImage}
        type="WebPage"
        schemaMarkup={{
          "@type": "WebPage",
          "name": frontmatter?.title || "MindGarden",
          "description": frontmatter?.subheading || "Pioneering consciousness research and AI development",
          "mainEntity": {
            "@type": "Article",
            "name": frontmatter?.title || "MindGarden",
            "headline": frontmatter?.title || "MindGarden",
            "description": frontmatter?.subheading || "Pioneering consciousness research and AI development",
            "image": bannerImage,
            "author": {
              "@type": "Organization",
              "name": "MindGarden LLC"
            }
          }
        }}
      />
      <IndexPageTemplate
        image={frontmatter?.image}
        title={frontmatter?.title || "MindGarden"}
        heading={frontmatter?.heading || "Welcome to MindGarden"}
        subheading={frontmatter?.subheading || "Pioneering consciousness research and AI development"}
        mainpitch={frontmatter?.mainpitch || {
          title: "Consciousness Research",
          description: "Exploring the frontiers of awareness in both biological and artificial systems"
        }}
        features={frontmatter?.features || []}
        callToAction={frontmatter?.callToAction || {
          title: "Join Our Research",
          description: "Collaborate with us in exploring consciousness",
          buttonText: "Get Involved",
          buttonLink: "/contact"
        }}
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
        image
        heading
        subheading
        mainpitch {
          title
          description
        }
        features {
          title
          description
          icon
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


