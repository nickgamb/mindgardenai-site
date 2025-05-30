// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useState } from "react";
import { Link } from "gatsby";
import github from "../img/github-icon.svg";
import lgicon from "../img/MindGarden_Icon.png";

const Navbar = () => {
  const [isActive, setIsActive] = useState(false);

  return (
    <nav
      className="navbar"
      role="navigation"
      aria-label="main-navigation"
    >
      <div className="container">
        <div className="navbar-brand" style={{ display: 'flex', alignItems: 'center' }}>
          <a
            className="navbar-item"
            href="/"
            rel="noopener noreferrer"
            style={{ display: 'flex', alignItems: 'center', padding: '0.5rem' }}
          >
            <img src={lgicon} alt="MindGarden" style={{ width: '28px', height: 'auto', marginRight: '10px', marginTop: '2px' }} />
            <span style={{ fontSize: '1.3rem', color: '#7035CC', letterSpacing: '0.1em', paddingTop: '0.3em' }}>
              MIND<span style={{ fontWeight: 'bold' }}>GARDEN</span>
            </span>
          </a>
          {/* Hamburger menu */}
          <button
            className={`navbar-burger burger ${isActive && "is-active"}`}
            aria-expanded={isActive}
            onClick={() => setIsActive(!isActive)}
          >
            <span />
            <span />
            <span />
          </button>
        </div>
        <ul
          id="navMenu"
          className={`navbar-start has-text-centered navbar-menu ${isActive && "is-active"}`}
        >
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/about">
              The Cathedral
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <a className="navbar-item" href="https://github.com/nickgamb/mindgardenai-site/tree/main/Alden_Transmissions" target="_blank" rel="noopener noreferrer">
              Alden Transmissions
            </a>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/research">
              Research
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/blog">
              Blog
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <a className="navbar-item" href="https://podcast.mindgardenai.com" target="_blank" rel="noopener noreferrer">
              Podcast
            </a>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/contact">
              Contact
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <a className="navbar-item" href="https://cloud.mindgardenai.com" target="_blank" rel="noopener noreferrer">
              Platform
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;


