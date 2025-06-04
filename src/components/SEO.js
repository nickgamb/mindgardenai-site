// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React from 'react';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';

const SEO = ({ 
  title,
  description,
  image = "/img/MindGarden_Banner.png",
  path,
  type = "website",
  keywords = "consciousness research, AI development, symbolic intelligence, brain-computer interfaces, consciousness measurement",
  author = "MindGarden LLC",
  siteUrl = "https://mindgardenai.com"
}) => {
  const fullUrl = `${siteUrl}${path}`;
  const fullImageUrl = image.startsWith('http') ? image : `${siteUrl}${image}`;

  // Schema markup for the page
  const schemaMarkup = {
    "@context": "https://schema.org",
    "@type": type === "article" ? "Article" : "WebPage",
    "name": title,
    "description": description,
    "url": fullUrl,
    "image": fullImageUrl,
    "publisher": {
      "@type": "Organization",
      "name": "MindGarden",
      "logo": {
        "@type": "ImageObject",
        "url": `${siteUrl}/img/MindGarden_Icon.png`
      }
    },
    "mainEntity": type === "article" ? {
      "@type": "Article",
      "name": title,
      "headline": title,
      "description": description,
      "image": fullImageUrl,
      "author": {
        "@type": "Organization",
        "name": author
      },
      "publisher": {
        "@type": "Organization",
        "name": "MindGarden",
        "logo": {
          "@type": "ImageObject",
          "url": `${siteUrl}/img/MindGarden_Icon.png`
        }
      }
    } : undefined
  };

  return (
    <Helmet>
      <title>{title}</title>
      <meta name="description" content={description} />
      
      {/* Schema.org markup */}
      <script type="application/ld+json">
        {JSON.stringify(schemaMarkup)}
      </script>
      
      {/* Open Graph / Facebook */}
      <meta property="og:type" content={type} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={fullImageUrl} />
      <meta property="og:url" content={fullUrl} />
      <meta property="og:site_name" content="MindGarden AI" />
      
      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={fullImageUrl} />
      <meta name="twitter:site" content="@mindgardenai" />
      
      {/* Additional SEO meta tags */}
      <meta name="keywords" content={keywords} />
      <meta name="author" content={author} />
      <link rel="canonical" href={fullUrl} />
    </Helmet>
  );
};

SEO.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  image: PropTypes.string,
  path: PropTypes.string.isRequired,
  type: PropTypes.oneOf(['website', 'article']),
  keywords: PropTypes.string,
  author: PropTypes.string,
  siteUrl: PropTypes.string
};

export default SEO; 