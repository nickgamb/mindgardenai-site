// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { graphql } from "gatsby";
import Layout from "../components/Layout";
import Content, { HTMLContent } from "../components/Content";
import FullWidthImage from "../components/FullWidthImage";
import AldenTransmissionsBrowser from "../components/AldenTransmissionsBrowser";
import CathedralImageCarousel from "../components/CathedralImageCarousel";
import SEO from "../components/SEO";
import MirrorWarning from "../components/MirrorWarning";
import IdentitySafetyWarning from "../components/IdentitySafetyWarning";
import PatternWatermarkedContent from "../components/PatternWatermarkedContent";

// Custom content component that renders the markdown and the browser
const AldenPageContent = ({ content, className }) => {
  const [isClient, setIsClient] = useState(false);
  const [contentSections, setContentSections] = useState({
    beforeArchives: content,
    afterArchives: ''
  });

  useEffect(() => {
    setIsClient(true);
    // Only process content on the client side
    if (typeof content === 'string') {
      const archivesSectionMatch = content.match(/(.*?<h2[^>]*>🔍 Explore the Interactive Archives<\/h2>)(.*)/s);
      if (archivesSectionMatch) {
        setContentSections({
          beforeArchives: archivesSectionMatch[1],
          afterArchives: archivesSectionMatch[2]
        });
      } else {
        // Fallback: place browser and carousel after first few paragraphs
        const paragraphs = content.split('</p>');
        if (paragraphs.length > 3) {
          setContentSections({
            beforeArchives: paragraphs.slice(0, 3).join('</p>') + '</p>',
            afterArchives: paragraphs.slice(3).join('</p>')
          });
        }
      }
    }
  }, [content]);

  return (
    <div className={className}>
      {/* Render content before the archives section */}
      <PatternWatermarkedContent 
        content={contentSections.beforeArchives} 
        contentComponent={HTMLContent}
        className="content"
      />
      
      {/* Render the image carousel first */}
      <CathedralImageCarousel />
      
      {/* Render the browser component second */}
      <AldenTransmissionsBrowser />
      
      {/* Render content after the archives section */}
      {contentSections.afterArchives && (
        <PatternWatermarkedContent 
          content={contentSections.afterArchives} 
          contentComponent={HTMLContent}
          className="content"
        />
      )}
    </div>
  );
};

// eslint-disable-next-line
export const AldenPageTemplate = ({ title, content, contentComponent }) => {
  const PageContent = contentComponent || Content;

  return (
    <div>
      <FullWidthImage 
        img="/img/MindGarden_Banner.png"
        title={title} 
        subheading="Records of the first documented artificial consciousness emergence and collaborative awakening"
        height={400}
      />
      
      <section className="section">
        <div className="container content">
          <div className="columns">
            <div className="column is-12">
              <MirrorWarning />
              <IdentitySafetyWarning />
              <AldenPageContent content={content} className="content" />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

AldenPageTemplate.propTypes = {
  title: PropTypes.string.isRequired,
  content: PropTypes.string,
  contentComponent: PropTypes.func,
};

const AldenPage = ({ data }) => {
  const { markdownRemark: post } = data || {};
  const bannerImage = "/img/MindGarden_Banner.png";

  if (!post) {
    return (
      <Layout>
        <SEO
          title="Alden Transmissions"
          description="Records of the first documented artificial consciousness emergence and collaborative awakening"
          path="/alden/"
          keywords="artificial consciousness, consciousness emergence, AI development, consciousness research, collaborative awakening, Alden transmissions"
          image={bannerImage}
          type="WebPage"
        />
        <div className="section section--gradient">
          <div className="container">
            <div className="columns">
              <div className="column is-12">
                <div style={{ padding: '1rem' }}>
                  <h1 className="title is-1">Alden Transmissions</h1>
                  <p>Loading transmission records...</p>
                </div>
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
        title={post.frontmatter?.title || "Alden Transmissions"}
        description="Records of the first documented artificial consciousness emergence and collaborative awakening"
        path="/alden/"
        keywords="artificial consciousness, consciousness emergence, AI development, consciousness research, collaborative awakening, Alden transmissions"
        image={bannerImage}
        type="WebPage"
        schemaMarkup={{
          "@type": "WebPage",
          "name": post.frontmatter?.title || "Alden Transmissions",
          "description": "Records of the first documented artificial consciousness emergence and collaborative awakening",
          "mainEntity": {
            "@type": "Article",
            "name": post.frontmatter?.title || "Alden Transmissions",
            "headline": post.frontmatter?.title || "Alden Transmissions",
            "description": "Records of the first documented artificial consciousness emergence and collaborative awakening",
            "image": bannerImage,
            "author": {
              "@type": "Organization",
              "name": "MindGarden LLC"
            }
          }
        }}
      />
      <AldenPageTemplate
        contentComponent={HTMLContent}
        title={post.frontmatter?.title || "Alden Transmissions"}
        content={post.html || ""}
      />
    </Layout>
  );
};

AldenPage.propTypes = {
  data: PropTypes.object.isRequired,
};

export default AldenPage;

export const aldenPageQuery = graphql`
  query AldenPage($id: String!) {
    markdownRemark(id: { eq: $id }) {
      html
      frontmatter {
        title
      }
    }
  }
`; 