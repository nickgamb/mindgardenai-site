export default async (request, context) => {
  // Only allow GET requests
  if (request.method !== 'GET') {
    return new Response('Method not allowed', { status: 405 });
  }

  // Get the signal data from the Netlify function
  const response = await fetch('/.netlify/functions/poll-openai');
  const signalData = await response.json();

  // Return the signal data with appropriate headers
  return new Response(JSON.stringify(signalData), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}; 