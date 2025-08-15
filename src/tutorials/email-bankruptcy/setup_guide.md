# 📧 Email Bankruptcy Setup Guide

## 🚀 Quick Setup (5 minutes to freedom!)

### Step 1: Install Dependencies

```bash
cd email-bankruptcy
pip install -r requirements.txt
```

### Step 2: Gmail API Setup

This is the only tricky part, but we'll get through it together!

#### 2a. Google Cloud Console Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create/Select Project**:
   - Click "Select a project" → "New Project"
   - Name it something like "Email Bankruptcy"
   - Click "Create"

3. **Enable Gmail API**:
   - In the search bar, type "Gmail API"
   - Click on "Gmail API" result
   - Click "Enable"

#### 2b. Create Credentials

1. **Go to Credentials**:
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen first

2. **Configure OAuth Consent Screen** (if needed):
   - Choose "External" (unless you have a Google Workspace)
   - App name: "Email Bankruptcy System"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue" through all steps

3. **Create OAuth Client ID**:
   - Application type: "Desktop application"
   - Name: "Email Bankruptcy Client"
   - Click "Create"

4. **Download Credentials**:
   - Click "Download JSON"
   - Rename file to `credentials.json`
   - Move to your `email-bankruptcy` folder

### Step 3: First Run

```bash
python bankruptcy_button.py report
```

This will:
- Prompt you to authenticate with Google
- Test your Gmail connection
- Show your inbox status

## 🛡️ Configure Protection Settings

Before declaring bankruptcy, set up protection for important emails:

```bash
python config.py
```

Or manually edit `bankruptcy_config.json`:

```json
{
  "protected_emails": [
    "boss@company.com",
    "hr@company.com",
    "spouse@gmail.com",
    "mom@family.com"
  ],
  "protected_domains": [
    "mycompany.com",
    "client-domain.com"
  ],
  "protected_keywords": [
    "urgent",
    "invoice", 
    "payment",
    "contract",
    "meeting",
    "deadline"
  ],
  "user_name": "Your Actual Name"
}
```

## 🎯 Your First Bankruptcy

### Test Drive (Recommended)

```bash
python bankruptcy_button.py dry-run
```

This shows you exactly what would happen without actually doing it.

### The Real Deal

```bash
python bankruptcy_button.py
```

Follow the interactive prompts for the full ceremonial experience!

## 🔧 Troubleshooting

### "No module named 'google'" Error

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### "credentials.json not found"

1. Make sure the file is in the `email-bankruptcy` folder
2. Check the filename is exactly `credentials.json` (not `credentials.json.txt`)
3. Verify you downloaded it from the correct Google Cloud project

### "Authentication failed"

1. Delete `token.pickle` if it exists
2. Run the script again to re-authenticate
3. Make sure you're using the same Google account that has the emails

### "Gmail API not enabled"

Go back to Google Cloud Console and ensure Gmail API is enabled for your project.

### Rate Limiting / Quota Exceeded

The system respects Gmail API limits, but if you hit issues:
- Wait a few minutes and try again
- Use smaller batch sizes for large inboxes
- Consider running bankruptcy during off-peak hours

## 🎊 Success! What Now?

After your first successful bankruptcy:

1. **Enjoy the zen** of inbox zero
2. **Set up email habits** to prevent future overwhelming
3. **Consider regular maintenance** (maybe quarterly bankruptcies?)
4. **Share your success** - normalize email bankruptcy!

## 🔒 Security Notes

- Your emails never leave your computer except for the bankruptcy notices
- You can revoke Gmail access anytime in your Google Account settings
- The system only accesses what it needs (read, send, modify labels)
- All authentication is handled by Google's secure OAuth system

## 📱 Advanced Tips

### Customize Your Bankruptcy Message

Edit the message template in `bankruptcy_config.json`:

```json
{
  "bankruptcy_message": "Your custom message here..."
}
```

### Schedule Regular Bankruptcies

Add to your calendar:
- Monthly inbox review
- Quarterly bankruptcy consideration
- Annual protection list update

### Team Bankruptcy

Some companies are adopting "Email Bankruptcy Fridays" where the whole team resets together!

---

**You're ready!** Remember, email bankruptcy isn't giving up - it's taking control. Your future self will thank you for this digital decluttering.

🧘 *May the force of inbox zero be with you.*
