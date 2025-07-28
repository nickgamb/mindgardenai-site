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
import { graphql } from "gatsby";
import Layout from "../components/Layout";
import Content, { HTMLContent } from "../components/Content";
import ScreenshotCarousel from "../components/ScreenshotCarousel";
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

export const ResearchPageTemplate = ({ title, content, contentComponent }) => {
  const PageContent = contentComponent || Content;

  return (
    <section className="section section--gradient">
      <div className="container">
        <div className="columns">
          <div className="column is-10 is-offset-1">
            <div className="section">
              <h2 className="title is-size-3 has-text-weight-bold is-bold-light">
                {title}
              </h2>
              
              {/* Platform Screenshots Carousel */}
              <div style={{ margin: '2rem 0' }}>
                <ScreenshotCarousel screenshots={platformScreenshots} />
              </div>
              
              <PageContent className="content" content={content} />
              
              {/* Call to Action Section */}
              <div style={{
                background: 'linear-gradient(135deg, rgba(112, 53, 204, 0.1) 0%, rgba(187, 134, 252, 0.1) 100%)',
                padding: '3rem 2rem',
                borderRadius: '16px',
                border: '1px solid rgba(112, 53, 204, 0.2)',
                margin: '3rem 0',
                textAlign: 'center'
              }}>
                <h3 style={{
                  fontSize: '2rem',
                  fontWeight: 'bold',
                  color: '#BB86FC',
                  marginBottom: '1rem'
                }}>
                  Ready to Get Started?
                </h3>
                <p style={{
                  fontSize: '1.2rem',
                  color: '#B3B3B3',
                  marginBottom: '2rem',
                  lineHeight: '1.6'
                }}>
                  Join the waitlist for early access to the MindGarden research platform
                </p>
                <a 
                  href="https://cloud.mindgardenai.com"
                  target="_blank"
                  rel="noopener noreferrer"
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
                  Join Waitlist
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

ResearchPageTemplate.propTypes = {
  title: PropTypes.string.isRequired,
  content: PropTypes.string,
  contentComponent: PropTypes.func,
};

const ResearchPage = ({ data }) => {
  const { markdownRemark: post } = data;

  return (
    <Layout>
      <SEO
        title={post.frontmatter.title}
        description="Professional EEG research platform with advanced analysis tools for neuroscience researchers and BCI developers"
        path="/research"
        keywords="EEG research, brain-computer interfaces, neuroscience platform, BCI development, EEG analysis tools"
        image="/img/MindGarden_Banner.png"
        type="WebPage"
      />
      <ResearchPageTemplate
        contentComponent={HTMLContent}
        title={post.frontmatter.title}
        content={post.html}
      />
    </Layout>
  );
};

ResearchPage.propTypes = {
  data: PropTypes.object.isRequired,
};

export default ResearchPage;

export const researchPageQuery = graphql`
  query ResearchPage($id: String!) {
    markdownRemark(id: { eq: $id }) {
      html
      frontmatter {
        title
      }
    }
  }
`; 