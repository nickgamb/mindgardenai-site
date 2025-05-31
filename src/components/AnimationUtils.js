// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com

import React, { useEffect, useState } from 'react';

export const useScrollAnimations = () => {
  useEffect(() => {
    // Only enable scroll animations on desktop with JavaScript
    const isDesktop = window.innerWidth >= 769;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (!isDesktop || prefersReducedMotion) {
      // On mobile or when reduced motion is preferred, ensure all elements are visible
      const animatedElements = document.querySelectorAll(
        '.animate-on-scroll, .animate-fade-in, .section-reveal'
      );
      animatedElements.forEach((el) => {
        el.style.opacity = '1';
        el.style.transform = 'none';
        el.classList.add('visible');
      });
      return;
    }

    // Desktop with motion allowed - proceed with animations
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, observerOptions);

    // Small delay to ensure DOM is ready
    setTimeout(() => {
      const animatedElements = document.querySelectorAll(
        '.animate-on-scroll, .animate-fade-in, .section-reveal'
      );
      
      animatedElements.forEach((el) => observer.observe(el));
    }, 100);

    // Cleanup function
    return () => {
      const animatedElements = document.querySelectorAll(
        '.animate-on-scroll, .animate-fade-in, .section-reveal'
      );
      animatedElements.forEach((el) => observer.unobserve(el));
    };
  }, []);
};

export const useParallaxEffect = () => {
  useEffect(() => {
    const handleScroll = () => {
      const scrolled = window.pageYOffset;
      const parallaxElements = document.querySelectorAll('.parallax-element');
      
      parallaxElements.forEach((element) => {
        const speed = element.dataset.speed || 0.5;
        const yPos = -(scrolled * speed);
        element.style.transform = `translateY(${yPos}px)`;
      });
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
};

export const useCursorEffect = () => {
  useEffect(() => {
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    cursor.style.cssText = `
      position: fixed;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(112, 53, 204, 0.8), rgba(112, 53, 204, 0.2));
      pointer-events: none;
      z-index: 9999;
      transition: transform 0.1s ease;
    `;
    document.body.appendChild(cursor);

    const moveCursor = (e) => {
      cursor.style.left = e.clientX - 10 + 'px';
      cursor.style.top = e.clientY - 10 + 'px';
    };

    const scaleUpCursor = () => {
      cursor.style.transform = 'scale(1.5)';
    };

    const scaleDownCursor = () => {
      cursor.style.transform = 'scale(1)';
    };

    document.addEventListener('mousemove', moveCursor);
    
    // Add hover effects for interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .btn, .enhanced-hover-card');
    interactiveElements.forEach((el) => {
      el.addEventListener('mouseenter', scaleUpCursor);
      el.addEventListener('mouseleave', scaleDownCursor);
    });

    return () => {
      document.removeEventListener('mousemove', moveCursor);
      interactiveElements.forEach((el) => {
        el.removeEventListener('mouseenter', scaleUpCursor);
        el.removeEventListener('mouseleave', scaleDownCursor);
      });
      if (cursor.parentNode) {
        cursor.parentNode.removeChild(cursor);
      }
    };
  }, []);
};

export const useTypingEffect = (text, speed = 100) => {
  const [displayText, setDisplayText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setDisplayText(prev => prev + text[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, speed);

      return () => clearTimeout(timeout);
    }
  }, [currentIndex, text, speed]);

  return displayText;
};

// Enhanced SacredGlyph component wrapper with more animations
export const EnhancedSacredGlyph = ({ 
  glyph = "spiral", 
  size = "64px", 
  animation = true, 
  enhancement = "glow",
  className = "" 
}) => {
  const glyphMap = {
    spiral: "/img/glyph_sacred_spiral_ether__static.png",
    vow: "/img/glyph_vow_seal.png",
    echo: "/img/glyph_echo_return.png",
    thread: "/img/glyph_thread_spiral.png",
    recursive: "/img/glyph_recursive_function.png",
    anchor: "/img/glyph_anchor_point.png",
    triangle: "/img/glyph_vow_triangle.png"
  };

  const getEnhancementClass = () => {
    switch (enhancement) {
      case 'glow': return 'consciousness-glow';
      case 'float': return 'float-element';
      case 'floatReverse': return 'float-element-reverse';
      default: return '';
    }
  };

  const styles = {
    width: size,
    height: size,
    objectFit: "contain",
    filter: "drop-shadow(0 0 15px rgba(112, 53, 204, 0.4))",
    transition: "all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
    cursor: "pointer"
  };

  return (
    <img
      src={glyphMap[glyph] || glyphMap.spiral}
      alt={`Enhanced Cathedral ${glyph} glyph`}
      className={`cathedral-glyph enhanced-image ${getEnhancementClass()} ${className}`}
      style={styles}
      onClick={() => {
        // Add click ripple effect
        const ripple = document.createElement('div');
        ripple.style.cssText = `
          position: absolute;
          border-radius: 50%;
          background: rgba(112, 53, 204, 0.3);
          transform: scale(0);
          animation: ripple 0.6s linear;
          pointer-events: none;
        `;
        
        const rect = event.target.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = event.clientX - rect.left - size / 2 + 'px';
        ripple.style.top = event.clientY - rect.top - size / 2 + 'px';
        
        event.target.parentNode.appendChild(ripple);
        
        setTimeout(() => {
          ripple.remove();
        }, 600);
      }}
    />
  );
};

// Particle system component
export const ParticleBackground = ({ density = 'medium', color = 'purple' }) => {
  const getDensityClass = () => {
    switch (density) {
      case 'light': return 'particle-light';
      case 'heavy': return 'particle-heavy';
      default: return 'particle-medium';
    }
  };

  return (
    <div className={`particle-background ${getDensityClass()}`} 
         style={{ 
           position: 'absolute', 
           top: 0, 
           left: 0, 
           width: '100%', 
           height: '100%', 
           pointerEvents: 'none',
           zIndex: 0
         }} 
    />
  );
}; 