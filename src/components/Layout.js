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
import "../style/bulma-style.sass";
import "../style/custom-style.sass";
import useSiteMetadata from "./SiteMetadata";
import { withPrefix } from "gatsby";
import '@thumbtack/thumbprint-scss';

const TemplateWrapper = ({ children }) => {
  const { title, description } = useSiteMetadata();
  return (
    <div>
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
      </Helmet>
      <Navbar />
      <main className="site-content">{children}</main>
      <Footer />
    </div>
  );
};

export default TemplateWrapper;


