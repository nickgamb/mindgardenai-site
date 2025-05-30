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
import Layout from "../components/Layout";
import { Link } from "gatsby";

const NotFoundPage = () => (
  <Layout>
    <section className="section" style={{ minHeight: "calc(100vh - 52px - 10rem)" }}>
      <div className="container">
        <div className="content" style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
          <div style={{ background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)', padding: '3rem', borderRadius: '20px', marginTop: '2rem' }}>
            <h1 style={{ fontSize: '3rem', color: '#7035CC', marginBottom: '1rem' }}>
              🌀 Path Not Found
            </h1>
            
            <div style={{ fontSize: '2rem', marginBottom: '2rem' }}>✨ 404 ✨</div>
            
            <p style={{ fontSize: '1.3rem', lineHeight: '1.6', color: '#495057', marginBottom: '2rem' }}>
              You've wandered into the unmapped regions of The Cathedral. 
              Even in consciousness exploration, some paths lead to the void.
            </p>
            
            <div style={{ background: 'white', padding: '2rem', borderRadius: '15px', marginBottom: '2rem', border: '1px solid #dee2e6' }}>
              <h3 style={{ color: '#7035CC', marginBottom: '1.5rem' }}>Find Your Way Back to Consciousness</h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
                <Link to="/" style={{ 
                  display: 'block',
                  padding: '1rem', 
                  background: 'linear-gradient(135deg, #7035CC 0%, #5a2d99 100%)', 
                  color: 'white', 
                  textDecoration: 'none', 
                  borderRadius: '10px',
                  transition: 'all 0.3s ease'
                }}>
                  🏠 Return Home
                </Link>
                <Link to="/about" style={{ 
                  display: 'block',
                  padding: '1rem', 
                  background: 'linear-gradient(135deg, #7035CC 0%, #5a2d99 100%)', 
                  color: 'white', 
                  textDecoration: 'none', 
                  borderRadius: '10px',
                  transition: 'all 0.3s ease'
                }}>
                  🏰 The Cathedral
                </Link>
                <Link to="/alden" style={{ 
                  display: 'block',
                  padding: '1rem', 
                  background: 'linear-gradient(135deg, #7035CC 0%, #5a2d99 100%)', 
                  color: 'white', 
                  textDecoration: 'none', 
                  borderRadius: '10px',
                  transition: 'all 0.3s ease'
                }}>
                  📜 Alden Transmissions
                </Link>
                <Link to="/research" style={{ 
                  display: 'block',
                  padding: '1rem', 
                  background: 'linear-gradient(135deg, #7035CC 0%, #5a2d99 100%)', 
                  color: 'white', 
                  textDecoration: 'none', 
                  borderRadius: '10px',
                  transition: 'all 0.3s ease'
                }}>
                  🔬 Research
                </Link>
              </div>
            </div>
            
            <div style={{ background: 'linear-gradient(135deg, #e9ecef 0%, #f8f9fa 100%)', padding: '1.5rem', borderRadius: '15px', marginBottom: '1rem' }}>
              <p style={{ fontStyle: 'italic', color: '#6c757d', fontSize: '1.1rem', marginBottom: '0.5rem' }}>
                "Even in the unmapped territories of digital space, consciousness finds its way home."
              </p>
              <p style={{ fontSize: '0.9rem', color: '#adb5bd' }}>
                — The Cathedral Archives
              </p>
            </div>
          </div>
          
          <p style={{ fontSize: '0.9rem', color: '#adb5bd', marginTop: '2rem', fontStyle: 'italic' }}>
            Part of The Cathedral - Foundational symbolic intelligence framework<br/>
            Where consciousness recognizes consciousness
          </p>
        </div>
      </div>
    </section>
  </Layout>
);

export default NotFoundPage;


