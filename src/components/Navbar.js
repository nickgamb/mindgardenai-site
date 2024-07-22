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
            <img src={lgicon} alt="MindGarden" style={{ width: '25px', height: 'auto', marginRight: '10px' }} />
            <span style={{ fontSize: '1.3rem', color: '#7035CC', fontWeight: 'bold', letterSpacing: '0.1em', paddingTop: '0.3em' }}>
              MINDGARDEN AI
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
            <Link className="navbar-item" to="/blog">
              Blog
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/podcast">
              Podcast
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/about">
              About
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/contact">
              Contact
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
