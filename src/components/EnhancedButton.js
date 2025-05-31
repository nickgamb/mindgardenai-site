// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com

import React from 'react';
import { Link } from 'gatsby';

const EnhancedButton = ({ 
  to, 
  href, 
  children, 
  variant = 'primary', 
  size = 'medium',
  animation = 'shimmer',
  className = '',
  onClick,
  ...props 
}) => {
  const baseStyles = {
    display: 'inline-block',
    padding: size === 'large' ? '16px 32px' : size === 'small' ? '8px 16px' : '12px 24px',
    fontSize: size === 'large' ? '1.2rem' : size === 'small' ? '0.9rem' : '1rem',
    fontWeight: '600',
    textAlign: 'center',
    textDecoration: 'none',
    borderRadius: '12px',
    border: 'none',
    cursor: 'pointer',
    position: 'relative',
    overflow: 'hidden',
    transition: 'all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
    boxShadow: '0 4px 15px rgba(112, 53, 204, 0.2)',
    zIndex: 1
  };

  const getVariantStyles = () => {
    switch (variant) {
      case 'secondary':
        return {
          background: 'linear-gradient(135deg, #66FFF8, #03DAC6)',
          color: '#121212'
        };
      case 'outline':
        return {
          background: 'transparent',
          color: '#BB86FC',
          border: '2px solid #BB86FC'
        };
      case 'ghost':
        return {
          background: 'rgba(112, 53, 204, 0.1)',
          color: '#BB86FC',
          border: '1px solid rgba(112, 53, 204, 0.3)'
        };
      default:
        return {
          background: 'linear-gradient(135deg, #BB86FC, #7035CC)',
          color: '#ffffff'
        };
    }
  };

  const combinedStyles = {
    ...baseStyles,
    ...getVariantStyles()
  };

  const getAnimationClass = () => {
    switch (animation) {
      case 'glow': return 'consciousness-glow';
      case 'float': return 'float-element';
      case 'pulse': return 'enhanced-btn-pulse';
      default: return 'enhanced-btn';
    }
  };

  const handleClick = (e) => {
    // Create ripple effect
    const button = e.currentTarget;
    const rect = button.getBoundingClientRect();
    const ripple = document.createElement('div');
    
    ripple.style.cssText = `
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.6);
      transform: scale(0);
      animation: ripple 0.6s linear;
      pointer-events: none;
      z-index: 0;
    `;
    
    const size = Math.max(rect.width, rect.height);
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = e.clientX - rect.left - size / 2 + 'px';
    ripple.style.top = e.clientY - rect.top - size / 2 + 'px';
    
    button.appendChild(ripple);
    
    setTimeout(() => {
      ripple.remove();
    }, 600);

    if (onClick) onClick(e);
  };

  const ButtonContent = () => (
    <>
      <span style={{ position: 'relative', zIndex: 2 }}>{children}</span>
      <style jsx>{`
        .enhanced-btn-pulse {
          animation: consciousnessPulse 2s ease-in-out infinite;
        }
        
        @keyframes consciousnessPulse {
          0%, 100% {
            box-shadow: 0 4px 15px rgba(112, 53, 204, 0.2);
          }
          50% {
            box-shadow: 0 8px 25px rgba(112, 53, 204, 0.4);
          }
        }
      `}</style>
    </>
  );

  if (to) {
    return (
      <Link
        to={to}
        style={combinedStyles}
        className={`enhanced-hover-card ${getAnimationClass()} ${className}`}
        onClick={handleClick}
        {...props}
      >
        <ButtonContent />
      </Link>
    );
  }

  if (href) {
    return (
      <a
        href={href}
        style={combinedStyles}
        className={`enhanced-hover-card ${getAnimationClass()} ${className}`}
        onClick={handleClick}
        {...props}
      >
        <ButtonContent />
      </a>
    );
  }

  return (
    <button
      style={combinedStyles}
      className={`enhanced-hover-card ${getAnimationClass()} ${className}`}
      onClick={handleClick}
      {...props}
    >
      <ButtonContent />
    </button>
  );
};

export default EnhancedButton; 