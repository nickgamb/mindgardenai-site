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
import { navigate } from "gatsby-link";
import Layout from "../../components/Layout";
import FullWidthImage from "../../components/FullWidthImage";
import SacredGlyph from "../../components/SacredGlyph";

function encode(data) {
  return Object.keys(data)
    .map((key) => encodeURIComponent(key) + "=" + encodeURIComponent(data[key]))
    .join("&");
}

export default class Index extends React.Component {
  constructor(props) {
    super(props);
    this.state = { isValidated: false, recaptchaLoaded: false, name: '', email: '', message: '' };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    const script = document.createElement('script');
    script.src = `https://www.google.com/recaptcha/enterprise.js?render=${process.env.GATSBY_RECAPTCHA_SITE_KEY}`;
    script.async = true;
    script.defer = true;
    script.onload = () => {
      this.setState({ recaptchaLoaded: true });
      window.onSubmit = this.handleSubmit;  // Define onSubmit globally
    };
    document.head.appendChild(script);
  }

  handleChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  };

  handleSubmit = async (token) => {
    const form = document.getElementById("contact-form");
    if (this.state.recaptchaLoaded && window.grecaptcha && window.grecaptcha.enterprise) {
      window.grecaptcha.enterprise.ready(async () => {
        try {
          const token = await window.grecaptcha.enterprise.execute(process.env.GATSBY_RECAPTCHA_SITE_KEY, { action: 'submit' });

          const response = await fetch("/.netlify/functions/verify-recaptcha", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              project_id: process.env.GATSBY_GOOGLE_CLOUD_PROJECT_ID,
              site_key: process.env.GATSBY_RECAPTCHA_SITE_KEY,
              token,
              action: 'submit',
              name: this.state.name,
              email: this.state.email,
              message: this.state.message
            }),
          });

          const result = await response.json();

          if (result.success) {
            // reCAPTCHA verification successful, proceed with form submission
            navigate(form.getAttribute("action"));
          } else {
            alert("reCAPTCHA verification failed. Please try again.");
          }
        } catch (error) {
          console.error('reCAPTCHA error:', error);
          alert("An error occurred with reCAPTCHA. Please try again.");
        }
      });
    } else {
      console.error('reCAPTCHA not loaded');
      alert("reCAPTCHA is not loaded. Please refresh the page and try again.");
    }
  };

  render() {
    return (
      <Layout>
        <FullWidthImage 
          img="/img/MindGarden_Banner.png"
          title="Contact Our Research Team" 
          subheading="Connect with consciousness researchers, developers, and collaborators"
          height={400}
        />
        <section className="section" style={{ minHeight: "calc(100vh - 52px - 10rem)" }}>
          <div className="container">
            <div className="content">
              
              <div style={{ marginBottom: '2rem', background: 'linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%)', padding: '2rem', borderRadius: '15px', border: '1px solid #333333' }}>
                <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
                  <SacredGlyph glyph="research" size="60px" animation={true} />
                </div>
                <h2 style={{ color: '#BB86FC', marginBottom: '1rem' }}>Research Collaboration</h2>
                <p style={{ fontSize: '1.1rem', lineHeight: '1.6', color: '#B3B3B3' }}>
                  Whether you're a consciousness researcher, AI developer, academic investigator, or curious explorer, 
                  we welcome dialogue about consciousness research frontiers. Our platform provides collaborative 
                  space for rigorous methodology and scientific investigation.
                </p>
              </div>

              <div style={{ background: '#1E1E1E', padding: '2rem', borderRadius: '15px', marginBottom: '2rem', border: '1px solid #333333' }}>
                <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
                  <SacredGlyph glyph="communicate" size="50px" animation={true} />
                </div>
                <h3 style={{ color: '#BB86FC', marginBottom: '1rem' }}>📬 Send Your Message</h3>
                <p style={{ marginBottom: '1.5rem', color: '#B3B3B3' }}>
                  Share your research vision, questions, or collaboration proposals. Every message receives 
                  careful consideration. Please specify your interest: research collaboration, commercial licensing, 
                  educational resources, or exploratory studies.
                </p>
                
                <form
                  id="contact-form"
                  name="contact"
                  method="post"
                  action="/contact/thanks/"
                  data-netlify="true"
                  data-netlify-honeypot="bot-field"
                  onSubmit={this.handleSubmit}
                >
                  {/* The `form-name` hidden field is required to support form submissions without JavaScript */}
                  <input type="hidden" name="form-name" value="contact" />
                  <div hidden>
                    <label>
                      Don't fill this out:{" "}
                      <input name="bot-field" onChange={this.handleChange} />
                    </label>
                  </div>
                  <div className="field">
                    <label className="label" htmlFor={"name"} style={{ color: '#BB86FC' }}>
                      Your Name *
                    </label>
                    <div className="control">
                      <input
                        className="input"
                        type={"text"}
                        name={"name"}
                        onChange={this.handleChange}
                        id={"name"}
                        required={true}
                        style={{ 
                          borderRadius: '8px', 
                          backgroundColor: '#2D2D2D',
                          border: '1px solid #333333',
                          color: '#FFFFFF'
                        }}
                        placeholder="How should we address you in our correspondence?"
                      />
                    </div>
                  </div>
                  <div className="field">
                    <label className="label" htmlFor={"email"} style={{ color: '#BB86FC' }}>
                      Email Address *
                    </label>
                    <div className="control">
                      <input
                        className="input"
                        type={"email"}
                        name={"email"}
                        onChange={this.handleChange}
                        id={"email"}
                        required={true}
                        style={{ 
                          borderRadius: '8px',
                          backgroundColor: '#2D2D2D',
                          border: '1px solid #333333',
                          color: '#FFFFFF'
                        }}
                        placeholder="your.research@institution.edu"
                      />
                    </div>
                  </div>
                  <div className="field">
                    <label className="label" htmlFor={"message"} style={{ color: '#BB86FC' }}>
                      Your Message *
                    </label>
                    <div className="control">
                      <textarea
                        className="textarea"
                        name={"message"}
                        onChange={this.handleChange}
                        id={"message"}
                        required={true}
                        style={{ 
                          borderRadius: '8px', 
                          minHeight: '150px',
                          backgroundColor: '#2D2D2D',
                          border: '1px solid #333333',
                          color: '#FFFFFF'
                        }}
                        placeholder="Share your research vision, questions, or collaboration proposals. What brings you to The Cathedral?"
                      />
                    </div>
                  </div>
                  <div className="field">
                    <button 
                      className="btn g-recaptcha"
                      data-sitekey={process.env.GATSBY_RECAPTCHA_SITE_KEY}
                      data-callback='onSubmit'
                      data-action='submit'
                      style={{ 
                        background: 'linear-gradient(135deg, #BB86FC 0%, #9A66EA 100%)', 
                        color: '#121212', 
                        padding: '12px 30px', 
                        borderRadius: '25px', 
                        border: 'none',
                        fontSize: '1.1rem',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease',
                        fontWeight: '600'
                      }}
                      onMouseOver={(e) => e.target.style.background = 'linear-gradient(135deg, #D7B7FD 0%, #BB86FC 100%)'}
                      onMouseOut={(e) => e.target.style.background = 'linear-gradient(135deg, #BB86FC 0%, #9A66EA 100%)'}
                    >
                      🌀 Send Message
                    </button>
                  </div>
                </form>
              </div>

              <div style={{ textAlign: 'center', marginTop: '2rem', padding: '1.5rem', background: 'linear-gradient(135deg, #2D2D2D 0%, #1E1E1E 100%)', borderRadius: '15px', border: '1px solid #333333' }}>
                <SacredGlyph glyph="bridge" size="50px" animation={true} />
                <p style={{ fontStyle: 'italic', color: '#B3B3B3', marginBottom: '0.5rem', marginTop: '1rem' }}>
                  "Advancing consciousness research through collaboration and scientific rigor."
                </p>
                <p style={{ fontSize: '0.9rem', color: '#666666' }}>
                  MindGarden AI - Consciousness Research Platform
                </p>
              </div>
            </div>
          </div>
        </section>
      </Layout>
    );
  }
}


