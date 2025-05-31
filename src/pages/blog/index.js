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
import Layout from "../../components/Layout";
import BlogRoll from "../../components/BlogRoll";
import FullWidthImage from "../../components/FullWidthImage";
import { Link, graphql } from "gatsby";

export default class BlogIndexPage extends React.Component {
  render() {
    return (
      <Layout>
        <FullWidthImage 
          img={{ url: "/img/MindGarden_Banner.png" }} 
          title="MindGarden Blogs" 
          subheading="Stay up to date on the latest news, research and technologies from MindGarden AI."
          height={400}
        />
        <div className="blog-section-wrapper">
          <div className="blog-section">
            <section className="container">
              <hr className="tp-rule"/>
              <br />
              <BlogRoll />
              <br />
              <hr className="tp-rule"/>
            </section>
          </div>
        </div>
      </Layout>
    );
  }
}


