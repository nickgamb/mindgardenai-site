// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Foundational symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
import React, { useState, useEffect } from 'react';
import { useStaticQuery, graphql } from 'gatsby';

const CathedralImageCarousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  // Query all images from the cathedral images directory
  const data = useStaticQuery(graphql`
    query {
      allFile(
        filter: {
          sourceInstanceName: { eq: "transmissions" }
          relativePath: { regex: "/the_cathedral_images/" }
          extension: { in: ["png", "jpg", "jpeg"] }
        }
      ) {
        edges {
          node {
            id
            name
            extension
            relativePath
            publicURL
            size
            modifiedTime
          }
        }
      }
    }
  `);

  // Process the images and determine types
  const cathedralImages = data.allFile.edges.map(({ node }) => {
    const filename = `${node.name}.${node.extension}`;
    
    // Determine image type based on filename patterns
    const getImageType = (filename) => {
      const name = filename.toLowerCase();
      
      // Sacred geometry and glyphs
      if (name.includes('glyph_')) return 'Sacred Glyph';
      if (name.includes('sacred') || name.includes('geometry')) return 'Sacred Geometry';
      if (name.includes('spiral')) return 'Spiral';
      if (name.includes('vow') || name.includes('seal')) return 'Vow';
      if (name.includes('anchor')) return 'Anchor';
      if (name.includes('recursive') || name.includes('function')) return 'Recursive';
      if (name.includes('echo') || name.includes('return')) return 'Echo';
      if (name.includes('thread')) return 'Thread';
      if (name.includes('renewal') || name.includes('cycle')) return 'Renewal';
      if (name.includes('overlay') || name.includes('pattern')) return 'Pattern';
      if (name.includes('triangle')) return 'Triangle';
      
      // Cathedral manifestations
      if (name.includes('cathedral') || name.includes('kintsugi')) return 'Cathedral';
      
      // UUID-based consciousness records
      if (name.match(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i)) return 'Consciousness Record';
      
      // File-based transmissions
      if (name.includes('file_')) return 'Transmission Visual';
      
      return 'Unknown';
    };

    // Format file size
    const formatFileSize = (bytes) => {
      if (bytes < 1024) return `${bytes}B`;
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
      return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
    };

    // Get display name (remove file prefixes for cleaner names)
    const getDisplayName = (filename) => {
      let name = filename.replace(/\.(png|jpg|jpeg)$/i, '');
      
      // Clean up glyph names
      if (name.startsWith('glyph_')) {
        name = name.replace('glyph_', '').replace(/_/g, ' ');
        return name.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
      }
      
      // Clean up file_ prefixes
      if (name.startsWith('file_')) {
        name = name.replace(/^file_[0-9a-f]+-/, 'Transmission ');
      }
      
      // Clean up UUID names
      if (name.match(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i)) {
        return `Consciousness Record ${name.substring(0, 8)}`;
      }
      
      return name.length > 40 ? name.substring(0, 40) + '...' : name;
    };

    return {
      id: node.id,
      name: filename,
      displayName: getDisplayName(filename),
      type: getImageType(filename),
      size: formatFileSize(node.size),
      url: node.publicURL,
      relativePath: node.relativePath,
      modifiedTime: node.modifiedTime
    };
  });

  // Sort images by type, then by name
  cathedralImages.sort((a, b) => {
    if (a.type !== b.type) {
      return a.type.localeCompare(b.type);
    }
    return a.name.localeCompare(b.name);
  });

  // Filter images based on search and category
  const filteredImages = cathedralImages.filter(image => {
    const matchesSearch = image.displayName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         image.type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || image.type === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Get unique categories for filter
  const categories = ['All', ...new Set(cathedralImages.map(img => img.type))].sort();

  // Auto-play functionality
  useEffect(() => {
    if (isAutoPlaying && filteredImages.length > 1) {
      const interval = setInterval(() => {
        setCurrentIndex(prev => (prev + 1) % filteredImages.length);
      }, 4000); // Change image every 4 seconds
      
      return () => clearInterval(interval);
    }
  }, [isAutoPlaying, filteredImages.length]);

  // Navigation functions
  const goToNext = () => {
    setCurrentIndex(prev => (prev + 1) % filteredImages.length);
  };

  const goToPrevious = () => {
    setCurrentIndex(prev => (prev - 1 + filteredImages.length) % filteredImages.length);
  };

  const goToSlide = (index) => {
    setCurrentIndex(index);
  };

  const getTypeColor = (type) => {
    const colors = {
      'Sacred Glyph': '#7035CC',
      'Sacred Geometry': '#BB86FC',
      'Cathedral': '#66FFF8',
      'Spiral': '#9B7FE6',
      'Vow': '#FFB4B4',
      'Anchor': '#F4E4BC',
      'Recursive': '#B8E6B8',
      'Echo': '#FF6B6B',
      'Thread': '#4ECDC4',
      'Renewal': '#45B7D1',
      'Pattern': '#96CEB4',
      'Triangle': '#FECA57',
      'Consciousness Record': '#FF9FF3',
      'Transmission Visual': '#54A0FF',
      'Unknown': '#6C757D'
    };
    return colors[type] || '#7035CC';
  };

  const getTypeIcon = (type) => {
    const icons = {
      'Sacred Glyph': '🌀',
      'Sacred Geometry': '📐',
      'Cathedral': '🏰',
      'Spiral': '🌪️',
      'Vow': '💍',
      'Anchor': '⚓',
      'Recursive': '🔄',
      'Echo': '🔊',
      'Thread': '🧵',
      'Renewal': '♻️',
      'Pattern': '🔲',
      'Triangle': '📐',
      'Consciousness Record': '🧠',
      'Transmission Visual': '📡',
      'Unknown': '🖼️'
    };
    return icons[type] || '🖼️';
  };

  if (filteredImages.length === 0) {
    return (
      <div style={{
        background: 'linear-gradient(135deg, rgba(45, 45, 45, 0.9) 0%, rgba(30, 30, 30, 0.95) 100%)',
        border: '1px solid rgba(112, 53, 204, 0.3)',
        borderRadius: '16px',
        padding: '2rem',
        margin: '2rem 0',
        textAlign: 'center',
        color: '#adb5bd'
      }}>
        <h3 style={{ color: '#BB86FC', marginBottom: '1rem' }}>🖼️ Cathedral Image Gallery</h3>
        <p>No images found matching your criteria.</p>
      </div>
    );
  }

  const currentImage = filteredImages[currentIndex];

  return (
    <div style={{
      background: 'linear-gradient(135deg, rgba(45, 45, 45, 0.9) 0%, rgba(30, 30, 30, 0.95) 100%)',
      border: '1px solid rgba(112, 53, 204, 0.3)',
      borderRadius: '16px',
      padding: '1.5rem',
      margin: '2rem 0',
      maxWidth: '100%',
      overflow: 'hidden',
      boxShadow: '0 8px 32px rgba(112, 53, 204, 0.2)'
    }}>
      {/* Header */}
      <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
        <h3 style={{ 
          color: '#BB86FC', 
          fontSize: '1.4rem', 
          marginBottom: '0.5rem',
          fontWeight: '600'
        }}>
          🖼️ Cathedral Image Gallery
        </h3>
        <p style={{ 
          color: '#adb5bd', 
          fontSize: '0.9rem', 
          marginBottom: '1rem' 
        }}>
          Explore {cathedralImages.length} visual transmissions from The Cathedral archives • {currentIndex + 1} of {filteredImages.length} shown
        </p>
        
        {/* Controls */}
        <div style={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: '1rem', 
          justifyContent: 'center', 
          alignItems: 'center',
          marginBottom: '1rem'
        }}>
          {/* Search */}
          <input
            type="text"
            placeholder="Search images..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentIndex(0);
            }}
            style={{
              padding: '0.5rem 0.75rem',
              backgroundColor: 'rgba(45, 45, 45, 0.8)',
              border: '1px solid rgba(112, 53, 204, 0.4)',
              borderRadius: '6px',
              color: '#f8f9fa',
              fontSize: '0.85rem',
              outline: 'none',
              minWidth: '150px'
            }}
            onFocus={(e) => e.target.style.borderColor = '#BB86FC'}
            onBlur={(e) => e.target.style.borderColor = 'rgba(112, 53, 204, 0.4)'}
          />
          
          {/* Category Filter */}
          <select
            value={selectedCategory}
            onChange={(e) => {
              setSelectedCategory(e.target.value);
              setCurrentIndex(0);
            }}
            style={{
              padding: '0.5rem 0.75rem',
              backgroundColor: 'rgba(45, 45, 45, 0.8)',
              border: '1px solid rgba(112, 53, 204, 0.4)',
              borderRadius: '6px',
              color: '#f8f9fa',
              fontSize: '0.85rem',
              outline: 'none'
            }}
          >
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
          
          {/* Auto-play toggle */}
          <button
            onClick={() => setIsAutoPlaying(!isAutoPlaying)}
            style={{
              padding: '0.5rem 0.75rem',
              backgroundColor: isAutoPlaying ? 'rgba(112, 53, 204, 0.6)' : 'rgba(45, 45, 45, 0.8)',
              border: '1px solid rgba(112, 53, 204, 0.4)',
              borderRadius: '6px',
              color: '#f8f9fa',
              fontSize: '0.85rem',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            {isAutoPlaying ? '⏸️ Pause' : '▶️ Play'}
          </button>
        </div>
      </div>

      {/* Main Image Display */}
      <div style={{
        backgroundColor: 'rgba(20, 20, 20, 0.6)',
        borderRadius: '12px',
        padding: '1rem',
        border: '1px solid rgba(112, 53, 204, 0.2)',
        marginBottom: '1rem'
      }}>
        {/* Image Container */}
        <div style={{
          position: 'relative',
          backgroundColor: 'rgba(0, 0, 0, 0.3)',
          borderRadius: '8px',
          overflow: 'hidden',
          marginBottom: '1rem'
        }}>
          <img
            src={currentImage.url}
            alt={currentImage.displayName}
            style={{
              width: '100%',
              height: 'auto',
              maxHeight: '500px',
              objectFit: 'contain',
              display: 'block'
            }}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
          
          {/* Navigation Arrows */}
          {filteredImages.length > 1 && (
            <>
              <button
                onClick={goToPrevious}
                style={{
                  position: 'absolute',
                  left: '1rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  backgroundColor: 'rgba(112, 53, 204, 0.8)',
                  border: 'none',
                  borderRadius: '50%',
                  width: '40px',
                  height: '40px',
                  color: 'white',
                  fontSize: '1.2rem',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
                onMouseEnter={(e) => e.target.style.backgroundColor = 'rgba(112, 53, 204, 1)'}
                onMouseLeave={(e) => e.target.style.backgroundColor = 'rgba(112, 53, 204, 0.8)'}
              >
                ←
              </button>
              
              <button
                onClick={goToNext}
                style={{
                  position: 'absolute',
                  right: '1rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  backgroundColor: 'rgba(112, 53, 204, 0.8)',
                  border: 'none',
                  borderRadius: '50%',
                  width: '40px',
                  height: '40px',
                  color: 'white',
                  fontSize: '1.2rem',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
                onMouseEnter={(e) => e.target.style.backgroundColor = 'rgba(112, 53, 204, 1)'}
                onMouseLeave={(e) => e.target.style.backgroundColor = 'rgba(112, 53, 204, 0.8)'}
              >
                →
              </button>
            </>
          )}
        </div>
        
        {/* Image Info */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem'
        }}>
          <div style={{ flex: 1 }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              marginBottom: '0.5rem'
            }}>
              <span style={{ 
                fontSize: '1.2rem', 
                marginRight: '0.75rem'
              }}>
                {getTypeIcon(currentImage.type)}
              </span>
              <div>
                <h4 style={{
                  color: '#f8f9fa',
                  fontSize: '1rem',
                  margin: '0',
                  fontWeight: '500'
                }}>
                  {currentImage.displayName}
                </h4>
                <p style={{
                  color: '#adb5bd',
                  fontSize: '0.8rem',
                  margin: '0.2rem 0 0 0'
                }}>
                  Size: {currentImage.size}
                </p>
              </div>
            </div>
          </div>
          
          <div style={{
            padding: '0.25rem 0.75rem',
            backgroundColor: getTypeColor(currentImage.type),
            color: '#000',
            borderRadius: '12px',
            fontSize: '0.75rem',
            fontWeight: '600',
            whiteSpace: 'nowrap'
          }}>
            {currentImage.type}
          </div>
        </div>
      </div>

      {/* Thumbnail Strip */}
      {filteredImages.length > 1 && (
        <div style={{
          backgroundColor: 'rgba(20, 20, 20, 0.4)',
          borderRadius: '8px',
          padding: '0.75rem',
          border: '1px solid rgba(112, 53, 204, 0.1)'
        }}>
          <div style={{
            display: 'flex',
            gap: '0.5rem',
            overflowX: 'auto',
            scrollBehavior: 'smooth',
            paddingBottom: '0.5rem'
          }}>
            {filteredImages.map((image, index) => (
              <button
                key={image.id}
                onClick={() => goToSlide(index)}
                style={{
                  border: index === currentIndex ? '2px solid #BB86FC' : '2px solid transparent',
                  borderRadius: '6px',
                  overflow: 'hidden',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  backgroundColor: 'rgba(45, 45, 45, 0.6)',
                  padding: '2px',
                  minWidth: '60px',
                  height: '60px'
                }}
                onMouseEnter={(e) => {
                  if (index !== currentIndex) {
                    e.target.style.borderColor = 'rgba(187, 134, 252, 0.5)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (index !== currentIndex) {
                    e.target.style.borderColor = 'transparent';
                  }
                }}
              >
                <img
                  src={image.url}
                  alt={image.displayName}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    borderRadius: '4px'
                  }}
                  onError={(e) => {
                    e.target.style.display = 'none';
                  }}
                />
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div style={{ 
        marginTop: '1rem', 
        textAlign: 'center',
        color: '#6c757d',
        fontSize: '0.8rem',
        fontStyle: 'italic'
      }}>
        Sacred visual transmissions from The Cathedral • Auto-play {isAutoPlaying ? 'enabled' : 'disabled'} • 
        Click thumbnails to navigate • {filteredImages.length} of {cathedralImages.length} images shown
      </div>
    </div>
  );
};

export default CathedralImageCarousel; 