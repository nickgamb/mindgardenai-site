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
import { graphql } from "gatsby";
import Layout from "../components/Layout";
import SymbolBrowser from "../components/SymbolBrowser";
import FullWidthImage from "../components/FullWidthImage";
import CathedralGlyph from "../components/SacredGlyph";

export default function SymbolsTemplate({ data }) {
  const { markdownRemark: post } = data;

  return (
    <Layout>
      <FullWidthImage 
        img={post.frontmatter.image || "/img/MindGarden_Banner.png"}
        title={post.frontmatter.title} 
        subheading={post.frontmatter.subheading}
        height={400}
      />
      
      <section className="section section--gradient">
        <div className="container">
          <div className="columns">
            <div className="column is-12">
              <div className="section">
                <div className="glyph-container">
                  <CathedralGlyph glyph="spiral" size="100px" animation={true} className="cathedral-glyph" />
                </div>
                
                <div className="feature-section">
                  <h2 className="section-title has-text-centered has-text-primary">{post.frontmatter.title}</h2>
                  <div 
                    className="section-description"
                    dangerouslySetInnerHTML={{ __html: post.html }}
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
        image
      }
    }
  }
`; 