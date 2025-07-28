// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md

import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

const ScreenshotCarousel = ({ screenshots, autoPlay = true, interval = 4000 }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (!autoPlay || screenshots.length <= 1) return;

    const timer = setInterval(() => {
      handleNext();
    }, interval);

    return () => clearInterval(timer);
  }, [currentIndex, autoPlay, interval, screenshots.length]);

  const handleNext = () => {
    if (isAnimating) return;
    setIsAnimating(true);
    setCurrentIndex((prev) => (prev + 1) % screenshots.length);
    setTimeout(() => setIsAnimating(false), 300);
  };

  const handlePrev = () => {
    if (isAnimating) return;
    setIsAnimating(true);
    setCurrentIndex((prev) => (prev - 1 + screenshots.length) % screenshots.length);
    setTimeout(() => setIsAnimating(false), 300);
  };

  const goToSlide = (index) => {
    if (isAnimating || index === currentIndex) return;
    setIsAnimating(true);
    setCurrentIndex(index);
    setTimeout(() => setIsAnimating(false), 300);
  };

  if (!screenshots || screenshots.length === 0) {
    return <div>No screenshots available</div>;
  }

  return (
    <div className="screenshot-carousel" style={{
      position: 'relative',
      width: '100%',
      maxWidth: '1200px',
      margin: '0 auto',
      borderRadius: '16px',
      overflow: 'hidden',
      boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
      background: 'linear-gradient(135deg, rgba(45, 45, 45, 0.9) 0%, rgba(30, 30, 30, 0.95) 100%)',
      border: '1px solid rgba(112, 53, 204, 0.2)'
    }}>
      {/* Main Image Display */}
      <div style={{
        position: 'relative',
        width: '100%',
        paddingTop: '56.25%', // 16:9 aspect ratio
        overflow: 'hidden'
      }}>
        <img
          src={screenshots[currentIndex].src}
          alt={screenshots[currentIndex].alt}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transition: 'transform 0.3s ease-in-out',
            transform: isAnimating ? 'scale(1.02)' : 'scale(1)'
          }}
        />
        
        {/* Overlay gradient for better text readability */}
        <div style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: '30%',
          background: 'linear-gradient(transparent, rgba(0, 0, 0, 0.7))',
          zIndex: 1
        }} />
        
        {/* Navigation arrows */}
        {screenshots.length > 1 && (
          <>
            <button
              onClick={handlePrev}
              style={{
                position: 'absolute',
                left: '20px',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'rgba(112, 53, 204, 0.8)',
                border: 'none',
                borderRadius: '50%',
                width: '50px',
                height: '50px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                color: 'white',
                fontSize: '20px',
                transition: 'all 0.3s ease',
                zIndex: 2,
                opacity: 0.8
              }}
              onMouseEnter={(e) => {
                e.target.style.opacity = '1';
                e.target.style.transform = 'translateY(-50%) scale(1.1)';
              }}
              onMouseLeave={(e) => {
                e.target.style.opacity = '0.8';
                e.target.style.transform = 'translateY(-50%) scale(1)';
              }}
            >
              ←
            </button>
            <button
              onClick={handleNext}
              style={{
                position: 'absolute',
                right: '20px',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'rgba(112, 53, 204, 0.8)',
                border: 'none',
                borderRadius: '50%',
                width: '50px',
                height: '50px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                color: 'white',
                fontSize: '20px',
                transition: 'all 0.3s ease',
                zIndex: 2,
                opacity: 0.8
              }}
              onMouseEnter={(e) => {
                e.target.style.opacity = '1';
                e.target.style.transform = 'translateY(-50%) scale(1.1)';
              }}
              onMouseLeave={(e) => {
                e.target.style.opacity = '0.8';
                e.target.style.transform = 'translateY(-50%) scale(1)';
              }}
            >
              →
            </button>
          </>
        )}
        
        {/* Caption */}
        {screenshots[currentIndex].caption && (
          <div style={{
            position: 'absolute',
            bottom: '20px',
            left: '20px',
            right: '20px',
            color: 'white',
            fontSize: '1.1rem',
            fontWeight: '500',
            textShadow: '0 2px 4px rgba(0, 0, 0, 0.8)',
            zIndex: 2
          }}>
            {screenshots[currentIndex].caption}
          </div>
        )}
      </div>

      {/* Dot indicators */}
      {screenshots.length > 1 && (
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '12px',
          padding: '20px',
          background: 'rgba(20, 20, 20, 0.9)'
        }}>
          {screenshots.map((_, index) => (
            <button
              key={index}
              onClick={() => goToSlide(index)}
              style={{
                width: '12px',
                height: '12px',
                borderRadius: '50%',
                border: 'none',
                background: index === currentIndex 
                  ? '#BB86FC' 
                  : 'rgba(255, 255, 255, 0.3)',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                transform: index === currentIndex ? 'scale(1.2)' : 'scale(1)'
              }}
              onMouseEnter={(e) => {
                if (index !== currentIndex) {
                  e.target.style.background = 'rgba(255, 255, 255, 0.5)';
                }
              }}
              onMouseLeave={(e) => {
                if (index !== currentIndex) {
                  e.target.style.background = 'rgba(255, 255, 255, 0.3)';
                }
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
};

ScreenshotCarousel.propTypes = {
  screenshots: PropTypes.arrayOf(
    PropTypes.shape({
      src: PropTypes.string.isRequired,
      alt: PropTypes.string.isRequired,
      caption: PropTypes.string
    })
  ).isRequired,
  autoPlay: PropTypes.bool,
  interval: PropTypes.number
};

export default ScreenshotCarousel; 