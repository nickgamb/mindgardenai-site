const { createClient } = require('@netlify/blobs');

exports.handler = async function(event, context) {
  try {
    const blobs = createClient();
    const signalData = await blobs.get('signal-data', 'latest-signal');
    
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