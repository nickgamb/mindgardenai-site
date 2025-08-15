"""
Gmail API Integration for Email Bankruptcy
Handles authentication and email operations
"""

import os
import pickle
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Gmail API dependencies not installed. Run: pip install -r requirements.txt")
    exit(1)

class GmailBankruptcyAPI:
    """Gmail API wrapper for email bankruptcy operations"""
    
    # Gmail API scopes needed for email bankruptcy
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.modify'
    ]
    
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"""
=== GMAIL API SETUP REQUIRED ===
1. Go to: https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download credentials as '{self.credentials_file}'
6. Place the file in this directory: {os.getcwd()}

Detailed instructions: https://developers.google.com/gmail/api/quickstart/python
==================================
                    """)
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            print("✅ Gmail API authentication successful!")
            return True
        except Exception as e:
            print(f"❌ Gmail API authentication failed: {e}")
            return False
    
    def get_inbox_emails(self, days_back: int = 30, max_results: int = 500) -> List[Dict]:
        """Get emails from inbox for bankruptcy processing"""
        if not self.service:
            print("❌ Gmail service not authenticated")
            return []
        
        try:
            # Calculate date filter
            cutoff_date = datetime.now() - timedelta(days=days_back)
            query = f'in:inbox before:{cutoff_date.strftime("%Y/%m/%d")}'
            
            print(f"📧 Fetching emails from inbox older than {cutoff_date.strftime('%B %d, %Y')}...")
            
            # Get message list
            results = self.service.users().messages().list(
                userId='me', 
                q=query, 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print("📭 No emails found matching criteria")
                return []
            
            print(f"📫 Found {len(messages)} emails to process")
            
            # Get detailed message info
            email_details = []
            for msg in messages[:max_results]:  # Limit processing
                try:
                    message = self.service.users().messages().get(
                        userId='me', 
                        id=msg['id']
                    ).execute()
                    
                    # Extract email details
                    headers = message['payload'].get('headers', [])
                    email_info = {
                        'id': msg['id'],
                        'from': self._get_header_value(headers, 'From'),
                        'to': self._get_header_value(headers, 'To'),
                        'subject': self._get_header_value(headers, 'Subject'),
                        'date': self._get_header_value(headers, 'Date'),
                        'thread_id': message.get('threadId'),
                        'snippet': message.get('snippet', ''),
                        'labels': message.get('labelIds', [])
                    }
                    
                    email_details.append(email_info)
                    
                except HttpError as e:
                    print(f"⚠️ Error fetching message {msg['id']}: {e}")
                    continue
            
            return email_details
            
        except HttpError as e:
            print(f"❌ Error fetching inbox emails: {e}")
            return []
    
    def send_bankruptcy_message(self, to_email: str, bankruptcy_message: str) -> bool:
        """Send bankruptcy declaration to a specific email"""
        if not self.service:
            print("❌ Gmail service not authenticated")
            return False
        
        try:
            # Create message
            message = MIMEMultipart()
            message['to'] = to_email
            message['subject'] = "Email Bankruptcy Declaration - Action Required"
            
            # Add bankruptcy message
            message.attach(MIMEText(bankruptcy_message, 'plain'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send message
            send_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f"✅ Bankruptcy notice sent to: {to_email}")
            return True
            
        except HttpError as e:
            print(f"❌ Error sending bankruptcy message to {to_email}: {e}")
            return False
    
    def archive_emails(self, email_ids: List[str]) -> bool:
        """Archive a list of emails (remove from inbox)"""
        if not self.service or not email_ids:
            return False
        
        try:
            # Gmail API batch request to remove inbox label
            self.service.users().messages().batchModify(
                userId='me',
                body={
                    'ids': email_ids,
                    'removeLabelIds': ['INBOX']
                }
            ).execute()
            
            print(f"📦 Archived {len(email_ids)} emails")
            return True
            
        except HttpError as e:
            print(f"❌ Error archiving emails: {e}")
            return False
    
    def _get_header_value(self, headers: List[Dict], header_name: str) -> str:
        """Extract header value from email headers"""
        for header in headers:
            if header['name'].lower() == header_name.lower():
                return header['value']
        return ''
    
    def _extract_email_address(self, from_field: str) -> str:
        """Extract email address from 'From' field"""
        import re
        email_pattern = r'<([^>]+)>'
        match = re.search(email_pattern, from_field)
        if match:
            return match.group(1)
        elif '@' in from_field:
            return from_field.strip()
        return from_field
    
    def get_unique_senders(self, emails: List[Dict]) -> List[str]:
        """Get unique sender email addresses from email list"""
        senders = set()
        for email in emails:
            from_field = email.get('from', '')
            if from_field:
                sender_email = self._extract_email_address(from_field)
                if sender_email and '@' in sender_email:
                    senders.add(sender_email)
        
        return list(senders)
    
    def test_connection(self) -> bool:
        """Test Gmail API connection"""
        if not self.service:
            return False
        
        try:
            # Try to get user profile
            profile = self.service.users().getProfile(userId='me').execute()
            email = profile.get('emailAddress')
            print(f"✅ Connected to Gmail account: {email}")
            return True
        except HttpError as e:
            print(f"❌ Gmail connection test failed: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    print("🚀 Testing Gmail API connection...")
    gmail = GmailBankruptcyAPI()
    
    if gmail.test_connection():
        print("📧 Ready for email bankruptcy operations!")
    else:
        print("❌ Gmail API setup required. See instructions above.")
