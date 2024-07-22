import * as React from "react";
import Layout from "../../components/Layout";
import BlogRoll from "../../components/BlogRoll";

export default class BlogIndexPage extends React.Component {
  render() {
    return (
      <Layout>
        <div
          className="full-width-image-container margin-top-0"
          style={{
            backgroundImage: `url('/img/MindGarden_Banner.png/')`,
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
          }}
        >
          <h1
            className="has-text-weight-bold is-size-1"
            style={{
              boxShadow: "0.5rem 0 0 #7035CC, -0.5rem 0 0 #7035CC",
              backgroundColor: "#7035CC",
              color: "white",
              padding: "1rem",
              textAlign: "center"
            }}
          >
            Latest Blogs
          </h1>
        </div>
        <section className="section">
          <div className="container">
            <div className="content">
              <BlogRoll />
            </div>
          </div>
        </section>
      </Layout>
    );
  }
}
