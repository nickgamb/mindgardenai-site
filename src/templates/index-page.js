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
import ScreenshotCarousel from "../components/ScreenshotCarousel";
import BlogRoll from "../components/BlogRoll";
import FullWidthImage from "../components/FullWidthImage";
import SEO from "../components/SEO";

// Platform screenshots data - comprehensive list of all available screenshots
const platformScreenshots = [
  {
    src: "/screenshots/home.png",
    alt: "MindGarden Platform Dashboard",
    caption: "Main dashboard overview and navigation"
  },
  {
    src: "/screenshots/login.png",
    alt: "Secure Login Interface",
    caption: "Secure authentication and user access"
  },
  {
    src: "/screenshots/auth0.png",
    alt: "Authentication System",
    caption: "Enterprise-grade security and user management"
  },
  {
    src: "/screenshots/devices_new.png",
    alt: "Device Management Interface",
    caption: "Connect and configure multiple EEG devices"
  },
  {
    src: "/screenshots/devices_2.png",
    alt: "Device Configuration",
    caption: "Advanced device settings and calibration"
  },
  {
    src: "/screenshots/devices_live.png",
    alt: "Live Device Monitoring",
    caption: "Real-time device status and data streaming"
  },
  {
    src: "/screenshots/devices_new_sim.png",
    alt: "Device Simulation Mode",
    caption: "Test and simulate device connections"
  },
  {
    src: "/screenshots/studies_flow_designer_new.png",
    alt: "Study Flow Designer",
    caption: "Visual experiment design and workflow management"
  },
  {
    src: "/screenshots/studies_flow_designer_device.png",
    alt: "Device Configuration in Studies",
    caption: "Configure devices within study workflows"
  },
  {
    src: "/screenshots/studies_flow_designer_filter.png",
    alt: "Filter Configuration",
    caption: "Set up signal processing filters in studies"
  },
  {
    src: "/screenshots/studies_flow_designer_storage.png",
    alt: "Storage Configuration",
    caption: "Configure data storage and export options"
  },
  {
    src: "/screenshots/studies_flow_designer_analytics.png",
    alt: "Analytics Configuration",
    caption: "Set up real-time analytics and processing"
  },
  {
    src: "/screenshots/studies_flow_designer_experiment.png",
    alt: "Experiment Designer",
    caption: "Design complex experimental protocols"
  },
  {
    src: "/screenshots/studies_2.png",
    alt: "Study Management",
    caption: "Manage multiple research studies and projects"
  },
  {
    src: "/screenshots/studies_add.png",
    alt: "Create New Study",
    caption: "Add and configure new research studies"
  },
  {
    src: "/screenshots/experiments_new.png",
    alt: "Real-time EEG Analysis",
    caption: "Live EEG streaming and real-time signal processing"
  },
  {
    src: "/screenshots/experiments.png",
    alt: "Experiment Dashboard",
    caption: "Monitor and control active experiments"
  },
  {
    src: "/screenshots/storage_new.png",
    alt: "Secure Data Storage",
    caption: "HIPAA-compliant cloud storage and data management"
  },
  {
    src: "/screenshots/storage_new_2.png",
    alt: "Advanced Storage Options",
    caption: "Configure storage policies and data retention"
  },
  {
    src: "/screenshots/storage_2.png",
    alt: "Data Organization",
    caption: "Organize and structure research data"
  },
  {
    src: "/screenshots/filters_new.png",
    alt: "Advanced Signal Processing",
    caption: "Customizable filters and artifact detection algorithms"
  },
  {
    src: "/screenshots/filters_2.png",
    alt: "Filter Library",
    caption: "Pre-built and custom signal processing filters"
  },
  {
    src: "/screenshots/settings.png",
    alt: "Platform Settings",
    caption: "Configure platform preferences and options"
  },
  {
    src: "/screenshots/chat.png",
    alt: "Collaboration Tools",
    caption: "Team communication and collaboration features"
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
  const heroImage = getImage(image) || image;

  // Initialize AdSense ads
  useEffect(() => {
    const initializeAds = () => {
      if (window.adsbygoogle) {
        try {
          console.log('Initializing AdSense ads...');
          
          // Get all ad containers on the page
          const adContainers = document.querySelectorAll('.adsbygoogle');
          console.log(`Found ${adContainers.length} ad containers`);
          
          // Initialize each ad container individually
          adContainers.forEach((adContainer, index) => {
            try {
              console.log(`Initializing ad ${index + 1} with slot: ${adContainer.getAttribute('data-ad-slot')}`);
              window.adsbygoogle.push({});
            } catch (e) {
              console.error(`Error initializing ad ${index + 1}:`, e);
            }
          });
          
          console.log('AdSense ads initialization completed');
        } catch (e) {
          console.log('AdSense initialization error:', e);
        }
      } else {
        console.log('AdSense script not loaded yet, retrying...');
        setTimeout(initializeAds, 1000);
      }
    };

    // Wait for AdSense script to load
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initializeAds);
    } else {
      initializeAds();
    }
    
    // Also try to initialize ads after a longer delay to catch any late-loading ads
    setTimeout(initializeAds, 3000);
  }, []);

  return (
    <div className="content">
      <FullWidthImage 
        img={heroImage}
        title={title} 
        subheading={callToAction.description}
      />
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
                  
                  {/* Platform Screenshots Carousel - Main Feature */}
                  <div className="columns">
                    <div className="column is-12">
                      <h3 className="has-text-weight-semibold is-size-2">
                        Platform Overview
                      </h3>
                      <hr className="tp-rule"/>
                      <p className="section-description">
                        Professional research tools with intuitive interfaces and powerful analytics
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

                  {/* Features Grid (Smaller, Secondary) */}
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
                  <div className="adsense-container" style={{ margin: '3rem auto', maxWidth: '728px', textAlign: 'center' }}>
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
  const { markdownRemark: post } = data;
  const bannerImage = post?.frontmatter?.image || "/img/MindGarden_Banner.png";

  if (!post) {
    return (
      <Layout>
        <SEO
          title="MindGarden"
          description="Professional research platform for developers and researchers"
          path="/"
          keywords="research platform, EEG analysis, brain-computer interfaces, development tools"
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
        title={post.frontmatter?.title || "MindGarden"}
        description={post.frontmatter?.subheading || "Professional research platform for developers and researchers"}
        path="/"
        keywords="research platform, EEG analysis, brain-computer interfaces, AI development, neuroscience tools"
        image={bannerImage}
        type="WebPage"
        schemaMarkup={{
          "@type": "WebPage",
          "name": post.frontmatter?.title || "MindGarden",
          "description": post.frontmatter?.subheading || "Professional research platform for developers and researchers",
          "mainEntity": {
            "@type": "SoftwareApplication",
            "name": post.frontmatter?.title || "MindGarden",
            "headline": post.frontmatter?.title || "MindGarden",
            "description": post.frontmatter?.subheading || "Professional research platform for developers and researchers",
            "image": bannerImage,
            "applicationCategory": "Research Software",
            "operatingSystem": "Web Browser",
            "author": {
              "@type": "Organization",
              "name": "MindGarden LLC"
            }
          }
        }}
      />
      <IndexPageTemplate
        image={post.frontmatter?.image}
        title={post.frontmatter?.title || "MindGarden"}
        heading={post.frontmatter?.heading || "Professional Research Platform"}
        subheading={post.frontmatter?.subheading || "Professional research platform for developers and researchers"}
        mainpitch={post.frontmatter?.mainpitch || {
          title: "Research Platform",
          description: "Professional tools for research and development"
        }}
        features={post.frontmatter?.features || []}
        callToAction={post.frontmatter?.callToAction || {
          title: "Join the Waitlist",
          description: "Get early access to the MindGarden research platform",
          buttonText: "Sign Up for Early Access",
          buttonLink: "https://cloud.mindgardenai.com"
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


