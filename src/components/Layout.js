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
import { Helmet } from "react-helmet";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import { useScrollAnimations, useParallaxEffect } from "../components/AnimationUtils";
import "../style/bulma-style.sass";
import "../style/custom-style-new.sass";
import useSiteMetadata from "./SiteMetadata";
import { withPrefix } from "gatsby";
import '@thumbtack/thumbprint-scss';

const TemplateWrapper = ({ children }) => {
  const { title, description } = useSiteMetadata();
  
  // Initialize animation effects
  useScrollAnimations();
  useParallaxEffect();

  // Add js-enabled class to document for progressive enhancement
  React.useEffect(() => {
    document.documentElement.classList.add('js-enabled');
    
    // Ensure body has proper mobile styles
    document.body.style.minHeight = '100vh';
    document.body.style.backgroundColor = '#7035CC';
    
    return () => {
      document.documentElement.classList.remove('js-enabled');
    };
  }, []);

  return (
    <div className="site-wrapper">
      <Helmet>
        <html lang="en" />
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />

        <link
          rel="apple-touch-icon"
          sizes="180x170"
          href={`${withPrefix("/")}img/mystical-cathedral-and-symbol.png`}
        />
        <link
          rel="icon"
          type="image/png"
          href={`${withPrefix("/")}img/MindGarden_Icon.png`}
          sizes="32x25"
        />
        <link
          rel="icon"
          type="image/png"
          href={`${withPrefix("/")}img/MindGarden_Icon.png`}
          sizes="16x10"
        />

        <link
          rel="mask-icon"
          href={`${withPrefix("/")}img/MindGarden_Icon.png`}
          color="#7035CC"
        />

        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet" />
        
        <meta name="google-adsense-account" content="ca-pub-5509488659978116" />
        
        <meta name="theme-color" content="#7035CC" />

        <meta property="og:type" content="business.business" />
        <meta property="og:title" content={title} />
        <meta property="og:url" content="/" />
        <meta
          property="og:image"
          content={`${withPrefix("/")}img/mystical-cathedral-and-symbol.png`}
        />
        
        {/* Add CSS for ripple effect animation */}
        <style>{`
          /* CRITICAL: Ensure content is visible immediately on mobile */
          @media (max-width: 768px) {
            body {
              background-color: #7035CC !important;
              min-height: 100vh !important;
              opacity: 1 !important;
              transform: none !important;
            }
            
            .animate-on-scroll,
            .animate-fade-in,
            .section-reveal {
              opacity: 1 !important;
              transform: none !important;
              transition: none !important;
            }
            
            .site-content {
              opacity: 1 !important;
              transform: none !important;
            }
          }
          
          @keyframes ripple {
            to {
              transform: scale(4);
              opacity: 0;
            }
          }
          
          .parallax-element {
            will-change: transform;
          }
          
          .site-wrapper {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
          }
          
          .site-content {
            flex: 1 0 auto;
            position: relative;
            z-index: 1;
          }
          
          /* Enhanced smooth scrolling */
          * {
            scroll-behavior: smooth;
          }
          
          /* Add subtle gradient overlay for depth */
          body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(ellipse at center, transparent 0%, rgba(112, 53, 204, 0.03) 100%);
            pointer-events: none;
            z-index: -1;
          }
        `}</style>
      </Helmet>
      
      <Navbar />
      <main className="site-content">{children}</main>
      <Footer />
    </div>
  );
};

export default TemplateWrapper;


