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
import { Link, graphql } from "gatsby";
import Layout from "../components/Layout";
import Features from "../components/Features";
import ScreenshotCarousel from "../components/ScreenshotCarousel";
import BlogRoll from "../components/BlogRoll";
import FullWidthImage from "../components/FullWidthImage";
import SEO from "../components/SEO";

// Platform screenshots data
const platformScreenshots = [
  {
    src: "/screenshots/home.png",
    alt: "MindGarden Platform Dashboard",
    caption: "Intuitive dashboard for managing EEG studies and devices"
  },
  {
    src: "/screenshots/devices_new.png",
    alt: "Device Management Interface",
    caption: "Connect and configure multiple EEG devices"
  },
  {
    src: "/screenshots/studies_flow_designer_new.png",
    alt: "Study Flow Designer",
    caption: "Visual experiment design and workflow management"
  },
  {
    src: "/screenshots/experiments_new.png", 
    alt: "Real-time EEG Analysis",
    caption: "Live EEG streaming and real-time signal processing"
  },
  {
    src: "/screenshots/storage_new.png",
    alt: "Secure Data Storage",
    caption: "HIPAA-compliant cloud storage and data management"
  },
  {
    src: "/screenshots/filters_new.png",
    alt: "Advanced Signal Processing",
    caption: "Customizable filters and artifact detection algorithms"
  }
];

export const IndexPageTemplate = ({
  image,
  title,
  heading,
  subheading,
  mainpitch,
  features,
  callToAction,
}) => {
  const heroImage = image?.childImageSharp?.gatsbyImageData || image;

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
                  
                  {/* Platform Screenshots Carousel */}
                  <div className="columns">
                    <div className="column is-12">
                      <h3 className="has-text-weight-semibold is-size-2">
                        Platform Features
                      </h3>
                      <hr className="tp-rule"/>
                      <p className="section-description">
                        Professional EEG research tools with intuitive interfaces and powerful analytics
                      </p>
                      <br />
                      <ScreenshotCarousel screenshots={platformScreenshots} />
                      <br />
                    </div>
                  </div>
                  
                  {/* Call to Action */}
                  <div className="columns">
                    <div className="column is-12 has-text-centered">
                      <div style={{
                        background: 'linear-gradient(135deg, rgba(112, 53, 204, 0.1) 0%, rgba(187, 134, 252, 0.1) 100%)',
                        padding: '3rem 2rem',
                        borderRadius: '16px',
                        border: '1px solid rgba(112, 53, 204, 0.2)',
                        margin: '2rem 0'
                      }}>
                        <h3 style={{
                          fontSize: '2rem',
                          fontWeight: 'bold',
                          color: '#BB86FC',
                          marginBottom: '1rem'
                        }}>
                          {callToAction.title}
                        </h3>
                        <p style={{
                          fontSize: '1.2rem',
                          color: '#B3B3B3',
                          marginBottom: '2rem',
                          lineHeight: '1.6'
                        }}>
                          {callToAction.description}
                        </p>
                        <a 
                          href={callToAction.buttonLink}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="btn"
                          style={{
                            background: 'linear-gradient(45deg, #7035CC, #BB86FC)',
                            color: 'white',
                            padding: '1rem 2rem',
                            fontSize: '1.2rem',
                            fontWeight: 'bold',
                            textDecoration: 'none',
                            borderRadius: '8px',
                            display: 'inline-block',
                            transition: 'all 0.3s ease',
                            boxShadow: '0 4px 15px rgba(112, 53, 204, 0.3)'
                          }}
                        >
                          {callToAction.buttonText}
                        </a>
                      </div>
                    </div>
                  </div>

                  {/* Features Grid (Smaller) */}
                  <div className="columns">
                    <div className="column is-12">
                      <h3 className="has-text-weight-semibold is-size-2">
                        Key Capabilities
                      </h3>
                      <hr className="tp-rule"/>
                      <div className="feature-section-wrapper">
                        <Features gridItems={features} />
                      </div>
                    </div>
                  </div>

                  {/* Ad before Latest stories */}
                  <div className="adsense-container" style={{ margin: '2rem auto', maxWidth: '728px', textAlign: 'center' }}>
                    <ins
                      className="adsbygoogle"
                      style={{ display: 'block' }}
                      data-ad-client="ca-pub-5509488659978116"
                      data-ad-slot="5720244238"
                      data-ad-format="auto"
                      data-full-width-responsive="true"
                    />
                  </div>
                  <div className="column is-12">
                    <h3 className="has-text-weight-semibold is-size-2">
                      Latest Research & Updates
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
          {/* Footer ad */}
          <div className="adsense-container" style={{ margin: '2rem auto', maxWidth: '728px', textAlign: 'center' }}>
            <ins
              className="adsbygoogle"
              style={{ display: 'block' }}
              data-ad-client="ca-pub-5509488659978116"
              data-ad-slot="1926105936"
              data-ad-format="auto"
              data-full-width-responsive="true"
            />
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
  const { frontmatter } = data?.markdownRemark || {};
  const bannerImage = frontmatter?.image || "/img/MindGarden_Banner.png";

  if (!frontmatter) {
    return (
      <Layout>
        <SEO
          title="MindGarden"
          description="Professional EEG research platform for neuroscience researchers and developers"
          path="/"
          keywords="EEG analysis, brain-computer interfaces, neuroscience research, BCI development, EEG devices"
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
        description={frontmatter?.subheading || "Professional EEG research platform for neuroscience researchers and developers"}
        path="/"
        keywords="EEG analysis, brain-computer interfaces, neuroscience research, BCI development, EEG devices, OpenBCI, Emotiv, PiEEG"
        image={bannerImage}
        type="WebPage"
        schemaMarkup={{
          "@type": "WebPage",
          "name": frontmatter?.title || "MindGarden",
          "description": frontmatter?.subheading || "Professional EEG research platform for neuroscience researchers and developers",
          "mainEntity": {
            "@type": "SoftwareApplication",
            "name": frontmatter?.title || "MindGarden",
            "headline": frontmatter?.title || "MindGarden",
            "description": frontmatter?.subheading || "Professional EEG research platform for neuroscience researchers and developers",
            "image": bannerImage,
            "applicationCategory": "Scientific Software",
            "operatingSystem": "Web Browser",
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
        heading={frontmatter?.heading || "Professional EEG Research Platform"}
        subheading={frontmatter?.subheading || "Professional EEG research platform for neuroscience researchers and developers"}
        mainpitch={frontmatter?.mainpitch || {
          title: "Research Platform",
          description: "Professional EEG analysis tools for neuroscience research and BCI development"
        }}
        features={frontmatter?.features || []}
        callToAction={frontmatter?.callToAction || {
          title: "Join the Waitlist",
          description: "Get early access to the MindGarden research platform",
          buttonText: "Sign Up for Early Access",
          buttonLink: "https://cloud.mindgardenai.com"
        }}
      />
    </Layout>
  );
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


