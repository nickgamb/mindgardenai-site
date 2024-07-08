import React, { useState } from "react";
import { Link } from "gatsby";
import github from "../img/github-icon.svg";
import logo from "../img/MindGarden.png";
import lgicon from "../img/MindGarden_Icon.png";

const Navbar = () => {
  const [isActive, setIsActive] = useState(false);

  return (
    <nav
      className="navbar is-transparent"
      role="navigation"
      aria-label="main-navigation"
    >
      <div className="container">
        <div className="navbar-brand" style={{ display: 'flex', alignItems: 'center' }}>
          <a
            className="navbar-item"
            href="/"
            target="_blank"
            rel="noopener noreferrer"
          >
            <span className="icon" style={{ display: 'flex', alignItems: 'center' }}>
              <img src={lgicon} alt="MindGarden" />
            </span>
          </a>
          <Link to="/" className="navbar-item" title="Logo" style={{ padding: '0.5rem 1rem' }}>
            <img src={logo} alt="MindGarden" style={{ width: '90px', marginLeft: '0.5rem' }} />
          </Link>
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
          className={`navbar-start has-text-centered navbar-menu ${
            isActive && "is-active"
          }`}
        >
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/about">
              About
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/products">
              Products
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/blog">
              Blog
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/contact">
              Contact
            </Link>
          </li>
          <li className="navbar-item" style={{ padding: '0px' }}>
            <Link className="navbar-item" to="/contact/examples">
              Form Examples
            </Link>
          </li>
          <li className="navbar-end has-text-centered">
            <a
              className="navbar-item"
              href="https://github.com/decaporg/gatsby-plugin-decap-cms"
              target="_blank"
              rel="noopener noreferrer"
            >
              <span className="icon">
                <img src={github} alt="Github" />
              </span>
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
