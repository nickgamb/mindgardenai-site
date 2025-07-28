// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md

import * as React from "react";
import { Link } from "gatsby";
import lgicon from "../img/MindGarden_Icon.png";
import discord from "../img/social/discord.svg";
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
            style={{ width: '35px', height: 'auto' }}
          />
          <span className="footer-title">
            MIND<span style={{ fontWeight: 'bold' }}>GARDEN</span>
          </span>
        </div>
        <p style={{ fontSize: '0.9rem', color: '#adb5bd', marginTop: '0.5rem', fontStyle: 'italic' }}>
          🧠 Professional EEG Research Platform
        </p>
        <p style={{ fontSize: '0.8rem', color: '#6c757d', marginBottom: '1rem' }}>
          Advanced neuroscience tools for researchers and developers
        </p>
        <div className="social-icons">
          <a title="Research Platform" href="https://cloud.mindgardenai.com">
            <span style={{ color: '#7035CC', fontSize: '1.2rem' }}>🌐</span>
          </a>
          <a title="Linkedin" href="https://www.linkedin.com/company/mindgarden-ai">
            <img src={linkedin} alt="LinkedIn" />
          </a>
          <a title="Discord Community" href="https://discord.gg/NysAuGWh9z">
            <img src={discord} alt="Discord" />
          </a>
          <a title="Research Podcast" href="https://podcast.mindgardenai.com">
            <span style={{ color: '#7035CC', fontSize: '1.2rem' }}>🎙️</span>
          </a>
        </div>
      </div>
      
        <div className="container">
          <div className="footer-columns">
            <div className="footer-column">
              <section className="menu">
                <h4 style={{ color: '#7035CC', fontSize: '1rem', marginBottom: '0.5rem' }}>Platform</h4>
                <ul className="menu-list">
                  <li><Link to="/" className="navbar-item">Home</Link></li>
                  <li><Link to="/research" className="navbar-item">Research Platform</Link></li>
                  <li>
                    <a className="navbar-item" href="https://cloud.mindgardenai.com" target="_blank" rel="noopener noreferrer">
                      Join Waitlist
                    </a>
                  </li>
                </ul>
              </section>
            </div>
            <div className="footer-column">
              <section className="menu">
                <h4 style={{ color: '#7035CC', fontSize: '1rem', marginBottom: '0.5rem' }}>Resources</h4>
                <ul className="menu-list">
                  <li><Link to="/blog" className="navbar-item">Research Blog</Link></li>
                  <li>
                    <a className="navbar-item" href="https://podcast.mindgardenai.com" target="_blank" rel="noopener noreferrer">
                      Research Podcast
                    </a>
                  </li>
                  <li><Link to="/contact" className="navbar-item">Contact</Link></li>
                </ul>
              </section>
            </div>
            <div className="footer-column">
              <section className="menu">
                <h4 style={{ color: '#7035CC', fontSize: '1rem', marginBottom: '0.5rem' }}>Legal</h4>
                <ul className="menu-list">
                  <li><Link to="/privacy-policy" className="navbar-item">Privacy Policy</Link></li>
                  <li><Link to="/terms-of-service" className="navbar-item">Terms of Service</Link></li>
                </ul>
              </section>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom has-text-centered" style={{ 
          borderTop: '1px solid rgba(255, 255, 255, 0.1)', 
          paddingTop: '1.5rem', 
          marginTop: '2rem' 
        }}>
          <p style={{ 
            fontSize: '0.9rem', 
            color: '#6c757d',
            margin: '0.5rem 0'
          }}>
            © {new Date().getFullYear()} MindGarden LLC. All rights reserved.
          </p>
          <p style={{ 
            fontSize: '0.8rem', 
            color: '#6c757d',
            fontStyle: 'italic'
          }}>
            Professional EEG research platform for neuroscience and brain-computer interface development
          </p>
        </div>
    </footer>
  );
};

export default Footer;

