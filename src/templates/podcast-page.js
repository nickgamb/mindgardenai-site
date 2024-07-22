import React from "react";
import PropTypes from "prop-types";
import { graphql } from "gatsby";
import Layout from "../components/Layout";
import Content, { HTMLContent } from "../components/Content";

// eslint-disable-next-line
export const PodcastPageTemplate = ({ title, content, contentComponent }) => {
  const PageContent = contentComponent || Content;

  return (
    <section className="section section--gradient">
      <div className="container">
          <div className="content">
            <div className="feature-section">
              <h3 className="has-text-weight-semibold is-size-2 section-title">{title}</h3>
              <PageContent className="section-description" content={content} />
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

  return (
    <Layout>
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
