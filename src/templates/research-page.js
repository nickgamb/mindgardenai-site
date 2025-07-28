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