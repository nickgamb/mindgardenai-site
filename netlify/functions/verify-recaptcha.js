const { RecaptchaEnterpriseServiceClient } = require('@google-cloud/recaptcha-enterprise');

async function createAssessment({
  projectID,
  recaptchaKey,
  token,
  recaptchaAction,
}) {
  const client = new RecaptchaEnterpriseServiceClient();
  const projectPath = client.projectPath(projectID);

  const request = {
    assessment: {
      event: {
        token: token,
        siteKey: recaptchaKey,
      },
    },
    parent: projectPath,
  };

  const [response] = await client.createAssessment(request);

  if (!response.tokenProperties.valid) {
    console.log(`The CreateAssessment call failed because the token was: ${response.tokenProperties.invalidReason}`);
    return null;
  }

  if (response.tokenProperties.action === recaptchaAction) {
    console.log(`The reCAPTCHA score is: ${response.riskAnalysis.score}`);
    response.riskAnalysis.reasons.forEach((reason) => {
      console.log(reason);
    });

    return response.riskAnalysis.score;
  } else {
    console.log("The action attribute in your reCAPTCHA tag does not match the action you are expecting to score");
    return null;
  }
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const { token, action } = JSON.parse(event.body);

  if (!token || !action) {
    return { statusCode: 400, body: "Missing token or action" };
  }

  try {
    const score = await createAssessment({
      projectID: process.env.GOOGLE_CLOUD_PROJECT_ID,
      recaptchaKey: process.env.RECAPTCHA_SITE_KEY,
      token: token,
      recaptchaAction: action,
    });

    if (score !== null) {
      return { 
        statusCode: 200, 
        body: JSON.stringify({ success: true, score: score }) 
      };
    } else {
      return { 
        statusCode: 200, 
        body: JSON.stringify({ success: false, message: "Invalid reCAPTCHA token or action mismatch" }) 
      };
    }
  } catch (error) {
    console.error('Error:', error);
    return { 
      statusCode: 500, 
      body: JSON.stringify({ success: false, message: "Error verifying reCAPTCHA" }) 
    };
  }
};
