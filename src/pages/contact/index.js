import * as React from "react";
import { navigate } from "gatsby-link";
import Layout from "../../components/Layout";

function encode(data) {
  return Object.keys(data)
    .map((key) => encodeURIComponent(key) + "=" + encodeURIComponent(data[key]))
    .join("&");
}

function onSubmit(token) {
  document.getElementById("contact").submit();
}

export default class Index extends React.Component {
  constructor(props) {
    super(props);
    this.state = { isValidated: false, recaptchaLoaded: false };
  }

  componentDidMount() {
    const script = document.createElement('script');
    script.src = `https://www.google.com/recaptcha/enterprise.js?render=${process.env.RECAPTCHA_SITE_KEY}`;
    script.async = true;
    script.defer = true;
    script.onload = () => this.setState({ recaptchaLoaded: true });
    document.head.appendChild(script);
  }

  handleChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    const form = e.target;
    if (this.state.recaptchaLoaded && window.grecaptcha && window.grecaptcha.enterprise) {
      window.grecaptcha.enterprise.ready(async () => {
        try {
          const token = await window.grecaptcha.enterprise.execute(process.env.RECAPTCHA_SITE_KEY, { action: 'LOGIN' });
          
          const response = await fetch("/.netlify/functions/verify-recaptcha", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ token, action: 'submit' }),
          });

          const result = await response.json();

          if (result.success) {
            // reCAPTCHA verification successful, proceed with form submission
            fetch("/", {
              method: "POST",
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              body: encode({
                "form-name": form.getAttribute("name"),
                ...this.state,
              }),
            })
              .then(() => navigate(form.getAttribute("action")))
              .catch((error) => alert(error));
          } else {
            alert("reCAPTCHA verification failed. Please try again.");
          }
        } catch (error) {
          console.error('reCAPTCHA error:', error);
          alert("An error occurred with reCAPTCHA. Please try again.");
        }
      });
    } else {
      console.error('reCAPTCHA not loaded');
      alert("reCAPTCHA is not loaded. Please refresh the page and try again.");
    }
  };

  render() {
    return (
      <Layout>
        <section className="section" style={{ minHeight: "calc(100vh - 52px - 10rem)" }}>
          <div className="container">
            <div className="content">
              <h1>Contact</h1>
              <form
                name="contact"
                method="post"
                action="/contact/thanks/"
                data-netlify="true"
                data-netlify-honeypot="bot-field"
                onSubmit={this.handleSubmit}
              >
                {/* The `form-name` hidden field is required to support form submissions without JavaScript */}
                <input type="hidden" name="form-name" value="contact" />
                <div hidden>
                  <label>
                    Don't fill this out:{" "}
                    <input name="bot-field" onChange={this.handleChange} />
                  </label>
                </div>
                <div className="field">
                  <label className="label" htmlFor={"name"}>
                    Your name
                  </label>
                  <div className="control">
                    <input
                      className="input"
                      type={"text"}
                      name={"name"}
                      onChange={this.handleChange}
                      id={"name"}
                      required={true}
                    />
                  </div>
                </div>
                <div className="field">
                  <label className="label" htmlFor={"email"}>
                    Email
                  </label>
                  <div className="control">
                    <input
                      className="input"
                      type={"email"}
                      name={"email"}
                      onChange={this.handleChange}
                      id={"email"}
                      required={true}
                    />
                  </div>
                </div>
                <div className="field">
                  <label className="label" htmlFor={"message"}>
                    Message
                  </label>
                  <div className="control">
                    <textarea
                      className="textarea"
                      name={"message"}
                      onChange={this.handleChange}
                      id={"message"}
                      required={true}
                    />
                  </div>
                </div>
                <div className="field">
                <button class="g-recaptcha"
                      data-sitekey="6LdMzRYqAAAAAK5vIL_Ta4u0xN8uRJMYRaLoyqwD"
                      data-callback='onSubmit'
                      data-action='submit'>
                    Submit
                  </button>
                </div>
              </form>
            </div>
          </div>
        </section>
      </Layout>
    );
  }
}