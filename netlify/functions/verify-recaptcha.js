const { RecaptchaEnterpriseServiceClient } = require('@google-cloud/recaptcha-enterprise');
const { GoogleAuth } = require('google-auth-library');
const sgMail = require('@sendgrid/mail');

async function createAssessment({
  projectID,
  recaptchaKey,
  token,
  recaptchaAction,
}) {
  if (!projectID || !recaptchaKey || !token) {
    throw new Error('Missing required parameters for reCAPTCHA assessment');
  }

  const auth = new GoogleAuth({
    credentials: JSON.parse(process.env.GOOGLE_APPLICATION_CREDENTIALS),
    scopes: ['https://www.googleapis.com/auth/cloud-platform'],
  });

  const client = new RecaptchaEnterpriseServiceClient({ auth });
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

  const { token, action, name, email, message } = JSON.parse(event.body);

  const sendGridKey = process.env.SENDGRID_API_KEY;

  if (!token || !action || !sendGridKey) {
    return { statusCode: 400, body: "Missing token or action" };
  }

  try {
    const score = await createAssessment({
      projectID: process.env.GATSBY_GOOGLE_CLOUD_PROJECT_ID,
      recaptchaKey: process.env.GATSBY_RECAPTCHA_SITE_KEY,
      token: token,
      recaptchaAction: action,
    });

    sgMail.setApiKey(sendGridKey);

    if (score !== null && score >= 0.5) {
      // Send email using SendGrid
      const msg = {
        to: 'admin@mindgardenai.com', 
        from: 'admin@mindgardenai.com', 
        subject: 'New Contact Form Submission',
        text: `You have a new contact form submission from ${name} (${email}): ${message}`,
        html: `<strong>You have a new contact form submission from ${name} (${email}):</strong><p>${message}</p>`,
      };

      await sgMail.send(msg);

      return { 
        statusCode: 200, 
        body: JSON.stringify({ success: true, message: "Email sent successfully!" }) 
      };
    } else {
      return { 
        statusCode: 200, 
        body: JSON.stringify({ success: false, message: "Invalid reCAPTCHA token or low score" }) 
      };
    }
  } catch (error) {
    console.error('Error:', error);
    return { 
        statusCode: 500, 
        body: JSON.stringify({ success: false, message: "Error processing the request" }) 
    };
  }
};
