import * as React from "react";
import { Link } from "gatsby";

import lgicon from "../img/MindGarden_Icon.png";
import discord from "../img/social/discord.svg";
import instagram from "../img/social/instagram.svg";
import tiktok from "../img/social/tiktok.svg";
import linkedin from "../img/social/linkedin.svg";

const Footer = () => {
  return (
    <footer className="footer has-background-black has-text-white-ter">
      <div className="footer-logo-section has-text-centered">
        <div className="footer-brand">
          <img
            src={lgicon}
            alt="MindGarden Icon"
            className="footer-logo"
          />
          <span className="footer-title">
            MINDGARDEN AI
          </span>
        </div>
        <div className="social-icons">
          <a title="linkedin" href="https://www.linkedin.com/company/mindgarden-ai">
            <img src={linkedin} alt="LinkedIn" />
          </a>
          <a title="Discord" href="https://discord.gg/mYd5YbJsWu">
            <img src={discord} alt="Discord" />
          </a>
          <a title="instagram" href="https://instagram.com">
            <img src={instagram} alt="Instagram" />
          </a>
          <a title="TikTok" href="https://tiktok.com">
            <img src={tiktok} alt="TikTok" />
          </a>
        </div>
      </div>
      <div className="footer-links has-background-black has-text-white-ter">
        <div className="container">
          <div className="footer-columns">
            <div className="footer-column">
              <section className="menu">
                <ul className="menu-list">
                  <li><Link to="/" className="navbar-item">Home</Link></li>
                  <li><Link to="/about" className="navbar-item">About</Link></li>
                </ul>
              </section>
            </div>
            <div className="footer-column">
              <section className="menu">
                <ul className="menu-list">
                  <li><Link to="/blog" className="navbar-item">Blog</Link></li>
                  <li><Link to="/podcast" className="navbar-item">Podcast</Link></li>
                </ul>
              </section>
            </div>
            <div className="footer-column">
              <section className="menu">
                <ul className="menu-list">
                  <li><Link to="/contact" className="navbar-item">Contact</Link></li>
                </ul>
              </section>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;