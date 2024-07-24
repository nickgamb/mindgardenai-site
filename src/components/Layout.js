import * as React from "react";
import { Helmet } from "react-helmet";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import "../style/bulma-style.sass";
import "../style/custom-style.sass";
import useSiteMetadata from "./SiteMetadata";
import { withPrefix } from "gatsby";
import '@thumbtack/thumbprint-scss';

const TemplateWrapper = ({ children }) => {
  const { title, description } = useSiteMetadata();
  return (
    <div>
      <Helmet>
        <html lang="en" />
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />

        <link
          rel="apple-touch-icon"
          sizes="180x170"
          href={`${withPrefix("/")}img/mindgardennologo.png`}
        />
        <link
          rel="icon"
          type="image/png"
          href={`${withPrefix("/")}img/mindgardennologo.png`}
          sizes="32x25"
        />
        <link
          rel="icon"
          type="image/png"
          href={`${withPrefix("/")}img/mindgardennologo.png`}
          sizes="16x10"
        />

        <link
          rel="mask-icon"
          href={`${withPrefix("/")}img/mindgardennologo.png`}
          color="#ff4400"
        />

        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet" />
        
        <meta name="theme-color" content="#161616" />

        <meta property="og:type" content="business.business" />
        <meta property="og:title" content={title} />
        <meta property="og:url" content="/" />
        <meta
          property="og:image"
          content={`${withPrefix("/")}img/MindGarden.png`}
        />
        <meta name="google-adsense-account" content="ca-pub-5509488659978116">
      </Helmet>
      <Navbar />
      <main className="site-content">{children}</main>
      <Footer />
    </div>
  );
};

export default TemplateWrapper;
