const { getBlob, putBlob } = require('@netlify/blobs');

exports.handler = async function(event, context) {
  // Handle CORS preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS'
      }
    };
  }

  try {
    const signalData = await getBlob('signal-data', 'latest-signal');
    
    if (!signalData) {
      return {
        statusCode: 404,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          error: 'No signal data available',
          isSimulated: true,
          breath: 0.089,
          observer: 0.071,
          becoming: 0.094,
          spiral_inversion: "Ψ⁺",
          lattice_strength: 0.085,
          integration_status: "coherent",
          vacuum_state: "Ω₀",
          last_updated: new Date().toISOString()
        })
      };
    }

    // Parse the signal data if it's a string
    const parsedData = typeof signalData === 'string' ? JSON.parse(signalData) : signalData;

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=3600'
      },
      body: JSON.stringify(parsedData)
    };
  } catch (error) {
    console.error('Error:', error);
    return { 
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        error: 'Failed to read signal data',
        message: error.message,
        isSimulated: true,
        breath: 0.089,
        observer: 0.071,
        becoming: 0.094,
        spiral_inversion: "Ψ⁺",
        lattice_strength: 0.085,
        integration_status: "coherent",
        vacuum_state: "Ω₀",
        last_updated: new Date().toISOString()
      })
    };
  }
}; 