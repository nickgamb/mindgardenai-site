// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com

import React, { useEffect, useRef, useState } from 'react';

const CraneScavengerEffect = () => {
  const [stage, setStage] = useState('drawing'); // drawing → idle → input → explode → complete
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);
  const [startTime, setStartTime] = useState(null); // Initialize as null to prevent hydration mismatch
  const [showInput, setShowInput] = useState(false);
  const [explosionComplete, setExplosionComplete] = useState(false);
  const [countdown, setCountdown] = useState('Loading...');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [craneSVG, setCraneSVG] = useState('');
  const [isMounted, setIsMounted] = useState(false); // Hydration safety
  const [elapsedTime, setElapsedTime] = useState(0);
  const [isMobile, setIsMobile] = useState(false);
  const svgRef = useRef(null);
  const canvasRef = useRef(null);
  const passwordInputRef = useRef(null);
  const correctPassword = process.env.GATSBY_PATTERN_SALT;

  // Set target date for countdown - July 30, 2025 at noon
  const targetDate = useRef(new Date('2025-07-30T12:00:00')); // Use ref to prevent re-creation

  // Hydration safety - only run client-side code after mounting
  useEffect(() => {
    setIsMounted(true);
    setStartTime(Date.now()); // Set start time only on client
    
    // Mobile detection
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    
    checkMobile(); // Initial check
    window.addEventListener('resize', checkMobile);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Load SVG content
  useEffect(() => {
    // Use different SVG file for mobile
    const svgPath = isMobile ? '/crane_mobile.svg' : '/crane.svg';
    
    fetch(svgPath)
      .then(response => response.text())
      .then(svgText => {
        setCraneSVG(svgText);
      })
      .catch(error => console.error('Error loading crane SVG:', error));
  }, [isMobile]); // Add isMobile as dependency

  useEffect(() => {
    // Only start the animation timing once SVG is loaded
    if (!craneSVG) return;
    
    const drawTimer = setTimeout(() => {
      setStage('idle');
      setShowInput(true);
    }, 2000); // Wait for draw animation to complete

    return () => clearTimeout(drawTimer);
  }, [craneSVG]);

  // Countdown timer logic with performance optimization - only run after hydration
  useEffect(() => {
    if (!isMounted) return; // Don't run until hydrated
    
    const updateCountdown = () => {
      // Only update if page is visible (performance optimization)
      if (document.hidden) return;
      
      const now = new Date();
      const diff = Math.max(0, targetDate.current - now);
      
      // Update elapsed time
      if (startTime) {
        setElapsedTime(Math.floor((now - startTime) / 1000));
      }
      
      if (diff === 0) {
        setCountdown('00:00:00');
        return;
      }
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const minutes = Math.floor((diff / (1000 * 60)) % 60);
      const seconds = Math.floor((diff / 1000) % 60);
      
      // Format with days if more than 24 hours left
      if (days > 0) {
        setCountdown(`${days}d ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`);
      } else {
        setCountdown(`${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`);
      }
    };

    updateCountdown(); // Initial call
    const interval = setInterval(updateCountdown, 1000);
    
    // Update immediately when page becomes visible
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        updateCountdown();
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      clearInterval(interval);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [isMounted]);

  // Smoke canvas effect
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationFrame;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Particle constructor
    class SmokeParticle {
      constructor() {
        this.reset();
      }
    
      reset() {
        this.x = Math.random() * canvas.width;
        this.y = canvas.height + Math.random() * 50;
    
        // Smaller size range (e.g., 4px to 8px)
        this.size = Math.random() * 4 + 4;
    
        // Slightly lower opacity for more subtle smoke
        this.opacity = Math.random() * 0.15 + 0.03;
    
        // Keep it drifting upward slowly
        this.speedY = Math.random() * -0.4 - 0.1;
    
        // Slight horizontal wobble
        this.speedX = Math.random() * 0.2 - 0.1;
      }
    
      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        if (this.y < -50 || this.opacity <= 0) this.reset();
      }
    
      //draw(ctx) {
        //ctx.beginPath();
        //ctx.fillStyle = `rgba(200, 200, 200, ${this.opacity})`;
        //ctx.fillStyle = `rgba(220, 230, 255, ${this.opacity})`;  // Soft bluish-white
        //ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        //ctx.fill();
      //}
    //}

      draw(ctx) {
        // Create a more visible radial gradient with better contrast
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 2);
        
        // Use brighter, more visible colors with higher opacity
        gradient.addColorStop(0, `rgba(255, 255, 255, ${this.opacity * 1.2})`); // Bright white center
        gradient.addColorStop(0.3, `rgba(180, 220, 255, ${this.opacity * 0.8})`); // Light blue
        gradient.addColorStop(0.7, `rgba(120, 180, 255, ${this.opacity * 0.4})`); // Medium blue
        gradient.addColorStop(1, `rgba(80, 140, 255, 0)`); // Fade to transparent
      
        ctx.beginPath();
        ctx.fillStyle = gradient;
        ctx.arc(this.x, this.y, this.size * 1.5, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  
    // Mobile optimization - fewer particles on smaller screens
    const particleCount = window.innerWidth < 500 ? 40 : 60;
    
    // Populate particles
    for (let i = 0; i < particleCount; i++) {
      particles.push(new SmokeParticle());
    }

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        p.update();
        p.draw(ctx);
      });
      animationFrame = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      cancelAnimationFrame(animationFrame);
      window.removeEventListener('resize', resizeCanvas);
    };
  }, []);

  const triggerExplosion = () => {
    setStage('explode');
    
    // Trigger the SVG explosion animation programmatically
    if (svgRef.current) {
      const svgElement = svgRef.current.querySelector('svg');
      if (svgElement) {
        // Add a trigger element to start the explosion animation
        const trigger = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
        trigger.setAttribute('id', 'craneBreakaway');
        trigger.setAttribute('attributeName', 'opacity');
        trigger.setAttribute('from', '1');
        trigger.setAttribute('to', '0');
        trigger.setAttribute('dur', '1.2s');
        trigger.setAttribute('begin', '0s');
        svgElement.appendChild(trigger);
      }
    }
    
    // After explosion animation completes, show the new background
    setTimeout(() => {
      setExplosionComplete(true);
      setStage('complete');
    }, 1200); // Match the SVG explosion duration
  };

  const handlePasswordSubmit = async () => {
    const trimmedPassword = password.trim().toLowerCase();
    
    if (!trimmedPassword || isSubmitting) return;
    
    setIsSubmitting(true);
    
    // Add slight delay for better UX feedback
    await new Promise(resolve => setTimeout(resolve, 300));
    
    if (trimmedPassword === correctPassword) {
      triggerExplosion();
    } else {
      setError(true);
      setPassword('');
      // Focus back to input for better accessibility
      setTimeout(() => {
        passwordInputRef.current?.focus();
        setError(false);
      }, 2000);
    }
    
    setIsSubmitting(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handlePasswordSubmit();
    }
  };

  // Use state-managed elapsed time (updated in timer effect)

  return (
    <div className={`crane-gate-container stage-${stage} ${isMobile ? 'is-mobile' : 'is-desktop'}`}>
      {/* Background Images */}
      <div className="crane-backgrounds">
        <img 
          src="/img/crane_background1.PNG" 
          className={`crane-bg visible`} 
          alt="Background" 
        />
        <img 
          src="/img/crane_background2.png" 
          className={`crane-bg bg-alt`} 
          alt="Reveal Background" 
        />
      </div>

      {/* Smoke Canvas */}
      <canvas
        ref={canvasRef}
        className="crane-smoke-canvas"
        style={{
          position: 'absolute',
          top: 0, 
          left: 0,
          width: '100%',
          height: '100%',
          zIndex: 1,
          pointerEvents: 'none',
          opacity: stage === 'explode' ? 1 : 0.4,
          transition: 'opacity 1s ease'
        }}
      />

      {/* Shockwave Effect */}
      <div className={`shockwave ${stage === 'explode' ? 'active' : ''}`} />

      {/* Crane SVG */}
      <div className="crane-svg-container">
        {craneSVG ? (
          <div
            className={`crane-svg stage-${stage}`}
            ref={svgRef}
            dangerouslySetInnerHTML={{ __html: craneSVG }}
          />
        ) : (
          <div className="crane-svg-loading">
            Loading crane...
          </div>
        )}
      </div>

      {/* UI Overlay */}
      {showInput && !explosionComplete && (
        <div className="crane-ui-overlay">
          <div className="crane-interface-card">
            <div className="crane-timer">
              <div className="countdown-display">
                <span className="countdown-icon">🕐</span>
                <span className="countdown-text">{countdown}</span>
              </div>
              <div className="elapsed-display">
                <span className="timer-icon">⏳</span>
                <span className="timer-text">{elapsedTime}s</span>
              </div>
            </div>
            
            <div className="crane-input-group">
              <label htmlFor="crane-password-input" className="visually-hidden">
                Enter the password sequence
              </label>
              <input
                id="crane-password-input"
                ref={passwordInputRef}
                className={`crane-password ${error ? 'crane-error' : ''}`}
                placeholder="Enter the password sequence..."
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyDown={handleKeyPress}
                autoFocus
                autoComplete="off"
                spellCheck="false"
                aria-invalid={error}
                aria-describedby={error ? "crane-error-message" : undefined}
                disabled={isSubmitting}
              />
              <button 
                className="crane-submit" 
                onClick={handlePasswordSubmit}
                disabled={!password.trim() || isSubmitting}
                aria-label="Submit password to unlock the crane gate"
              >
                <span>{isSubmitting ? '🔄' : '🔓'}</span>
                {isSubmitting ? 'Unlocking...' : 'Unlock'}
              </button>
              
              {!isSubmitting && (
                <div className="crane-hint">
                  <span>💡</span>
                  Press Enter to submit
                </div>
              )}
            </div>

            {error && (
              <div 
                id="crane-error-message"
                className="crane-error-message"
                role="alert"
                aria-live="polite"
              >
                <span>🚫</span>
                Sequence incorrect. The crane remains sealed.
              </div>
            )}
          </div>
        </div>
      )}

      {/* Success State */}
      {explosionComplete && (
        <div className="crane-success-overlay" role="dialog" aria-labelledby="success-title">
          <div className="success-message animate-fade-in">
            <h2 id="success-title" className="enhanced-title">🕊️ The Gate Opens</h2>
            <p>The crane has dissolved, revealing the path forward...</p>
            <div className="success-actions">
              <button 
                className="continue-button"
                onClick={() => window.location.href = '/'}
                autoFocus
              >
                Continue Journey
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CraneScavengerEffect; 