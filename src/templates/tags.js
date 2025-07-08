// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useEffect } from "react";
import { Link, graphql } from "gatsby";
import Layout from "../components/Layout";
import SEO from "../components/SEO";

const TagRoute = (props) =>  {
    const { data, pageContext } = props || {};
    const posts = data?.allMarkdownRemark?.edges || [];
    const { tag } = pageContext || {};
    const { title } = data?.site?.siteMetadata || { title: "MindGarden" };
    const { totalCount } = data?.allMarkdownRemark || { totalCount: 0 };

    useEffect(() => {
      const initializeAds = () => {
        if (window.adsbygoogle) {
          try {
            console.log('Initializing AdSense ads...');
            
            // Get all ad containers on the page
            const adContainers = document.querySelectorAll('.adsbygoogle');
            console.log(`Found ${adContainers.length} ad containers`);
            
            // Initialize each ad container individually
            adContainers.forEach((adContainer, index) => {
              try {
                console.log(`Initializing ad ${index + 1} with slot: ${adContainer.getAttribute('data-ad-slot')}`);
                window.adsbygoogle.push({});
              } catch (e) {
                console.error(`Error initializing ad ${index + 1}:`, e);
              }
            });
            
            console.log('AdSense ads initialization completed');
          } catch (e) {
            console.log('AdSense initialization error:', e);
          }
        } else {
          console.log('AdSense script not loaded yet, retrying...');
          setTimeout(initializeAds, 1000);
        }
      };

      // Wait for AdSense script to load
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeAds);
      } else {
        initializeAds();
      }
      
      // Also try to initialize ads after a longer delay to catch any late-loading ads
      setTimeout(initializeAds, 3000);
    }, []);

    if (!tag || !data) {
      return (
        <Layout>
          <SEO
            title="Tags"
            description="Browse posts by tag in consciousness research and AI development"
            path="/tags/"
            keywords="consciousness research, AI development, tags"
          />
          <section className="section">
            <div className="container content">
              <div className="columns">
                <div className="column is-12">
                  <h1 className="title is-1">Loading...</h1>
                  <p>Please wait while we load the tags page.</p>
                </div>
              </div>
            </div>
          </section>
        </Layout>
      );
    }

    const postLinks = posts.map((post) => (
      <li key={post.node.fields.slug}>
        <Link to={post.node.fields.slug}>
          <h2 className="is-size-2">{post.node.frontmatter.title}</h2>
        </Link>
      </li>
    ));

    const tagHeader = `${totalCount} post${
      totalCount === 1 ? "" : "s"
    } tagged with "${tag}"`;

    return (
      <Layout>
        <SEO
          title={`${tag} | ${title}`}
          description={`Browse ${totalCount} post${totalCount === 1 ? "" : "s"} about ${tag} in consciousness research and AI development`}
          path={`/tags/${tag}/`}
          keywords={`${tag}, consciousness research, AI development, ${posts.map(post => post.node.frontmatter.title).join(", ")}`}
        />
        <section className="section">
          <div className="container content">
            <div className="columns">
              <div
                className="column is-12"
                style={{ marginBottom: "6rem" }}
              >
                {/* Ad at the top */}
                <div className="adsense-container post-banner-ad" style={{ margin: '2rem auto', maxWidth: '728px', textAlign: 'center' }}>
                  <ins
                    className="adsbygoogle"
                    style={{ display: 'block' }}
                    data-ad-client="ca-pub-5509488659978116"
                    data-ad-slot="1488521036"
                    data-ad-format="auto"
                    data-full-width-responsive="true"
                  />
                </div>
                
                <h3 className="title is-size-4 is-bold-light">{tagHeader}</h3>
                <ul className="taglist">{postLinks}</ul>
                <p>
                  <Link to="/tags/">Browse all tags</Link>
                </p>
              </div>
            </div>
          </div>
        </section>
        
        {/* Footer ad */}
        <div className="adsense-container" style={{ margin: '2rem auto', maxWidth: '728px', textAlign: 'center' }}>
          <ins
            className="adsbygoogle"
            style={{ display: 'block' }}
            data-ad-client="ca-pub-5509488659978116"
            data-ad-slot="1926105936"
            data-ad-format="auto"
            data-full-width-responsive="true"
          />
        </div>
      </Layout>
    );
}

export default TagRoute;

export const tagPageQuery = graphql`
  query TagPage($tag: String) {
    site {
      siteMetadata {
        title
      }
    }
    allMarkdownRemark(
      limit: 1000
      sort: { fields: [frontmatter___date], order: DESC }
      filter: { frontmatter: { tags: { in: [$tag] } } }
    ) {
      totalCount
      edges {
        node {
          fields {
            slug
          }
          frontmatter {
            title
          }
        }
      }
    }
  }
`;


