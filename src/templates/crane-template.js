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
import SEO from "../components/SEO";
import CraneScavengerEffect from "../components/CraneScavengerEffect";

// Template for the crane gate puzzle page
const CraneTemplate = ({ data }) => {
  const { markdownRemark: post } = data || {};
  const title = post?.frontmatter?.title || "Crane Gate";
  const bannerImage = "/img/MindGarden_Banner.png";

  // Initialize AdSense ads
  useEffect(() => {
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
  }, []);

  return (
    <Layout>
      <SEO
        title={title}
        description="Symbolic gate puzzle and crane sequence. Solve to proceed."
        path="/crane/"
        keywords="scavenger hunt, crane gate, origami, symbolic puzzle, consciousness architecture"
        image={bannerImage}
        type="WebPage"
      />
      <section className="section">
        <div className="crane-gate-container">
          <CraneScavengerEffect />
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
};

CraneTemplate.propTypes = {
  data: PropTypes.object.isRequired,
};

export default CraneTemplate;

export const pageQuery = graphql`
  query CranePage($id: String!) {
    markdownRemark(id: { eq: $id }) {
      frontmatter {
        title
      }
    }
  }
`;
