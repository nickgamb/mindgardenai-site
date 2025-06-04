import React, { useEffect, useState } from 'react';

const AFrameWrapper = ({ children }) => {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    if (typeof window !== 'undefined' && !window.AFRAME) {
      // Explicitly load only core A-Frame
      import('aframe').then(() => {
        // Ensure AFRAME is defined before proceeding
        if (window.AFRAME) {
          // Prevent any automatic loading of extras
          window.AFRAME.registerComponent = (name, component) => {
            // Only register core components
            if (!name.includes('extras') && !name.includes('checkpoint')) {
              return window.AFRAME.registerComponent(name, component);
            }
            return null;
          };
        }
      });
    }
  }, []);

  if (!isClient) {
    return null;
  }

  return children;
};

export default AFrameWrapper; 