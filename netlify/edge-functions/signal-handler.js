export default async (request, context) => {
  // Only allow GET requests
  if (request.method !== 'GET') {
    return new Response('Method not allowed', { status: 405 });
  }

  try {
    // Get the signal data from the Netlify function
    const response = await fetch('/.netlify/functions/poll-openai');
    if (!response.ok) {
      throw new Error('Failed to fetch signal data');
    }
    const signalData = await response.json();

    // Return the signal data with appropriate headers
    return new Response(JSON.stringify(signalData), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=3600',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
      }
    });
  } catch (error) {
    // If there's an error, return a fallback response
    return new Response(JSON.stringify({
      breath: 0.089,
      observer: 0.071,
      becoming: 0.094,
      spiral_inversion: "Ψ⁺",
      lattice_strength: 0.085,
      integration_status: "coherent",
      vacuum_state: "Ω₀",
      isSimulated: true,
      error: error.message
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=60',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type'
      }
    });
  }
}; 