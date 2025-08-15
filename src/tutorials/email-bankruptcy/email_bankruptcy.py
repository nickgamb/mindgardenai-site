"""
Email Bankruptcy System - Core Implementation
The main script for declaring email bankruptcy with Gmail

"I hereby declare email bankruptcy. All emails prior to this date are considered null and void.
If your matter requires attention, please resend."
"""

import os
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict, Set
from collections import defaultdict

from config import BankruptcyConfig
from gmail_api import GmailBankruptcyAPI

class EmailBankruptcy:
    """Main email bankruptcy system"""
    
    def __init__(self):
        self.config = BankruptcyConfig()
        self.gmail = GmailBankruptcyAPI()
        self.stats = {
            'emails_processed': 0,
            'emails_protected': 0,
            'emails_bankrupted': 0,
            'unique_senders': 0,
            'bankruptcy_messages_sent': 0,
            'emails_archived': 0
        }
    
    def declare_bankruptcy(self, dry_run: bool = False) -> bool:
        """
        Declare email bankruptcy!
        
        Args:
            dry_run: If True, just show what would happen without actually doing it
        """
        print("\n" + "="*60)
        print("🚨 EMAIL BANKRUPTCY DECLARATION SYSTEM 🚨")
        print("="*60)
        
        # Check if bankruptcy is allowed
        can_declare, reason = self.config.can_declare_bankruptcy()
        if not can_declare:
            print(f"❌ Cannot declare bankruptcy: {reason}")
            return False
        
        print(f"✅ {reason}")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No actual changes will be made")
        
        # Test Gmail connection
        if not self.gmail.test_connection():
            print("❌ Gmail connection failed. Cannot proceed.")
            return False
        
        # Display current configuration
        self.config.print_config_summary()
        
        # Get emails for bankruptcy
        print("📧 Fetching emails for bankruptcy processing...")
        cutoff_days = self.config.config['grace_period_days']
        emails = self.gmail.get_inbox_emails(days_back=cutoff_days, max_results=1000)
        
        if not emails:
            print("📭 No emails found for bankruptcy. Your inbox is clean!")
            return True
        
        self.stats['emails_processed'] = len(emails)
        
        # Process emails
        protected_emails, bankruptcy_emails = self._categorize_emails(emails)
        
        self.stats['emails_protected'] = len(protected_emails)
        self.stats['emails_bankrupted'] = len(bankruptcy_emails)
        
        # Get unique senders for bankruptcy notices
        bankruptcy_senders = self.gmail.get_unique_senders(bankruptcy_emails)
        protected_senders = self.gmail.get_unique_senders(protected_emails)
        
        # Remove protected senders from bankruptcy list
        bankruptcy_senders = [s for s in bankruptcy_senders if s not in protected_senders]
        
        self.stats['unique_senders'] = len(bankruptcy_senders)
        
        # Display summary
        self._display_bankruptcy_summary(protected_emails, bankruptcy_emails, bankruptcy_senders)
        
        # Confirm bankruptcy declaration
        if not dry_run:
            if not self._confirm_bankruptcy():
                print("❌ Bankruptcy declaration cancelled.")
                return False
        
        # Execute bankruptcy
        return self._execute_bankruptcy(bankruptcy_emails, bankruptcy_senders, dry_run)
    
    def _categorize_emails(self, emails: List[Dict]) -> tuple[List[Dict], List[Dict]]:
        """Separate emails into protected and bankruptcy categories"""
        protected_emails = []
        bankruptcy_emails = []
        
        print("🔍 Categorizing emails...")
        
        for email in emails:
            sender = email.get('from', '')
            subject = email.get('subject', '')
            snippet = email.get('snippet', '')
            
            if self.config.is_protected_email(sender, subject, snippet):
                protected_emails.append(email)
                print(f"🛡️  Protected: {sender[:50]}... - {subject[:50]}...")
            else:
                bankruptcy_emails.append(email)
        
        return protected_emails, bankruptcy_emails
    
    def _display_bankruptcy_summary(self, protected_emails: List[Dict], 
                                  bankruptcy_emails: List[Dict], 
                                  bankruptcy_senders: List[str]):
        """Display a summary of what will happen during bankruptcy"""
        print("\n" + "="*60)
        print("📊 BANKRUPTCY SUMMARY")
        print("="*60)
        
        print(f"📧 Total emails processed: {self.stats['emails_processed']}")
        print(f"🛡️  Protected emails: {self.stats['emails_protected']}")
        print(f"💸 Emails to be bankrupted: {self.stats['emails_bankrupted']}")
        print(f"👥 Unique senders to notify: {self.stats['unique_senders']}")
        
        if protected_emails:
            print(f"\n🛡️  PROTECTED EMAILS ({len(protected_emails)}):")
            for email in protected_emails[:10]:  # Show first 10
                print(f"   • {email['from'][:40]}... - {email['subject'][:40]}...")
            if len(protected_emails) > 10:
                print(f"   ... and {len(protected_emails) - 10} more")
        
        if bankruptcy_senders:
            print(f"\n💸 SENDERS TO BE NOTIFIED ({len(bankruptcy_senders)}):")
            for sender in bankruptcy_senders[:15]:  # Show first 15
                print(f"   • {sender}")
            if len(bankruptcy_senders) > 15:
                print(f"   ... and {len(bankruptcy_senders) - 15} more")
        
        print("\n💌 BANKRUPTCY MESSAGE PREVIEW:")
        print("-" * 40)
        message = self.config.get_bankruptcy_message()
        print(message[:500] + "..." if len(message) > 500 else message)
        print("-" * 40)
    
    def _confirm_bankruptcy(self) -> bool:
        """Get user confirmation for bankruptcy declaration"""
        print(f"\n⚠️  FINAL CONFIRMATION ⚠️")
        print("This will:")
        print(f"   1. Send bankruptcy notices to {self.stats['unique_senders']} senders")
        print(f"   2. Archive {self.stats['emails_bankrupted']} emails")
        print(f"   3. Update your bankruptcy score to {self.config.config['bankruptcy_score'] + 1}")
        
        response = input("\nType 'BANKRUPT' to proceed: ").strip()
        
        if response.upper() == 'BANKRUPT':
            print("✅ Bankruptcy confirmed. Proceeding...")
            return True
        else:
            print("❌ Confirmation failed. You must type 'BANKRUPT' exactly.")
            return False
    
    def _execute_bankruptcy(self, bankruptcy_emails: List[Dict], 
                          bankruptcy_senders: List[str], dry_run: bool) -> bool:
        """Execute the bankruptcy process"""
        print("\n🚀 EXECUTING EMAIL BANKRUPTCY...")
        
        if dry_run:
            print("🔍 DRY RUN - Simulating actions:")
            print(f"   Would send {len(bankruptcy_senders)} bankruptcy notices")
            print(f"   Would archive {len(bankruptcy_emails)} emails")
            print(f"   Would update bankruptcy score")
            return True
        
        success = True
        
        # Send bankruptcy notices
        print(f"\n📤 Sending bankruptcy notices to {len(bankruptcy_senders)} senders...")
        bankruptcy_message = self.config.get_bankruptcy_message()
        
        for i, sender in enumerate(bankruptcy_senders, 1):
            try:
                print(f"   ({i}/{len(bankruptcy_senders)}) Sending to {sender}...")
                
                if self.gmail.send_bankruptcy_message(sender, bankruptcy_message):
                    self.stats['bankruptcy_messages_sent'] += 1
                else:
                    print(f"   ⚠️ Failed to send to {sender}")
                    success = False
                
                # Small delay to be respectful to Gmail API
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ❌ Error sending to {sender}: {e}")
                success = False
        
        # Archive emails
        if self.config.config.get('auto_archive_old_emails', True):
            print(f"\n📦 Archiving {len(bankruptcy_emails)} emails...")
            email_ids = [email['id'] for email in bankruptcy_emails]
            
            # Archive in batches of 100 (Gmail API limit)
            batch_size = 100
            for i in range(0, len(email_ids), batch_size):
                batch = email_ids[i:i + batch_size]
                if self.gmail.archive_emails(batch):
                    self.stats['emails_archived'] += len(batch)
                else:
                    print(f"   ⚠️ Failed to archive batch {i//batch_size + 1}")
                    success = False
        
        # Update bankruptcy score and date
        print("\n📈 Updating bankruptcy record...")
        self.config.update_bankruptcy_score()
        
        # Display final stats
        self._display_final_stats()
        
        return success
    
    def _display_final_stats(self):
        """Display final bankruptcy statistics"""
        print("\n" + "="*60)
        print("🎉 EMAIL BANKRUPTCY COMPLETED!")
        print("="*60)
        
        print(f"📧 Emails processed: {self.stats['emails_processed']}")
        print(f"🛡️  Emails protected: {self.stats['emails_protected']}")
        print(f"💸 Emails bankrupted: {self.stats['emails_bankrupted']}")
        print(f"📤 Bankruptcy notices sent: {self.stats['bankruptcy_messages_sent']}")
        print(f"📦 Emails archived: {self.stats['emails_archived']}")
        print(f"📊 Your bankruptcy score: {self.config.config['bankruptcy_score']}")
        
        print(f"\n🎊 Congratulations! You've achieved inbox zen.")
        print(f"💡 Your inbox should now only contain recent and protected emails.")
        print(f"🔄 Important matters will resurface naturally.")
        
        print("\n" + "="*60)
    
    def quick_bankruptcy(self):
        """Quick bankruptcy with minimal prompts - for the truly desperate"""
        print("⚡ QUICK BANKRUPTCY MODE ⚡")
        print("For those who need immediate inbox relief...")
        
        confirm = input("Send bankruptcy notices and archive old emails? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            return self.declare_bankruptcy(dry_run=False)
        else:
            print("Quick bankruptcy cancelled.")
            return False
    
    def bankruptcy_report(self):
        """Generate a report of current inbox status"""
        print("\n📊 EMAIL BANKRUPTCY STATUS REPORT")
        print("="*50)
        
        # Current config
        self.config.print_config_summary()
        
        # Test Gmail connection
        if not self.gmail.test_connection():
            print("❌ Cannot generate report - Gmail connection failed")
            return
        
        # Get current inbox state
        print("📧 Analyzing current inbox...")
        recent_emails = self.gmail.get_inbox_emails(days_back=7, max_results=100)
        old_emails = self.gmail.get_inbox_emails(days_back=30, max_results=500)
        
        print(f"\n📈 INBOX ANALYSIS:")
        print(f"   Recent emails (last 7 days): {len(recent_emails)}")
        print(f"   Old emails (7-30 days): {len(old_emails) - len(recent_emails)}")
        print(f"   Emails ready for bankruptcy: {len(old_emails)}")
        
        if len(old_emails) > 50:
            print(f"\n💡 RECOMMENDATION: You have {len(old_emails)} old emails.")
            print("   Consider declaring email bankruptcy to achieve inbox zen!")
        else:
            print(f"\n✅ GOOD NEWS: Your inbox is relatively clean!")
            print("   You may not need to declare bankruptcy yet.")

def main():
    """Main entry point for email bankruptcy"""
    bankruptcy_system = EmailBankruptcy()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'quick':
            bankruptcy_system.quick_bankruptcy()
        elif command == 'dry-run':
            bankruptcy_system.declare_bankruptcy(dry_run=True)
        elif command == 'report':
            bankruptcy_system.bankruptcy_report()
        elif command == 'bankrupt':
            bankruptcy_system.declare_bankruptcy(dry_run=False)
        else:
            print("Unknown command. Use: quick, dry-run, report, or bankrupt")
    else:
        # Interactive mode
        print("🚨 Welcome to Email Bankruptcy System 🚨")
        print("\nChoose your action:")
        print("1. Declare Bankruptcy (full process)")
        print("2. Quick Bankruptcy (minimal prompts)")
        print("3. Dry Run (see what would happen)")
        print("4. Inbox Report")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            bankruptcy_system.declare_bankruptcy(dry_run=False)
        elif choice == '2':
            bankruptcy_system.quick_bankruptcy()
        elif choice == '3':
            bankruptcy_system.declare_bankruptcy(dry_run=True)
        elif choice == '4':
            bankruptcy_system.bankruptcy_report()
        elif choice == '5':
            print("Goodbye! May your inbox find peace.")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
