"""
seed_documents.py

Loads realistic product-documentation content into MongoDB so the
Doc Assistant app has real data to search over, instead of the old
placeholder test sentences.

Run this once (or whenever you want to reset the data):
    python seed_documents.py
"""

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["doc_assistant"]
collection = db["documents"]

documents = [
    {
        "title": "How to Reset Your Password",
        "description": "Steps to reset a forgotten account password.",
        "content": (
            "If you forgot your password, go to the login page and click "
            "'Forgot Password'. Enter the email address associated with your "
            "account. You will receive a password reset link valid for 30 "
            "minutes. Click the link and choose a new password. If you don't "
            "receive the email, check your spam folder or contact support."
        ),
        "author": "Support Team",
        "tags": ["account", "password", "login"]
    },
    {
        "title": "Setting Up Your Account",
        "description": "Guide to creating and configuring a new account.",
        "content": (
            "To create an account, click 'Sign Up' on the homepage and enter "
            "your name, email, and a secure password. After signing up, verify "
            "your email address using the confirmation link we send you. Once "
            "verified, you can complete your profile and set your preferences "
            "in the Settings page."
        ),
        "author": "Onboarding Team",
        "tags": ["account", "setup", "onboarding"]
    },
    {
        "title": "Understanding Billing and Subscriptions",
        "description": "How billing cycles, invoices, and plan changes work.",
        "content": (
            "Your subscription renews automatically at the start of each "
            "billing cycle. You can view past invoices under Billing History "
            "in your account settings. To upgrade or downgrade your plan, go "
            "to Billing > Change Plan. Changes take effect immediately, and "
            "charges are prorated for the current cycle."
        ),
        "author": "Billing Team",
        "tags": ["billing", "subscription", "payments"]
    },
    {
        "title": "Generating an API Key",
        "description": "How to create and manage API keys for integrations.",
        "content": (
            "API keys allow you to authenticate requests to our API. To "
            "generate one, go to Developer Settings and click 'New API Key'. "
            "Give it a name to identify its use, then copy the key immediately "
            "since it won't be shown again. You can revoke a key at any time "
            "from the same page."
        ),
        "author": "Developer Relations",
        "tags": ["api", "developer", "integration"]
    },
    {
        "title": "Inviting Team Members",
        "description": "How to add collaborators to your workspace.",
        "content": (
            "To invite a team member, go to Workspace Settings > Members and "
            "click 'Invite'. Enter their email address and choose a role: "
            "Admin, Editor, or Viewer. They will receive an email invitation "
            "with a link to join. Pending invitations can be resent or "
            "cancelled from the Members page."
        ),
        "author": "Support Team",
        "tags": ["team", "collaboration", "permissions"]
    },
    {
        "title": "Exporting Your Data",
        "description": "How to export account data for backup or migration.",
        "content": (
            "You can export your data at any time from Settings > Data Export. "
            "Choose CSV or JSON format, select the date range, and click "
            "'Export'. Large exports are processed in the background and "
            "you'll receive a download link by email once ready. Exports "
            "are available for 7 days before the link expires."
        ),
        "author": "Data Team",
        "tags": ["data", "export", "backup"]
    },
    {
        "title": "Two-Factor Authentication (2FA)",
        "description": "How to enable extra login security on your account.",
        "content": (
            "Two-factor authentication adds a second verification step at "
            "login. To enable it, go to Security Settings and click 'Enable "
            "2FA'. Scan the QR code with an authenticator app like Google "
            "Authenticator or Authy, then enter the 6-digit code to confirm. "
            "Save your backup codes somewhere safe in case you lose access "
            "to your device."
        ),
        "author": "Security Team",
        "tags": ["security", "2fa", "login"]
    },
    {
        "title": "Troubleshooting Failed Payments",
        "description": "What to do if a subscription payment fails.",
        "content": (
            "If a payment fails, we will retry automatically over the next "
            "3 days and notify you by email. Make sure your card details are "
            "up to date under Billing > Payment Methods. If all retries fail, "
            "your account may be downgraded to the free tier until payment "
            "is resolved."
        ),
        "author": "Billing Team",
        "tags": ["billing", "payments", "troubleshooting"]
    }
]

def seed():
    existing_count = collection.count_documents({})
    print(f"Current documents in collection: {existing_count}")

    # Clear out old placeholder/test data first
    collection.delete_many({})
    print("Cleared existing documents.")

    result = collection.insert_many(documents)
    print(f"Inserted {len(result.inserted_ids)} documents.")

if __name__ == "__main__":
    seed()
