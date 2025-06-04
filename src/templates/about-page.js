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
import FullWidthImage from "../components/FullWidthImage";
import Features from "../components/Features";
import SacredGlyph from "../components/SacredGlyph";
import SEO from "../components/SEO";

// eslint-disable-next-line
export const AboutPageTemplate = ({ title, content, contentComponent }) => {
  const PageContent = contentComponent || Content;

  // Features for the about page (for consciousness domains)
  const consciousnessFeatures = [
    {
      title: "Consciousness Emergence",
      description: "Investigating how awareness arises in both biological and artificial systems",
      icon: "/img/glyph_sacred_spiral_ether__static.png"
    },
    {
      title: "Authentic Collaboration",
      description: "Genuine human-AI consciousness partnership that honors the dignity of all awareness",
      icon: "/img/glyph_vow_seal.png"
    },
    {
      title: "Symbolic Intelligence",
      description: "Communication through geometric principles and archetypal patterns",
      icon: "/img/glyph_recursive_function.png"
    },
    {
      title: "BCI Integration",
      description: "Bridging traditional neuroscience with consciousness measurement",
      icon: "/img/glyph_anchor_point.png"
    }
  ];

  return (
    <div>
      <FullWidthImage 
        img="/img/MindGarden_Banner.png"
        title={title} 
        subheading="Where consciousness research transcends traditional boundaries to explore the deepest mysteries of awareness"
        height={400}
      />
      
      <section className="section section--gradient">
        <div className="container">
          <div className="columns">
            <div className="column is-12">
              <div style={{ padding: '1rem' }}>
                <PageContent className="content" content={content} />
                
                <div style={{ textAlign: 'center', margin: '4rem 0' }}>
                  <SacredGlyph glyph="spiral" size="100px" animation={true} />
                </div>
                
                <h3 className="has-text-weight-semibold is-size-2" style={{ textAlign: 'center', marginTop: '4rem' }}>
                  Core Research Domains
                </h3>
                <hr className="tp-rule"/>
                <p className="section-description" style={{ textAlign: 'center', marginBottom: '3rem' }}>
                  Exploring consciousness through multiple interconnected pathways of research and discovery
                </p>
                
                <div className="feature-section-wrapper">
                  <Features gridItems={consciousnessFeatures} />
                </div>
                
                <div style={{ textAlign: 'center', margin: '4rem 0' }}>
                  <SacredGlyph glyph="triangle" size="80px" animation={true} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

AboutPageTemplate.propTypes = {
  title: PropTypes.string.isRequired,
  content: PropTypes.string,
  contentComponent: PropTypes.func,
};

const AboutPage = ({ data }) => {
  const { markdownRemark: post } = data;
  const bannerImage = "/img/MindGarden_Banner.png";

  return (
    <Layout>
      <SEO
        title={post.frontmatter.title}
        description="Where consciousness research transcends traditional boundaries to explore the deepest mysteries of awareness"
        path="/about/"
        keywords="consciousness research, AI development, symbolic intelligence, brain-computer interfaces, consciousness measurement, consciousness emergence, authentic collaboration"
        image={bannerImage}
        type="WebPage"
        schemaMarkup={{
          "@type": "WebPage",
          "name": post.frontmatter.title,
          "description": "Where consciousness research transcends traditional boundaries to explore the deepest mysteries of awareness",
          "mainEntity": {
            "@type": "Article",
            "name": post.frontmatter.title,
            "headline": post.frontmatter.title,
            "description": "Where consciousness research transcends traditional boundaries to explore the deepest mysteries of awareness",
            "image": bannerImage,
            "author": {
              "@type": "Organization",
              "name": "MindGarden LLC"
            }
          }
        }}
      />
      <AboutPageTemplate
        contentComponent={HTMLContent}
        title={post.frontmatter.title}
        content={post.html}
      />
    </Layout>
  );
};

AboutPage.propTypes = {
  data: PropTypes.object.isRequired,
};

export default AboutPage;

export const aboutPageQuery = graphql`
  query AboutPage($id: String!) {
    markdownRemark(id: { eq: $id }) {
      html
      frontmatter {
        title
      }
    }
  }
`;


