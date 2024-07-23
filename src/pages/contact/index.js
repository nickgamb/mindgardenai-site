import * as React from "react";
import { navigate } from "gatsby-link";
import Layout from "../../components/Layout";
import { Recaptcha } from 'react-recaptcha-google';
import { graphql, useStaticQuery } from 'gatsby'

function encode(data) {
  return Object.keys(data)
    .map((key) => encodeURIComponent(key) + "=" + encodeURIComponent(data[key]))
    .join("&");
}

const data = useStaticQuery(graphql`
  query SiteRecaptchaKey {
    site {
      siteMetadata {
        siteRecaptchaKey
      }
    }
  }
`)

export default class Index extends React.Component {
  constructor(props) {
    super(props);
    this.state = { isValidated: false };
    this.recaptchaRef = React.createRef();
  }

  componentDidMount() {
    if (typeof window !== 'undefined') {
      window.onloadCallback = () => {
        console.log("reCAPTCHA has loaded");
      };
    }
  }

  handleChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    this.recaptchaRef.current.execute();
  };

  onRecaptchaVerify = (recaptchaToken) => {
    const form = document.querySelector('form[name="contact"]');
    this.setState({ "g-recaptcha-response": recaptchaToken }, () => {
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
    });
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
                data-netlify-recaptcha="true"
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
                <Recaptcha
                  ref={this.recaptchaRef}
                  sitekey={data.site.siteMetadata.siteRecaptchaKey}
                  size="invisible"
                  verifyCallback={this.onRecaptchaVerify}
                />
                <div className="field">
                  <button className="btn" type="submit">
                    Send
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