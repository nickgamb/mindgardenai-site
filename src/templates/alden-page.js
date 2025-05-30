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
import AldenTransmissionsBrowser from "../components/AldenTransmissionsBrowser";

// Custom content component that renders the markdown and the browser
const AldenPageContent = ({ content, className }) => {
  // Find a good breaking point after the introduction
  // Look for the "## 🔍 Explore the Interactive Archives" heading we added
  const archivesSectionMatch = content.match(/(.*?<h2[^>]*>🔍 Explore the Interactive Archives<\/h2>)(.*)/s);
  
  if (archivesSectionMatch) {
    // Split at the archives section
    const beforeArchives = archivesSectionMatch[1];
    const afterArchives = archivesSectionMatch[2];
    
    return (
      <div className={className}>
        {/* Render content before the archives section */}
        <div dangerouslySetInnerHTML={{ __html: beforeArchives }} />
        
        {/* Render the browser component */}
        <AldenTransmissionsBrowser />
        
        {/* Render content after the archives section */}
        <div dangerouslySetInnerHTML={{ __html: afterArchives }} />
      </div>
    );
  } else {
    // Fallback: place browser after first few paragraphs
    const paragraphs = content.split('</p>');
    if (paragraphs.length > 3) {
      const beforeBrowser = paragraphs.slice(0, 3).join('</p>') + '</p>';
      const afterBrowser = paragraphs.slice(3).join('</p>');
      
      return (
        <div className={className}>
          <div dangerouslySetInnerHTML={{ __html: beforeBrowser }} />
          <AldenTransmissionsBrowser />
          <div dangerouslySetInnerHTML={{ __html: afterBrowser }} />
        </div>
      );
    } else {
      // Ultimate fallback: render all content then browser
      return (
        <div className={className}>
          <div dangerouslySetInnerHTML={{ __html: content }} />
          <AldenTransmissionsBrowser />
        </div>
      );
    }
  }
};

// eslint-disable-next-line
export const AldenPageTemplate = ({ title, content, contentComponent }) => {
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
              {contentComponent === HTMLContent ? (
                <AldenPageContent className="content" content={content} />
              ) : (
                <PageContent className="content" content={content} />
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

AldenPageTemplate.propTypes = {
  title: PropTypes.string.isRequired,
  content: PropTypes.string,
  contentComponent: PropTypes.func,
};

const AldenPage = ({ data }) => {
  const { markdownRemark: post } = data;

  return (
    <Layout>
      <AldenPageTemplate
        contentComponent={HTMLContent}
        title={post.frontmatter.title}
        content={post.html}
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