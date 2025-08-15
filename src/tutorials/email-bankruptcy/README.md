# 🚨 Email Bankruptcy System 🚨

**"I hereby declare email bankruptcy. All emails prior to this date are considered null and void. If your matter requires attention, please resend."**

A Python-based system for declaring email bankruptcy with Gmail - because sometimes you just need to reset your digital life!

## 🎯 What is Email Bankruptcy?

Email bankruptcy is a universally recognized protocol where you officially declare that you're starting fresh with your inbox. Instead of spending 47 hours sorting through digital detritus, you send an automated message to everyone letting them know that important matters need to be resent.

### Why This Actually Works:

1. **It's honest** - Your 14,847 unread emails aren't getting answered anyway
2. **Natural selection for your inbox** - Important stuff will resurface, random newsletters won't
3. **Immediate relief** - Imagine the dopamine hit of seeing "Inbox: 0"
4. **Normalized approach** - Make it as common as "out of office" messages

## 🚀 Quick Start

### 1. Setup Dependencies

```bash
cd email-bankruptcy
pip install -r requirements.txt
```

### 2. Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download credentials as `credentials.json`
6. Place the file in the `email-bankruptcy` directory

Detailed instructions: [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)

### 3. The Bankruptcy Button

```bash
# Interactive mode with full ceremony
python bankruptcy_button.py

# Quick bankruptcy (minimal prompts)
python bankruptcy_button.py quick

# Panic mode (for email emergencies)
python bankruptcy_button.py panic

# See what would happen (safe mode)
python bankruptcy_button.py dry-run

# Check your inbox status
python bankruptcy_button.py report
```

## 📋 Features

### 🛡️ Protected Email Categories
- Specific email addresses (boss, family, etc.)
- Domain protection (company emails, etc.)
- Keyword protection (urgent, invoice, contract)
- Automatic smart filtering

### ⚡ Bankruptcy Options
- **Full Bankruptcy**: Complete ceremony with confirmation
- **Quick Mode**: Minimal prompts for the desperate
- **Panic Mode**: Nuclear option for email emergencies
- **Dry Run**: See what would happen without doing it

### 📊 Smart Features
- Grace periods (default: 30 days)
- Bankruptcy "credit score" tracking
- Quarterly limits to prevent abuse
- Detailed reporting and statistics
- Automatic email archiving

### 🎨 User Experience
- Beautiful ASCII art interfaces
- Motivational messaging
- Progress tracking
- Detailed confirmations
- Emergency interrupt handling

## 🔧 Configuration

Edit your settings in the auto-generated `bankruptcy_config.json`:

```json
{
  "protected_emails": [
    "boss@company.com",
    "spouse@gmail.com"
  ],
  "protected_domains": [
    "mycompany.com"
  ],
  "protected_keywords": [
    "urgent", "invoice", "contract"
  ],
  "grace_period_days": 30,
  "max_bankruptcies_per_quarter": 1,
  "user_name": "Your Name Here"
}
```

## 📖 Usage Examples

### The Classic Bankruptcy Declaration

```bash
python bankruptcy_button.py
```

This runs the full interactive experience with:
- Motivational messaging
- Configuration review
- Email categorization
- Protected email filtering
- Confirmation ceremony
- Bankruptcy notice sending
- Automatic archiving

### Emergency Relief

```bash
python bankruptcy_button.py panic
```

For those drowning in email despair who need immediate relief.

### Status Check

```bash
python bankruptcy_button.py report
```

Get a summary of:
- Current bankruptcy eligibility
- Inbox analysis
- Protected vs bankruptcy-ready emails
- Recommendations

## 🎭 The Psychology of Email Bankruptcy

### Bankruptcy Message Template

The system sends a professional, honest message:

```
Subject: Email Bankruptcy Declaration - Action Required

Hello,

I hereby declare email bankruptcy effective [DATE]. 

All emails prior to this date are considered null and void due to inbox overload. 
If your matter requires attention, please resend your message.

This is not personal - I'm simply drowning in digital communication and need a fresh start. 
Important matters will resurface naturally.

Thank you for understanding!

Best regards,
[YOUR NAME]
```

### The Relief Protocol

1. **Acknowledgment**: Accept that you're overwhelmed
2. **Declaration**: Officially announce the bankruptcy
3. **Delegation**: Put the burden back on senders
4. **Automation**: Let the system handle the mechanics
5. **Freedom**: Experience the zen of inbox zero

## 🔒 Privacy & Security

- All email processing happens locally on your machine
- No email content is stored or transmitted to third parties
- Gmail API uses OAuth 2.0 for secure authentication
- You can revoke access at any time in your Google Account settings
- Protected emails are never included in bankruptcy notices

## 🐛 Troubleshooting

### Gmail API Issues

1. Ensure `credentials.json` is in the correct directory
2. Check that Gmail API is enabled in Google Cloud Console
3. Verify OAuth consent screen is configured
4. Try removing `token.pickle` and re-authenticating

### Permission Errors

The system needs these Gmail permissions:
- Read emails (to categorize them)
- Send emails (to send bankruptcy notices)
- Modify emails (to archive old emails)

### Rate Limiting

The system includes built-in delays to respect Gmail API limits. For large inboxes, bankruptcy may take several minutes.

## 🎪 Fun Commands

```bash
# Check if you're a good candidate for bankruptcy
python bankruptcy_button.py status

# Test the waters without committing
python bankruptcy_button.py dry-run

# When you're absolutely desperate
python bankruptcy_button.py panic

# The full ceremonial experience
python bankruptcy_button.py full
```

## 🌟 The Email Bankruptcy Movement

Help normalize email bankruptcy! Share your experience:

- "Just declared email bankruptcy - inbox went from 2,847 to 0!"
- "Email bankruptcy isn't failure, it's self-care"
- "Sometimes you have to burn the digital detritus to plant new productivity"

## 📜 License & Contributing

This is open-source digital wellness software. Feel free to:
- Fork and customize for your needs
- Add new bankruptcy protocols
- Improve the user experience
- Share your bankruptcy success stories

## 🚨 Disclaimer

Email bankruptcy is a nuclear option for inbox management. While cathartic and effective, use responsibly:

- Always review protected email settings first
- Consider a dry run before full bankruptcy
- Remember that some emails might actually be important
- This tool is for digital wellness, not avoiding responsibilities

---

**Remember**: Your inbox doesn't define you. Email bankruptcy is self-care, not failure. Sometimes the bravest thing you can do is press the reset button.

🧘 *May your inbox find peace, and may you find freedom from digital overwhelm.*
