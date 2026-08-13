import React, { useState } from "react";

const ARTICLE_CONTENT = {
  "Setting Up Your Account":
    "To create an account, click 'Sign Up' on the homepage and enter your name, email, and a secure password. After signing up, verify your email address using the confirmation link we send you. Once verified, you can complete your profile and set your preferences in the Settings page.",
  "How to Reset Your Password":
    "If you forgot your password, go to the login page and click 'Forgot Password'. Enter the email address associated with your account. You will receive a password reset link valid for 30 minutes. Click the link and choose a new password. If you don't receive the email, check your spam folder or contact support.",
  "Two-Factor Authentication (2FA)":
    "Two-factor authentication adds a second verification step at login. To enable it, go to Security Settings and click 'Enable 2FA'. Scan the QR code with an authenticator app like Google Authenticator or Authy, then enter the 6-digit code to confirm. Save your backup codes somewhere safe in case you lose access to your device.",
  "Understanding Billing and Subscriptions":
    "Your subscription renews automatically at the start of each billing cycle. You can view past invoices under Billing History in your account settings. To upgrade or downgrade your plan, go to Billing > Change Plan. Changes take effect immediately, and charges are prorated for the current cycle.",
  "Troubleshooting Failed Payments":
    "If a payment fails, we will retry automatically over the next 3 days and notify you by email. Make sure your card details are up to date under Billing > Payment Methods. If all retries fail, your account may be downgraded to the free tier until payment is resolved.",
  "Generating an API Key":
    "API keys allow you to authenticate requests to our API. To generate one, go to Developer Settings and click 'New API Key'. Give it a name to identify its use, then copy the key immediately since it won't be shown again. You can revoke a key at any time from the same page.",
  "Inviting Team Members":
    "To invite a team member, go to Workspace Settings > Members and click 'Invite'. Enter their email address and choose a role: Admin, Editor, or Viewer. They will receive an email invitation with a link to join. Pending invitations can be resent or cancelled from the Members page.",
  "Exporting Your Data":
    "You can export your data at any time from Settings > Data Export. Choose CSV or JSON format, select the date range, and click 'Export'. Large exports are processed in the background and you'll receive a download link by email once ready. Exports are available for 7 days before the link expires.",
};

const ARTICLES = [
  {
    title: "Setting Up Your Account",
    description:
      "Create your account, verify your email, and configure your profile.",
    category: "Getting Started",
    author: "Onboarding Team",
  },
  {
    title: "How to Reset Your Password",
    description: "Steps to recover access when you've forgotten your password.",
    category: "Account",
    author: "Support Team",
  },
  {
    title: "Two-Factor Authentication (2FA)",
    description: "Add a second verification step to keep your account secure.",
    category: "Security",
    author: "Security Team",
  },
  {
    title: "Understanding Billing and Subscriptions",
    description: "How billing cycles, invoices, and plan changes work.",
    category: "Billing",
    author: "Billing Team",
  },
  {
    title: "Troubleshooting Failed Payments",
    description: "What happens when a payment fails, and how to fix it.",
    category: "Billing",
    author: "Billing Team",
  },
  {
    title: "Generating an API Key",
    description:
      "Create and manage API keys to authenticate your integrations.",
    category: "Developers",
    author: "Developer Relations",
  },
  {
    title: "Inviting Team Members",
    description: "Add collaborators to your workspace and manage their roles.",
    category: "Team",
    author: "Support Team",
  },
  {
    title: "Exporting Your Data",
    description:
      "Download your account data as CSV or JSON for backup or migration.",
    category: "Data",
    author: "Data Team",
  },
];

const CATEGORY_COLORS = {
  "Getting Started": "#4F46E5",
  Account: "#0EA5A5",
  Security: "#E0763B",
  Billing: "#B45309",
  Developers: "#6D28D9",
  Team: "#059669",
  Data: "#DB2777",
};

function DocsPage({ onAskAbout }) {
  const [openArticle, setOpenArticle] = useState(null);

  return (
    <div className="docs-page">
      <header className="docs-nav">
        <div className="docs-nav-brand">
          <span className="docs-nav-mark">◆</span> Nimbus Docs
        </div>
        <nav className="docs-nav-links">
          <span>Guides</span>
          <span>API Reference</span>
          <span>Changelog</span>
        </nav>
      </header>

      <section className="docs-hero">
        <p className="docs-hero-eyebrow">Documentation</p>
        <h1>Everything you need to run Nimbus.</h1>
        <p className="docs-hero-sub">
          Setup guides, security, billing, and API references — or ask the
          assistant in the corner and skip the reading.
        </p>
      </section>

      <section className="docs-grid">
        {ARTICLES.map((article) => (
          <article
            className="docs-card docs-card-clickable"
            key={article.title}
            style={{ borderLeftColor: CATEGORY_COLORS[article.category] }}
            onClick={() => setOpenArticle(article)}
          >
            <span
              className="docs-card-category"
              style={{ color: CATEGORY_COLORS[article.category] }}
            >
              {article.category}
            </span>
            <h3>{article.title}</h3>
            <p>{article.description}</p>
            <span className="docs-card-author">{article.author}</span>
          </article>
        ))}
      </section>

      <footer className="docs-footer">
        Nimbus Docs — internal documentation, always evolving.
      </footer>

      {openArticle && (
        <div
          className="docs-modal-backdrop"
          onClick={() => setOpenArticle(null)}
        >
          <div className="docs-modal" onClick={(e) => e.stopPropagation()}>
            <span
              className="docs-card-category"
              style={{ color: CATEGORY_COLORS[openArticle.category] }}
            >
              {openArticle.category}
            </span>
            <h2>{openArticle.title}</h2>
            <p className="docs-modal-body">
              {ARTICLE_CONTENT[openArticle.title]}
            </p>
            <span className="docs-card-author">{openArticle.author}</span>
            <div className="docs-modal-actions">
              <button
                className="docs-modal-ask"
                onClick={() => {
                  onAskAbout && onAskAbout(openArticle.title);
                  setOpenArticle(null);
                }}
              >
                Ask the assistant about this →
              </button>
              <button
                className="docs-modal-close"
                onClick={() => setOpenArticle(null)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DocsPage;
