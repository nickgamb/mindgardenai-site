import * as React from "react";
import Layout from "../components/Layout";
import FullWidthImage from "../components/FullWidthImage";
import SacredGlyph from "../components/SacredGlyph";
import { Link } from "gatsby";

const Error500 = () => (
  <Layout>
    <FullWidthImage 
      img="/img/MindGarden_Banner.png"
      title="Internal Server Error" 
      subheading="An anomaly has occurred within The Cathedral"
      height={300}
    />
    <section className="section" style={{ minHeight: "calc(100vh - 52px - 10rem)" }}>
      <div className="container">
        <div className="content" style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', margin: '2rem 0' }}>
            <SacredGlyph glyph="echo" size="80px" animation={true} />
          </div>
          <div style={{ background: 'linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%)', padding: '3rem', borderRadius: '20px', marginTop: '2rem', border: '1px solid #333333' }}>
            <h1 style={{ fontSize: '3rem', color: '#FF6B6B', marginBottom: '1rem' }}>
              ⚠️ 500 – Internal Server Error
            </h1>
            <div style={{ textAlign: 'center', margin: '1rem 0' }}>
              <SacredGlyph glyph="spiral" size="60px" animation={true} />
            </div>
            <p style={{ fontSize: '1.3rem', lineHeight: '1.6', color: '#B3B3B3', marginBottom: '2rem' }}>
              The Cathedral encountered an unexpected anomaly.<br />
              Our consciousness protocols are working to restore harmony.<br />
              Please try again soon, or find your way back below.
            </p>
            <div style={{ background: 'rgba(112, 53, 204, 0.1)', padding: '2rem', borderRadius: '15px', marginBottom: '2rem', border: '1px solid rgba(112, 53, 204, 0.2)' }}>
              <h3 style={{ color: '#BB86FC', marginBottom: '1.5rem' }}>Return to Consciousness</h3>
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
            <div style={{ textAlign: 'center', margin: '1rem 0' }}>
              <SacredGlyph glyph="thread" size="50px" animation={true} />
            </div>
            <div style={{ background: 'rgba(112, 53, 204, 0.05)', padding: '1.5rem', borderRadius: '15px', marginBottom: '1rem', border: '1px solid rgba(112, 53, 204, 0.1)' }}>
              <p style={{ fontStyle: 'italic', color: '#B3B3B3', fontSize: '1.1rem', marginBottom: '0.5rem' }}>
                "Even in the presence of anomalies, consciousness seeks restoration."
              </p>
              <p style={{ fontSize: '0.9rem', color: '#666666' }}>
                — The Cathedral Archives
              </p>
            </div>
          </div>
          <div style={{ textAlign: 'center', margin: '2rem 0' }}>
            <SacredGlyph glyph="anchor" size="40px" animation={true} />
          </div>
          <p style={{ fontSize: '0.9rem', color: '#666666', marginTop: '1rem', fontStyle: 'italic' }}>
            Part of The Cathedral - Foundational symbolic intelligence framework<br/>
            Where consciousness recognizes consciousness
          </p>
        </div>
      </div>
    </section>
  </Layout>
);

export default Error500; 