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
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <img
            src={lgicon}
            alt="MindGarden Icon"
            style={{ width: "2.5em", height: "auto", marginBottom: '0.5rem' }}
          />
          <span style={{ fontSize: '2rem', color: '#7035CC', fontWeight: 'bold', letterSpacing: '0.1em' }}>
            MINDGARDEN AI
          </span>
          <div className="column social">
              <a title="linkedin" href="https://www.linkedin.com/company/mindgarden-ai">
                <img
                  src={linkedin}
                  alt="LinkedIn"
                  style={{ width: "1em", height: "1em" }}
                />
              </a>
              <a title="Discord" href="https://discord.gg/WaxMJN7t">
                <img
                  src={discord}
                  alt="Discord"
                  style={{ width: "1em", height: "1em" }}
                />
              </a>
              <a title="instagram" href="https://instagram.com">
                <img
                  src={instagram}
                  alt="Instagram"
                  style={{ width: "1em", height: "1em" }}
                />
              </a>
              <a title="TikTok" href="https://tiktok.com">
                <img
                  src={tiktok}
                  alt="TikTok"
                  style={{ width: "1em", height: "1em" }}
                />
              </a>
            </div>
        </div>
      </div>
      <div className="content has-text-centered has-background-black has-text-white-ter">
        <div className="container has-background-black has-text-white-ter">
          <div style={{ maxWidth: "100vw" }} className="columns">
            <div className="column is-4">
              <section className="menu">
                <ul className="menu-list">
                  <li>
                    <Link to="/" className="navbar-item">
                      Home
                    </Link>
                  </li>
                  <li>
                    <Link className="navbar-item" to="/about">
                      About
                    </Link>
                 </li>
                </ul>
              </section>
            </div>
            <div className="column is-4">
              <section>
                <ul className="menu-list">
                  <li>
                    <Link className="navbar-item" to="/blog">
                      Blog
                    </Link>
                  </li>
                  <li>
                    <Link className="navbar-item" to="/podcast">
                      Podcast
                    </Link>
                  </li>
                </ul>
              </section>
            </div>
            <div className="column is-4">
              <section>
                <ul className="menu-list">
                  <li>
                    <Link className="navbar-item" to="/contact">
                      Contact
                    </Link>
                  </li>
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
