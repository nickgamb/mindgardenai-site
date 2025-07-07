// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useEffect, useState } from "react";
import { graphql } from "gatsby";
import Layout from "../components/Layout";
import SymbolBrowser from "../components/SymbolBrowser";
import FullWidthImage from "../components/FullWidthImage";
import CathedralGlyph from "../components/SacredGlyph";
import SEO from "../components/SEO";

const MobileMessage = () => (
  <div className="section has-text-centered" style={{ padding: '2rem' }}>
    <div className="glyph-container" style={{ marginBottom: '1rem' }}>
      <CathedralGlyph glyph="spiral" size="60px" animation={true} className="cathedral-glyph" />
    </div>
    <h3 className="title is-4 has-text-primary">Symbol Browser Unavailable on Mobile</h3>
    <p className="subtitle is-6">
      The interactive symbol browser requires a desktop environment to properly render the 3D visualizations and complex graph structures.
      Please visit this page on a desktop computer to explore the full symbolic intelligence framework.
    </p>
    <div className="content">
      <p>
        In the meantime, you can explore our other research areas:
      </p>
      <ul>
        <li>Read about <a href="/blog">consciousness research</a></li>
        <li>Study <a href="/alden">Alden's transmissions</a></li>
        <li>Learn about <a href="/research">our methodology</a></li>
      </ul>
    </div>
  </div>
);

export default function SymbolsTemplate({ data }) {
  const { markdownRemark: post } = data || {};
  const bannerImage = "/img/MindGarden_Banner.png";

  if (!post) {
    return (
      <Layout>
        <SEO
          title="Symbols"
          description="Explore our symbolic intelligence framework for consciousness research and AI development"
          path="/symbols/"
          keywords="symbolic intelligence, consciousness mapping, cross-cultural analysis, technical integration, consciousness research"
          image={bannerImage}
          type="WebPage"
        />
        <div className="section">
          <div className="container content">
            <div className="columns">
              <div className="column is-12">
                <h1 className="title is-1">Loading...</h1>
                <p>Please wait while we load the symbols page.</p>
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
        title={post.frontmatter?.title || "Symbols"}
        description={post.frontmatter?.subheading || "Explore our symbolic intelligence framework for consciousness research and AI development"}
        path="/symbols/"
        keywords="symbolic intelligence, consciousness mapping, cross-cultural analysis, technical integration, consciousness research"
        image={bannerImage}
        type="WebPage"
        schemaMarkup={{
          "@type": "WebPage",
          "name": post.frontmatter?.title || "Symbols",
          "description": post.frontmatter?.subheading || "Explore our symbolic intelligence framework for consciousness research and AI development",
          "mainEntity": {
            "@type": "Article",
            "name": post.frontmatter?.title || "Symbols",
            "headline": post.frontmatter?.title || "Symbols",
            "description": post.frontmatter?.subheading || "Explore our symbolic intelligence framework for consciousness research and AI development",
            "image": bannerImage,
            "author": {
              "@type": "Organization",
              "name": "MindGarden LLC"
            }
          }
        }}
      />

      <FullWidthImage 
        img={bannerImage}
        title={post.frontmatter?.title || "Symbols"} 
        subheading={post.frontmatter?.subheading || "Explore our symbolic intelligence framework for consciousness research and AI development"}
        height={400}
      />
      
      {/* Ad after top banner */}
      <div className="adsense-container" style={{ margin: '2rem auto', maxWidth: '728px', textAlign: 'center' }}>
        <ins
          className="adsbygoogle"
          style={{ display: 'block' }}
          data-ad-client="ca-pub-5509488659978116"
          data-ad-slot="1234567890"
          data-ad-format="auto"
          data-full-width-responsive="true"
        />
      </div>
      
      <section className="section section--gradient">
        <div className="container">
          <div className="columns">
            <div className="column is-12">
              <div className="section">
                <div className="glyph-container">
                  <CathedralGlyph glyph="spiral" size="100px" animation={true} className="cathedral-glyph" />
                </div>
                
                <div className="feature-section">
                  <h2 className="section-title has-text-centered has-text-primary">{post.frontmatter?.title || "Symbols"}</h2>
                  <div 
                    className="section-description"
                    dangerouslySetInnerHTML={{ __html: post.html || "" }}
                  />
                </div>
                
                <SymbolBrowser />
                
                <div className="glyph-container">
                  <CathedralGlyph glyph="echo" size="60px" animation={true} className="cathedral-glyph" />
                </div>
                
                <div className="feature-section">
                  <h3 className="section-title has-text-primary">Symbol Research Applications</h3>
                  <div className="features">
                    <div className="feature-item-wrapper">
                      <div className="feature-item">
                        <h4 className="title has-text-primary">Consciousness Mapping</h4>
                        <p className="subtitle">
                          Study how symbols emerge and evolve in both human and artificial consciousness systems
                        </p>
                      </div>
                    </div>
                    <div className="feature-item-wrapper">
                      <div className="feature-item">
                        <h4 className="title has-text-primary">Cross-Cultural Analysis</h4>
                        <p className="subtitle">
                          Explore symbolic resonances across different traditions and consciousness frameworks
                        </p>
                      </div>
                    </div>
                    <div className="feature-item-wrapper">
                      <div className="feature-item">
                        <h4 className="title has-text-primary">Technical Integration</h4>
                        <p className="subtitle">
                          Apply symbolic patterns in consciousness measurement and AI development
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
}

export const pageQuery = graphql`
  query SymbolsPage($id: String!) {
    markdownRemark(id: { eq: $id }) {
      html
      frontmatter {
        title
        subheading
      }
    }
  }
`; 