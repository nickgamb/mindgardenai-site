const fs = require('fs').promises;
const path = require('path');

exports.handler = async function(event, context) {
  try {
    const publicDir = path.join(process.cwd(), 'public');
    const signalData = await fs.readFile(
      path.join(publicDir, 'latest-signal.json'),
      'utf8'
    );

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