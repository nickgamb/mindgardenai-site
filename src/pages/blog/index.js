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
import { useEffect } from "react";
import Layout from "../../components/Layout";
import BlogRoll from "../../components/BlogRoll";
import FullWidthImage from "../../components/FullWidthImage";
import SacredGlyph from "../../components/SacredGlyph";
import { Link } from "gatsby";

export default class BlogIndexPage extends React.Component {
  componentDidMount() {
    // Initialize AdSense ads
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
  }

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
            {/* Ad after top banner */}
            <div className="adsense-container post-banner-ad" style={{ margin: '2rem auto', maxWidth: '728px', textAlign: 'center' }}>
              <ins
                className="adsbygoogle"
                style={{ display: 'block' }}
                data-ad-client="ca-pub-5509488659978116"
                data-ad-slot="1488521036"
                data-ad-format="auto"
                data-full-width-responsive="true"
              />
          </div>
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
        </section>
      </Layout>
    );
  }
}


