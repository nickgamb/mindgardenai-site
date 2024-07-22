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
              className="has-text-weight-bold is-size-3-mobile is-size-2-tablet is-size-1-widescreen"
              style={{
                boxShadow: "#7035cc1a 0.5rem -5px 0px",
                backgroundColor: "#7035cc9c",
                color: "white",
                lineHeight: "1",
                padding: "0.25em",
                margin: "0",
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
