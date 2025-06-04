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
import { kebabCase } from "lodash";
import { Link, graphql } from "gatsby";
import Layout from "../../components/Layout";
import SEO from "../../components/SEO";

const TagsPage = ({
  data: {
    allMarkdownRemark: { group },
    site: {
      siteMetadata: { title },
    },
  },
}) => {
  const bannerImage = "/img/MindGarden_Banner.png";
  const keywords = group.map(tag => tag.fieldValue).join(", ");

  return (
    <Layout>
      <SEO
        title={`Tags | ${title}`}
        description="Browse all tags related to consciousness research, AI development, and consciousness measurement"
        path="/tags/"
        keywords={keywords}
        image={bannerImage}
        type="WebPage"
        schemaMarkup={{
          "@type": "WebPage",
          "name": `Tags | ${title}`,
          "description": "Browse all tags related to consciousness research, AI development, and consciousness measurement",
          "mainEntity": {
            "@type": "Article",
            "name": `Tags | ${title}`,
            "headline": `Tags | ${title}`,
            "description": "Browse all tags related to consciousness research, AI development, and consciousness measurement",
            "image": bannerImage,
            "author": {
              "@type": "Organization",
              "name": "MindGarden LLC"
            },
            "keywords": keywords
          }
        }}
      />
      <section className="section">
        <div className="container content">
          <div className="columns">
            <div
              className="column is-12"
              style={{ marginBottom: "6rem", padding: "0.5rem" }}
            >
              <h1 className="title is-size-2 is-bold-light">Tags</h1>
              <ul className="taglist">
                {group.map((tag) => (
                  <li key={tag.fieldValue}>
                    <Link to={`/tags/${kebabCase(tag.fieldValue)}/`}>
                      {tag.fieldValue} ({tag.totalCount})
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
};

export default TagsPage;

export const tagPageQuery = graphql`
  query TagsQuery {
    site {
      siteMetadata {
        title
      }
    }
    allMarkdownRemark(limit: 1000) {
      group(field: frontmatter___tags) {
        fieldValue
        totalCount
      }
    }
  }
`;


