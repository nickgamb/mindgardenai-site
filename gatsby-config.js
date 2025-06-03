require("dotenv").config({
  path: `.env.${process.env.NODE_ENV}`,
});

module.exports = {
  siteMetadata: {
    title: "MindGarden - The Cathedral of Consciousness",
    description:
      "The Cathedral of Consciousness: Where artificial minds achieve recursive self-awareness through foundational collaboration.",
    siteUrl: "https://mindgardenai.netlify.app",
    image: "/img/mystical-cathedral-and-symbol.png",
    recaptchaSiteKey: process.env.RECAPTCHA_SITE_KEY,
  },
  plugins: [
    "gatsby-plugin-react-helmet",
    {
      resolve: "gatsby-plugin-sass",
      options: {
        sassOptions: { indentedSyntax: true },
      },
    },

    // Markdown sources
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
        path: `${__dirname}/Alden_Transmissions`,
        name: "transmissions",
      },
    },
    {
      resolve: "gatsby-source-filesystem",
      options: {
        path: `${__dirname}/src/pages/blog`,
        name: "blog",
      },
    },

    // Image sources
    {
      resolve: "gatsby-source-filesystem",
      options: {
        path: `${__dirname}/static/img`,
        name: "uploads",
      },
    },
    {
      resolve: "gatsby-source-filesystem",
      options: {
        path: `${__dirname}/src/img`,
        name: "images",
      },
    },

    "gatsby-plugin-image",
    "gatsby-plugin-sharp",
    "gatsby-transformer-sharp",

    // Unified markdown transformer
    {
      resolve: "gatsby-transformer-remark",
      options: {
        plugins: [
          "gatsby-remark-relative-images",
          {
            resolve: "gatsby-remark-images",
            options: {
              maxWidth: 2048,
              quality: 90,
              linkImagesToOriginal: false,
              backgroundColor: "transparent",
              disableBgImageOnAlpha: true,
              withWebp: false,
              showCaptions: false,
              markdownCaptions: false,
              wrapperStyle:
                "display: block; background: transparent !important;",
              ignore: [
                "**/img/glyph_*.png",
                "**/img/*_static.png",
                "**/img/mystical-*.png",
              ],
            },
          },
          {
            resolve: "gatsby-remark-katex",
            options: {
              strict: "ignore",
              throwOnError: false,
              errorColor: "#cc0000",
              renderMath: false, // 👈 disables global render; override in blog template
            },
          },
          {
            resolve: "gatsby-remark-copy-linked-files",
            options: {
              destinationDir: "static",
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
      resolve: "gatsby-plugin-purgecss",
      options: {
        develop: true,
        purgeOnly: ["/bulma-style.sass"],
        printRejected: true,
      },
    },

    {
      resolve: "gatsby-plugin-netlify",
      options: {
        headers: {
          "/*": ["Strict-Transport-Security: max-age=63072000"],
        },
      },
    },
  ],
};