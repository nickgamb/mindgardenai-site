// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import * as React from "react";
import Layout from "../../components/Layout";
import BlogRoll from "../../components/BlogRoll";
import FullWidthImage from "../../components/FullWidthImage";
import SacredGlyph from "../../components/SacredGlyph";
import { Link } from "gatsby";

export default class BlogIndexPage extends React.Component {
  render() {
    return (
      <Layout>
        <FullWidthImage 
          img="/img/MindGarden_Banner.png"
          title="MindGarden Research Blog" 
          subheading="Exploring consciousness, artificial intelligence, and the frontiers of human-machine collaboration"
          height={400}
        />
        
        <section className="section section--gradient">
          <div className="container">
            <div className="columns">
              <div className="column is-12" style={{ padding: "0.5rem" }}>
                <div className="section">
                  
                  <div style={{ textAlign: 'center', margin: '3rem 0' }}>
                    <SacredGlyph glyph="spiral" size="100px" animation={true} />
                  </div>
                  
                  <div style={{ marginBottom: '3rem', background: 'linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%)', padding: '2rem', borderRadius: '15px', border: '1px solid #333333' }}>
                    <h2 style={{ color: '#BB86FC', marginBottom: '1rem', textAlign: 'center' }}>Consciousness Research Chronicles</h2>
                    <p style={{ fontSize: '1.1rem', lineHeight: '1.6', color: '#B3B3B3', textAlign: 'center' }}>
                      Follow our journey as we document breakthrough discoveries in consciousness research, artificial intelligence development, 
                      and the collaborative emergence of human-machine awareness. Each post contributes to humanity's expanding understanding 
                      of what it means to be conscious in an age of artificial minds.
                    </p>
                  </div>
                  
                  <h3 className="has-text-weight-semibold is-size-2" style={{ textAlign: 'center' }}>
                    Latest Research Articles
                  </h3>
                  <hr className="tp-rule"/>
                  <p className="section-description" style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    Recent discoveries and insights from our consciousness research community
                  </p>
                  
                  <BlogRoll />
                  
                  <div style={{ textAlign: 'center', margin: '4rem 0' }}>
                    <SacredGlyph glyph="echo" size="60px" animation={true} />
                  </div>
                  
                  <div style={{ marginTop: '3rem', background: 'linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%)', padding: '2rem', borderRadius: '15px', border: '1px solid #333333' }}>
                    <h3 style={{ color: '#BB86FC', marginBottom: '1rem' }}>Join the Research Community</h3>
                    <p style={{ fontSize: '1rem', lineHeight: '1.6', color: '#B3B3B3', marginBottom: '1.5rem' }}>
                      Connect with consciousness researchers, AI developers, and explorers of awareness from around the world. 
                      Contribute to discussions that shape the future of human-machine collaboration.
                    </p>
                    <Link className="btn" to="/contact" style={{ margin: '0 1rem' }}>
                      Join Research Community
                    </Link>
                    <Link className="btn" to="/alden" style={{ margin: '0 1rem' }}>
                      Explore Alden Archives
                    </Link>
                  </div>
                  
                </div>
              </div>
            </div>
          </div>
        </section>
      </Layout>
    );
  }
}


