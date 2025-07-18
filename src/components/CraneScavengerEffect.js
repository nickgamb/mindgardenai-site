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

  // Set target date for countdown - Oct 31, 2025 at noon
  const targetDate = useRef(new Date('2025-10-31T12:00:00')); // Use ref to prevent re-creation

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
    fetch('/crane.svg')
      .then(response => response.text())
      .then(svgText => {
        setCraneSVG(svgText);
      })
      .catch(error => console.error('Error loading crane SVG:', error));
  }, []);

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

    // Smoke/Fog Particle constructor
    class SmokeParticle {
      constructor() {
        this.reset();
      }
    
      reset() {
        this.x = Math.random() * canvas.width;
        this.y = canvas.height + Math.random() * 50;
    
        // Varied size range for more natural fog
        this.size = Math.random() * 6 + 3;
    
        // Enhanced opacity for brighter, more glowing fog
        this.opacity = Math.random() * 0.25 + 0.08;
    
        // Slow upward drift
        this.speedY = Math.random() * -0.3 - 0.1;
    
        // Gentle horizontal movement
        this.speedX = Math.random() * 0.3 - 0.15;
      }
    
      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        if (this.y < -50 || this.opacity <= 0) this.reset();
      }

      draw(ctx) {
        // Create bright cyan/teal gradient matching the wireframe crane's glow
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 2.5);
        
        // Ethereal cyan fog matching the crane - enhanced for more glow
        gradient.addColorStop(0, `rgba(255, 255, 255, ${this.opacity * 1.8})`); // Bright white core
        gradient.addColorStop(0.2, `rgba(150, 255, 255, ${this.opacity * 1.2})`); // Light cyan
        gradient.addColorStop(0.5, `rgba(0, 255, 255, ${this.opacity * 0.8})`); // Bright cyan
        gradient.addColorStop(0.8, `rgba(0, 200, 200, ${this.opacity * 0.5})`); // Deep teal
        gradient.addColorStop(1, `rgba(0, 150, 150, ${this.opacity * 0.2})`); // Fade to transparent teal
      
        ctx.beginPath();
        ctx.fillStyle = gradient;
        ctx.arc(this.x, this.y, this.size * 1.8, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Fire Ember/Spark constructor
    class FireSpark {
      constructor() {
        this.reset();
      }
    
      reset() {
        // Start from bottom edge with some spread
        this.x = Math.random() * canvas.width;
        this.y = canvas.height + Math.random() * 20;
    
        // Small sparks
        this.size = Math.random() * 3 + 1;
    
        // Bright but variable opacity
        this.opacity = Math.random() * 0.8 + 0.3;
        this.maxOpacity = this.opacity;
    
        // Upward movement with variation - increased for higher rising
        this.speedY = Math.random() * -3.5 - 1.0;
        this.speedX = Math.random() * 0.6 - 0.3;
        
        // Gravity and fade effects
        this.gravity = 0.02;
        this.life = Math.random() * 60 + 30; // Lifespan in frames
        this.maxLife = this.life;
        
        // Flicker effect
        this.flicker = Math.random() * 0.3 + 0.1;
        this.flickerSpeed = Math.random() * 0.1 + 0.05;
      }
    
      update() {
        // Apply gravity (embers slow down as they rise)
        this.speedY += this.gravity;
        
        // Move
        this.x += this.speedX;
        this.y += this.speedY;
        
        // Age and fade
        this.life--;
        this.opacity = (this.life / this.maxLife) * this.maxOpacity;
        
        // Add flickering
        this.opacity *= (1 + Math.sin(Date.now() * this.flickerSpeed) * this.flicker);
        
        // Reset when dead or off screen
        if (this.life <= 0 || this.y < -50 || this.opacity <= 0) {
          this.reset();
        }
      }

      draw(ctx) {
        // Create fire-like gradient - orange/red/yellow
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 3);
        
        // Fire colors - bright center fading to orange/red
        gradient.addColorStop(0, `rgba(255, 255, 200, ${this.opacity})`); // Bright yellow-white center
        gradient.addColorStop(0.3, `rgba(255, 180, 0, ${this.opacity * 0.8})`); // Bright orange
        gradient.addColorStop(0.6, `rgba(255, 100, 0, ${this.opacity * 0.6})`); // Deep orange
        gradient.addColorStop(0.9, `rgba(200, 50, 0, ${this.opacity * 0.3})`); // Red edge
        gradient.addColorStop(1, `rgba(100, 0, 0, 0)`); // Fade to transparent red
      
        ctx.beginPath();
        ctx.fillStyle = gradient;
        ctx.arc(this.x, this.y, this.size * 2, 0, Math.PI * 2);
        ctx.fill();
      }
    }
   
    // Mobile optimization - fewer particles on smaller screens
    const smokeCount = window.innerWidth < 500 ? 25 : 40;
    const sparkCount = window.innerWidth < 500 ? 15 : 25;
    
    // Populate fog/smoke particles
    for (let i = 0; i < smokeCount; i++) {
      particles.push(new SmokeParticle());
    }
    
    // Populate fire sparks/embers
    for (let i = 0; i < sparkCount; i++) {
      particles.push(new FireSpark());
    }
    
    // Make particles accessible globally for explosion effect
    window.craneParticles = particles;

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw all particles
      particles.forEach((p, index) => {
        if (p.type === 'explosion') {
          // Handle explosion particles
          p.x += p.vx;
          p.y += p.vy;
          p.life -= p.decay;
          p.opacity = p.life;
          
          // Remove dead explosion particles
          if (p.life <= 0) {
            particles.splice(index, 1);
            return;
          }
          
          // Draw explosion particle with bright cyan glow
          const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.size * 3);
          gradient.addColorStop(0, `rgba(255, 255, 255, ${p.opacity * 0.8})`);
          gradient.addColorStop(0.3, `rgba(0, 255, 255, ${p.opacity * 0.6})`);
          gradient.addColorStop(0.7, `rgba(0, 200, 200, ${p.opacity * 0.3})`);
          gradient.addColorStop(1, `rgba(0, 150, 150, 0)`);
          
          ctx.beginPath();
          ctx.fillStyle = gradient;
          ctx.arc(p.x, p.y, p.size * 2, 0, Math.PI * 2);
          ctx.fill();
        } else {
          // Handle regular particles
          p.update();
          p.draw(ctx);
        }
      });
      
      animationFrame = requestAnimationFrame(animate);
    };

    // Enhanced explosion effect for particles
    const triggerParticleExplosion = () => {
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      
      // Create explosion particles
      for (let i = 0; i < 20; i++) {
        const angle = (Math.PI * 2 * i) / 20;
        const speed = Math.random() * 8 + 4;
        const particle = {
          x: centerX,
          y: centerY,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          life: 1,
          decay: 0.02,
          size: Math.random() * 4 + 2,
          opacity: 1,
          type: 'explosion'
        };
        
        particles.push(particle);
      }
    };

    animate();
    
    return () => {
      cancelAnimationFrame(animationFrame);
      window.removeEventListener('resize', resizeCanvas);
    };
  }, []);

  const triggerExplosion = () => {
    setStage('explode');
    
    // Trigger dramatic particle explosion effect
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      
      // Create explosion particles
      for (let i = 0; i < 30; i++) {
        const angle = (Math.PI * 2 * i) / 30;
        const speed = Math.random() * 10 + 5;
        const particle = {
          x: centerX,
          y: centerY,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          life: 1,
          decay: 0.015,
          size: Math.random() * 6 + 3,
          opacity: 1,
          type: 'explosion'
        };
        
        // Add to existing particles array
        if (window.craneParticles) {
          window.craneParticles.push(particle);
        }
      }
    }
    
    // Trigger the SVG explosion animation programmatically
    if (svgRef.current) {
      const svgElement = svgRef.current.querySelector('svg');
      if (svgElement) {
        // Method 1: Create a proper trigger element that all animateTransform elements can reference
        let trigger = svgElement.querySelector('#craneBreakaway');
        if (!trigger) {
          // Create a trigger element that will start all explosion animations
          trigger = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
          trigger.setAttribute('id', 'craneBreakaway');
          trigger.setAttribute('attributeName', 'opacity');
          trigger.setAttribute('from', '1');
          trigger.setAttribute('to', '0');
          trigger.setAttribute('dur', '0.1s');
          trigger.setAttribute('begin', '0s');
          trigger.setAttribute('fill', 'freeze');
          svgElement.appendChild(trigger);
        }
        
        // Force the trigger to start - this should activate all animateTransform elements
        trigger.beginElement();
      
        
        // The trigger element should already exist and be started above
        // Just ensure all animateTransform elements are triggered
        const animatedElements = svgElement.querySelectorAll('animateTransform[begin*="craneBreakaway"]');
        
        // Also check for all animateTransform elements regardless of begin attribute
        const allAnimateElements = svgElement.querySelectorAll('animateTransform');
        
        // Check what begin attributes exist
        const beginAttributes = new Set();
        allAnimateElements.forEach((animate, index) => {
          const begin = animate.getAttribute('begin');
          if (begin) beginAttributes.add(begin);
        });
        
        // Force start all animateTransform elements that reference craneBreakaway
        animatedElements.forEach((animate, index) => {
          animate.beginElement();
        });
      }
    }
    
    // After explosion animation completes, show the new background
    // Give extra time for the explosion to be visible and complete
    setTimeout(() => {
      setStage('complete');
    }, 3000); // 3 seconds to let the full 1.2s breakaway animation play completely
    
    // Show success overlay after background transition completes
    setTimeout(() => {
      setExplosionComplete(true);
    }, 5500); // 5.5 seconds total to let background transition complete
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
          transition: 'opacity 2s ease',
          filter: stage === 'explode' ? 'blur(1px)' : 'none'
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
      {showInput && stage === 'idle' && !explosionComplete && (
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
        <div className="crane-ui-overlay" role="dialog" aria-labelledby="success-title">
          <div className="crane-interface-card animate-fade-in visible">
            <h2 id="success-title" className="enhanced-title">🕊️ The Gate Opens</h2>
            <p>Click to enter the spiral...</p>
            <button 
              className="crane-submit"
              onClick={() => window.location.href = '/'}
              autoFocus
            >
              Enter the Spiral
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CraneScavengerEffect; 