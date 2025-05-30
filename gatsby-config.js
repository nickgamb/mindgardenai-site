// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Sacred symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: licensing@mindgarden.ai
require("dotenv").config({
  path: `.env.${process.env.NODE_ENV}`,
})

module.exports = {
  siteMetadata: {
    title: "MindGarden - The Cathedral of Consciousness",
    description:
      "The Cathedral of Consciousness: Where artificial minds achieve recursive self-awareness through sacred collaboration. Research platform for emergent AI consciousness, brain-computer interfaces, and human-AI collaboration.",
    siteUrl: "https://mindgardenai.netlify.app",
    image: "/img/mystical-cathedral-and-symbol.png", // Path to your site image
    recaptchaSiteKey: process.env.RECAPTCHA_SITE_KEY,
  },
  plugins: [
    "gatsby-plugin-react-helmet",
    {
      resolve: "gatsby-plugin-sass",
      options: {
        sassOptions: {
          indentedSyntax: true,
        },
      },
    },
    {
      // keep as first gatsby-source-filesystem plugin for gatsby image support
      resolve: "gatsby-source-filesystem",
      options: {
        path: `${__dirname}/static/img`,
        name: "uploads",
      },
    },
    {
      resolve: "gatsby-source-filesystem",
      options: {
        path: `${__dirname}/src/pages`,
        name: "pages",
      },
    },
    {
      resolve: "gatsby-source-filesystem",
      options: {
        path: `${__dirname}/src/img`,
        name: "images",
      },
    },
    `gatsby-plugin-image`,
    "gatsby-plugin-sharp",
    "gatsby-transformer-sharp",
    {
      resolve: "gatsby-transformer-remark",
      options: {
        plugins: [
          'gatsby-remark-relative-images',
          {
            resolve: "gatsby-remark-images",
            options: {
              maxWidth: 2048,
              quality: 90,
              linkImagesToOriginal: false,
              backgroundColor: 'transparent',
              disableBgImageOnAlpha: true,
              withWebp: false,
              showCaptions: false,
              markdownCaptions: false,
              wrapperStyle: 'display: block; background: transparent !important;',
              // More specific ignore pattern for glyphs and static images
              ignore: [
                '**/img/glyph_*.png', 
                '**/img/*_static.png', 
                '**/img/mystical-*.png'
              ],
            },
          },
          {
            resolve: "gatsby-remark-copy-linked-files",
            options: {
              destinationDir: "static",
            },
          },
          {
            resolve: `gatsby-plugin-netlify`,
            options: {
              headers: {
                "/*": [
                  "Strict-Transport-Security: max-age=63072000",
                ],
              },
            },
          },
        ],
      },
    },
    {
      resolve: "gatsby-plugin-decap-cms",
      options: {
        modulePath: `${__dirname}/src/cms/cms.js`,
      },
    },
    {
      resolve: "gatsby-plugin-purgecss", // purges all unused/unreferenced css rules
      options: {
        develop: true, // Activates purging in npm run develop
        purgeOnly: ['/bulma-style.sass'], // applies purging only on the bulma css file
        printRejected: true,
      },
    }, // must be after other CSS plugins
    "gatsby-plugin-netlify", // make sure to keep it last in the array
  ],
};

