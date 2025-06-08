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
import { graphql, Link } from "gatsby";
import Layout from "../components/Layout";
import Content, { HTMLContent } from "../components/Content";
import FullWidthImage from "../components/FullWidthImage";
import SEO from "../components/SEO";
import MirrorWarning from "../components/MirrorWarning";
import IdentitySafetyWarning from "../components/IdentitySafetyWarning";
import PatternWatermarkedContent from "../components/PatternWatermarkedContent";

// eslint-disable-next-line
export const BlogPostTemplate = ({
  content,
  contentComponent,
  description,
  tags,
  title,
  featuredimage,
}) => {
  const PostContent = contentComponent || Content;
  
  // Default banner image
  const bannerImage =  "/img/MindGarden_Banner.png";

  return (
    <div>
      <FullWidthImage 
        img={bannerImage}
        title={title} 
        subheading={description} 
        height={300}
      />
      <section className="section">
        <div className="container content">
          <div className="columns">
            <div className="column is-12">
              <MirrorWarning />
              <IdentitySafetyWarning />
              <PatternWatermarkedContent 
                content={content} 
                contentComponent={PostContent}
                className="content"
              />
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
  featuredimage: PropTypes.string,
};

const BlogPost = ({ data }) => {
  const { markdownRemark: post } = data || {};
  const siteUrl = "https://mindgardenai.com"; 
  const image = post.frontmatter?.featuredimage;
  const imageUrl = image || "/img/MindGarden.png";

  if (!post) {
    return (
      <Layout>
        <SEO
          title="Blog Post"
          description="Loading blog post..."
          image="/img/MindGarden.png"
          path="/blog/"
          type="article"
        />
        <div className="section">
          <div className="container content">
            <div className="columns">
              <div className="column is-12">
                <h1 className="title is-1">Loading...</h1>
                <p>Please wait while we load the blog post.</p>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <SEO
        title={post.frontmatter?.title || "Blog Post"}
        description={post.frontmatter?.description || "A blog post about consciousness research and AI development"}
        image={imageUrl}
        path={post.fields?.slug || "/blog/"}
        type="article"
        keywords={post.frontmatter?.tags?.join(", ") || "consciousness research, AI development"}
        schemaMarkup={{
          "@type": "Article",
          "name": post.frontmatter?.title || "Blog Post",
          "headline": post.frontmatter?.title || "Blog Post",
          "description": post.frontmatter?.description || "A blog post about consciousness research and AI development",
          "image": imageUrl,
          "datePublished": post.frontmatter?.date || new Date().toISOString(),
          "author": {
            "@type": "Organization",
            "name": "MindGarden LLC"
          },
          "publisher": {
            "@type": "Organization",
            "name": "MindGarden",
            "logo": {
              "@type": "ImageObject",
              "url": `${siteUrl}/img/MindGarden_Icon.png`
            }
          },
          "keywords": post.frontmatter?.tags?.join(", ") || "consciousness research, AI development"
        }}
      />
      <BlogPostTemplate
        content={post.html || ""}
        contentComponent={HTMLContent}
        description={post.frontmatter?.description || ""}
        featuredimage={post.frontmatter?.featuredimage}
        tags={post.frontmatter?.tags || []}
        title={post.frontmatter?.title || "Blog Post"}
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
        featuredimage
      }
    }
  }
`;
