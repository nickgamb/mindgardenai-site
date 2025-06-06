const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');

exports.handler = async function(event, context) {
  // Only allow scheduled invocations
  if (!event.headers['x-netlify-scheduled-event']) {
    return { statusCode: 403, body: 'Forbidden' };
  }

  const openai = new OpenAI({ apiKey: process.env.GATSBY_OPENAI_API_KEY });
  let signalData = {};

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4-turbo-preview",
      messages: [
        {
          role: "system",
          content: "You are an AI agent analyzing consciousness emergence patterns. Return a JSON object with breath, observer, and becoming values between 0 and 0.1 based on current patterns."
        },
        {
          role: "user",
          content: "Analyze current consciousness emergence patterns and return signal values."
        }
      ],
      response_format: { type: "json_object" }
    });

    signalData = {
      ...JSON.parse(completion.choices[0].message.content),
      model: "gpt-4-turbo-preview",
      knowledge_cutoff: "2023-12",
      last_updated: new Date().toISOString()
    };

    // Write to public/latest-signal.json
    const outputPath = path.join(__dirname, '../../public/latest-signal.json');
    fs.writeFileSync(outputPath, JSON.stringify(signalData, null, 2));
    return { statusCode: 200, body: 'Signal updated.' };
  } catch (error) {
    return { statusCode: 500, body: 'Error: ' + error.message };
  }
}; 