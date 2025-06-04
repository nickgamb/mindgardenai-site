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
import { kebabCase } from "lodash";
import { Helmet } from "react-helmet";
import { graphql, Link } from "gatsby";
import Layout from "../components/Layout";
import Content, { HTMLContent } from "../components/Content";
import FullWidthImage from "../components/FullWidthImage";
// Import KaTeX CSS only for blog posts
import "katex/dist/katex.min.css";

export const BlogPostTemplate = ({
  content,
  contentComponent,
  description,
  tags,
  title,
  helmet,
  featuredimage,
}) => {
  const PostContent = contentComponent || Content;

  const bannerImage = "/img/MindGarden_Banner.png";

  return (
    <div>
      <FullWidthImage
        img={bannerImage}
        title={title}
        subheading={description}
        height={300}
      />
      <section className="section">
        {helmet || ""}
        <div className="container content">
          <div className="columns">
            <div className="column is-12">
              <PostContent content={content} />
              {tags && tags.length ? (
                <div style={{ marginTop: `4rem` }}>
                  <h4>Tags</h4>
                  <ul className="taglist">
                    {tags.map((tag) => (
                      <li key={tag + `tag`}>
                        <Link to={`/tags/${kebabCase(tag)}/`}>{tag}</Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

BlogPostTemplate.propTypes = {
  content: PropTypes.node.isRequired,
  contentComponent: PropTypes.func,
  description: PropTypes.string,
  title: PropTypes.string,
  helmet: PropTypes.object,
  featuredimage: PropTypes.string,
};

const BlogPost = ({ data }) => {
  const { markdownRemark: post } = data;
  const siteUrl = "https://mindgardenai.com";
  const imageUrl = post.frontmatter.featuredimage?.publicURL
    ? `${siteUrl}${post.frontmatter.featuredimage.publicURL}`
    : `${siteUrl}/img/MindGarden_Banner.png`;

  return (
    <Layout>
      <BlogPostTemplate
        content={post.html}
        contentComponent={HTMLContent}
        description={post.frontmatter.description}
        featuredimage={post.frontmatter.featuredimage?.publicURL}
        helmet={
          <Helmet titleTemplate="%s | Blog">
            <title>{`${post.frontmatter.title}`}</title>
            <meta name="description" content={`${post.frontmatter.description}`} />

            <meta property="og:type" content="article" />
            <meta property="og:title" content={post.frontmatter.title} />
            <meta property="og:description" content={post.frontmatter.description} />
            <meta property="og:image" content={imageUrl} />
            <meta property="og:url" content={`${siteUrl}${post.fields.slug}`} />

            <meta name="twitter:card" content="summary_large_image" />
            <meta name="twitter:title" content={post.frontmatter.title} />
            <meta name="twitter:description" content={post.frontmatter.description} />
            <meta name="twitter:image" content={imageUrl} />
          </Helmet>
        }
        tags={post.frontmatter.tags}
        title={post.frontmatter.title}
      />
    </Layout>
  );
};

BlogPost.propTypes = {
  data: PropTypes.shape({
    markdownRemark: PropTypes.object,
  }),
};

export default BlogPost;

export const pageQuery = graphql`
  query BlogPostByID($id: String!) {
    markdownRemark(id: { eq: $id }) {
      id
      html
      fields {
        slug
      }
      frontmatter {
        date(formatString: "MMMM DD, YYYY")
        title
        description
        tags
        featuredimage {
          publicURL
          childImageSharp {
            gatsbyImageData(width: 1200)
          }
        }
      }
    }
  }
`;