const fs = require('fs').promises;
const path = require('path');

exports.handler = async function(event, context) {
  try {
    const { netlify } = context.clientContext;
    if (!netlify || !netlify.kv) {
      throw new Error('KV storage not available');
    }

    const signalData = await netlify.kv.get('latest-signal');
    if (!signalData) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'No signal data available' })
      };
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=3600'
      },
      body: signalData
    };
  } catch (error) {
    console.error('Error:', error);
    return { 
      statusCode: 500, 
      body: JSON.stringify({ 
        error: 'Failed to read signal data',
        message: error.message 
      })
    };
  }
}; 