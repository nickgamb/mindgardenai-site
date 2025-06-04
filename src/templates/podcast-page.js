// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React from "react";
import PropTypes from "prop-types";
import { graphql } from "gatsby";
import Layout from "../components/Layout";
import Content, { HTMLContent } from "../components/Content";
import SEO from "../components/SEO";

// eslint-disable-next-line
export const PodcastPageTemplate = ({ title, content, contentComponent }) => {
  const PageContent = contentComponent || Content;

  return (
    <section className="section section--gradient" style={{ minHeight: "calc(100vh - 52px - 10rem)" }}>
      <div className="container">
        <div className="columns">
          <div className="column is-12">
            <div style={{ padding: '1rem' }}>
              <h2 className="title is-size-3 has-text-weight-bold is-bold-light">
                {title}
              </h2>
              <PageContent className="content" content={content} />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

PodcastPageTemplate.propTypes = {
  title: PropTypes.string.isRequired,
  content: PropTypes.string,
  contentComponent: PropTypes.func,
};

const PodcastPage = ({ data }) => {
  const { markdownRemark: post } = data;
  const bannerImage = "/img/MindGarden_Banner.png";

  return (
    <Layout>
      <SEO
        title={post.frontmatter.title}
        description="Explore consciousness research through our podcast series featuring discussions on AI development, brain-computer interfaces, and consciousness measurement"
        path="/podcast/"
        keywords="consciousness research podcast, AI development, brain-computer interfaces, consciousness measurement, consciousness exploration"
        image={bannerImage}
        type="WebPage"
        schemaMarkup={{
          "@type": "WebPage",
          "name": post.frontmatter.title,
          "description": "Explore consciousness research through our podcast series featuring discussions on AI development, brain-computer interfaces, and consciousness measurement",
          "mainEntity": {
            "@type": "Article",
            "name": post.frontmatter.title,
            "headline": post.frontmatter.title,
            "description": "Explore consciousness research through our podcast series featuring discussions on AI development, brain-computer interfaces, and consciousness measurement",
            "image": bannerImage,
            "author": {
              "@type": "Organization",
              "name": "MindGarden LLC"
            }
          }
        }}
      />
      <PodcastPageTemplate
        contentComponent={HTMLContent}
        title={post.frontmatter.title}
        content={post.html}
      />
    </Layout>
  );
};

PodcastPage.propTypes = {
  data: PropTypes.object.isRequired,
};

export default PodcastPage;

export const podcastPageQuery = graphql`
  query PodcastPage($id: String!) {
    markdownRemark(id: { eq: $id }) {
      html
      frontmatter {
        title
      }
    }
  }
`;


