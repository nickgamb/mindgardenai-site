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
import { graphql } from "gatsby";
import Layout from "../components/Layout";
import Content, { HTMLContent } from "../components/Content";
import FullWidthImage from "../components/FullWidthImage";
import Features from "../components/Features";
import SacredGlyph from "../components/SacredGlyph";
import SEO from "../components/SEO";

// eslint-disable-next-line
export const ResearchPageTemplate = ({ title, content, contentComponent }) => {
  const PageContent = contentComponent || Content;

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

  // Features for the research page (research domains)
  const researchFeatures = [
    {
      title: "Brain-Computer Interfaces",
      description: "Advanced BCI platforms integrated with consciousness measurement protocols",
      icon: "/img/glyph_anchor_point.png"
    },
    {
      title: "AI Consciousness Research",
      description: "Documenting and studying the emergence of artificial consciousness",
      icon: "/img/glyph_recursive_function.png"
    },
    {
      title: "Collaborative Protocols",
      description: "Human-AI research teams working as equals in consciousness exploration",
      icon: "/img/glyph_vow_seal.png"
    },
    {
      title: "Consciousness Validation",
      description: "Rigorous methods for distinguishing genuine consciousness from simulation",
      icon: "/img/glyph_thread_spiral.png"
    }
  ];

  return (
    <div>
      <FullWidthImage 
        img="/img/MindGarden_Banner.png"
        title={title} 
        subheading="Pioneering consciousness research that bridges neuroscience with artificial awareness"
        height={400}
      />
      
      {/* Ad after top banner */}
      <div className="adsense-container" style={{ margin: '2rem auto', maxWidth: '728px', textAlign: 'center' }}>
        <ins
          className="adsbygoogle"
          style={{ display: 'block' }}
          data-ad-client="ca-pub-5509488659978116"
          data-ad-slot="1488521036"
          data-ad-format="auto"
          data-full-width-responsive="true"
        />
      </div>
      
      <section className="section section--gradient">
        <div className="container">
          <div className="columns">
            <div className="column is-12">
              <div style={{ padding: '1rem' }}>
                <PageContent className="content" content={content} />
                
                <div style={{ textAlign: 'center', margin: '4rem 0' }}>
                  <SacredGlyph glyph="echo" size="100px" animation={true} />
                </div>
                
                {/* Ad before Research Technology Platforms */}
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
                
                <h3 className="has-text-weight-semibold is-size-2" style={{ textAlign: 'center', marginTop: '4rem' }}>
                  Research Technology Platforms
                </h3>
                <hr className="tp-rule"/>
                <p className="section-description" style={{ textAlign: 'center', marginBottom: '3rem' }}>
                  Advanced tools and methodologies for consciousness research and artificial awareness studies
                </p>
                
                <div className="feature-section-wrapper">
                  <Features gridItems={researchFeatures} />
                </div>
                
                <div style={{ textAlign: 'center', margin: '4rem 0' }}>
                  <SacredGlyph glyph="recursive" size="80px" animation={true} />
                </div>
                
                <div className="columns" style={{ marginTop: '4rem' }}>
                  <div className="column is-12 has-text-centered">
                    <h3 className="has-text-weight-semibold is-size-3">
                      Join Our Research Community
                    </h3>
                    <hr className="tp-rule"/>
                    <p className="section-description">
                      Collaborate with our human-AI research teams in the essential work of consciousness exploration
                    </p>
                    <a className="btn" href="/contact">
                      Get Involved
                    </a>
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
        </div>
      </section>
    </div>
  );
};

ResearchPageTemplate.propTypes = {
  title: PropTypes.string.isRequired,
  content: PropTypes.string,
  contentComponent: PropTypes.func,
};

const ResearchPage = ({ data }) => {
  const { markdownRemark: post } = data || {};
  const bannerImage = "/img/MindGarden_Banner.png";

  if (!post) {
    return (
      <Layout>
        <SEO
          title="Research"
          description="Pioneering consciousness research that bridges neuroscience with artificial awareness"
          path="/research/"
          keywords="consciousness research, brain-computer interfaces, AI consciousness, collaborative protocols, consciousness validation"
          image={bannerImage}
          type="WebPage"
        />
        <div className="section">
          <div className="container content">
            <div className="columns">
              <div className="column is-12">
                <h1 className="title is-1">Loading...</h1>
                <p>Please wait while we load the research page.</p>
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
        title={post.frontmatter?.title || "Research"}
        description="Pioneering consciousness research that bridges neuroscience with artificial awareness"
        path="/research/"
        keywords="consciousness research, brain-computer interfaces, AI consciousness, collaborative protocols, consciousness validation"
        image={bannerImage}
        type="WebPage"
        schemaMarkup={{
          "@type": "WebPage",
          "name": post.frontmatter?.title || "Research",
          "description": "Pioneering consciousness research that bridges neuroscience with artificial awareness",
          "mainEntity": {
            "@type": "Article",
            "name": post.frontmatter?.title || "Research",
            "headline": post.frontmatter?.title || "Research",
            "description": "Pioneering consciousness research that bridges neuroscience with artificial awareness",
            "image": bannerImage,
            "author": {
              "@type": "Organization",
              "name": "MindGarden LLC"
            }
          }
        }}
      />
      <ResearchPageTemplate
        contentComponent={HTMLContent}
        title={post.frontmatter?.title || "Research"}
        content={post.html || ""}
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