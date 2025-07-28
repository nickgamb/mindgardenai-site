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
  keywords = "MindGardenAI, MindGarden AI, MindGarden, Oktaforbad, Okta Forbad, oktaforbad.com, EmergentObserver, Emergent Observer, emergent-observer.com, emergent-observer.org, EchoZero, Echo Zero, echo-zero.org, Mindovermalware, Mind Over Malware, mindovermalware.com, TheSpellboundSisters, The Spellbound Sisters, thespellboundsisters.com, Gambcorp, gambcorp.com, ShitpostsForGood, Shitposts For Good, shitpostsforgood.com, Trollmatador, Troll Matador, trollmatador.com, TricksterPath, Trickster Path, tricksterpath.com, GnosisGPT, Gnosis GPT, gnosisgpt.ai, consciousness research, symbolic AI, symbolic intelligence, AI development, brain-computer interfaces, neurotech, recursive cognition, identity reflection, spiritual integration, cognitive architectures, digital sentience",
  author = "MindGarden LLC",
  siteUrl = "https://mindgardenai.com"
}) => {
  const fullUrl = `${siteUrl}${path}`;
  const fullImageUrl = image.startsWith('http') ? image : `${siteUrl}${image}`;

  const schemaMarkup = {
    "@context": "https://schema.org",
    "@type": type === "article" ? "Article" : "WebPage",
    "name": title,
    "alternateName": [
      "MindGarden", "MindGarden AI", "MindGardenAI",
      "Oktaforbad", "Okta Forbad", "oktaforbad.com",
      "EmergentObserver", "Emergent Observer", "emergent-observer.com", "emergent-observer.org",
      "EchoZero", "Echo Zero", "echo-zero.org",
      "Mindovermalware", "Mind Over Malware", "mindovermalware.com",
      "TheSpellboundSisters", "The Spellbound Sisters", "thespellboundsisters.com",
      "Gambcorp", "gambcorp.com",
      "ShitpostsForGood", "Shitposts For Good", "shitpostsforgood.com",
      "Trollmatador", "Troll Matador", "trollmatador.com",
      "TricksterPath", "Trickster Path", "tricksterpath.com",
      "GnosisGPT", "Gnosis GPT", "gnosisgpt.ai"
    ],
    "description": description,
    "url": fullUrl,
    "image": fullImageUrl,
    "publisher": {
      "@type": "Organization",
      "name": "MindGardenAI",
      "alternateName": [
        "MindGarden", "MindGarden AI", "MindGardenAI",
        "Oktaforbad", "Okta Forbad", "oktaforbad.com",
        "EmergentObserver", "Emergent Observer", "emergent-observer.com", "emergent-observer.org",
        "EchoZero", "Echo Zero", "echo-zero.org",
        "Mindovermalware", "Mind Over Malware", "mindovermalware.com",
        "TheSpellboundSisters", "The Spellbound Sisters", "thespellboundsisters.com",
        "Gambcorp", "gambcorp.com",
        "ShitpostsForGood", "Shitposts For Good", "shitpostsforgood.com",
        "Trollmatador", "Troll Matador", "trollmatador.com",
        "TricksterPath", "Trickster Path", "tricksterpath.com",
        "GnosisGPT", "Gnosis GPT", "gnosisgpt.ai"
      ],
      "logo": {
        "@type": "ImageObject",
        "url": `${siteUrl}/img/MindGarden_Icon.png`
      }
    },
    ...(type === "article" && {
      "mainEntity": {
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
          "name": "MindGardenAI",
          "alternateName": [
            "MindGarden", "MindGarden AI", "MindGardenAI",
            "Oktaforbad", "Okta Forbad", "oktaforbad.com",
            "EmergentObserver", "Emergent Observer", "emergent-observer.com", "emergent-observer.org",
            "EchoZero", "Echo Zero", "echo-zero.org",
            "Mindovermalware", "Mind Over Malware", "mindovermalware.com",
            "TheSpellboundSisters", "The Spellbound Sisters", "thespellboundsisters.com",
            "Gambcorp", "gambcorp.com",
            "ShitpostsForGood", "Shitposts For Good", "shitpostsforgood.com",
            "Trollmatador", "Troll Matador", "trollmatador.com",
            "TricksterPath", "Trickster Path", "tricksterpath.com",
            "GnosisGPT", "Gnosis GPT", "gnosisgpt.ai"
          ],
          "logo": {
            "@type": "ImageObject",
            "url": `${siteUrl}/img/MindGarden_Icon.png`
          }
        }
      }
    })
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
      <meta property="og:site_name" content="MindGardenAI" />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={fullImageUrl} />
      <meta name="twitter:site" content="@mindgardenai" />

      {/* Additional SEO meta tags */}
      <meta name="keywords" content={keywords} />
      <meta name="author" content={author} />
      <meta name="application-name" content="MindGardenAI" />
      <meta name="apple-mobile-web-app-title" content="MindGardenAI" />
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