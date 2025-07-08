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
    if (window.adsbygoogle) {
      try {
        window.adsbygoogle.push({});
      } catch (e) {
        console.log('AdSense initialization error:', e);
      }
    }
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
      <div className="crane-gate-wrapper">
        <CraneScavengerEffect />
        
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
      </div>
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
