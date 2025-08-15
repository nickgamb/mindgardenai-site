#!/usr/bin/env python3
"""
Email Bankruptcy Demo Script
Shows what the system looks like without actually connecting to Gmail
"""

import time
import random
from datetime import datetime

def demo_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🚨 EMAIL BANKRUPTCY DEMO 🚨                              ║
║                                                              ║
║    See what email bankruptcy looks like without              ║
║    actually connecting to your Gmail account                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def simulate_gmail_connection():
    """Simulate Gmail API connection"""
    print("🔗 Connecting to Gmail API...")
    time.sleep(1)
    print("✅ Connected to Gmail account: demo.user@gmail.com")
    return True

def simulate_email_fetch():
    """Simulate fetching emails"""
    print("\n📧 Fetching emails from inbox older than November 15, 2024...")
    time.sleep(2)
    
    # Simulate finding emails
    email_count = random.randint(847, 2341)
    print(f"📫 Found {email_count} emails to process")
    
    return email_count

def simulate_email_categorization(email_count):
    """Simulate categorizing emails"""
    print("\n🔍 Categorizing emails...")
    time.sleep(1)
    
    protected_count = random.randint(15, 45)
    bankruptcy_count = email_count - protected_count
    
    # Show some example protected emails
    protected_examples = [
        "boss@company.com - Quarterly Review Schedule",
        "hr@company.com - Benefits Enrollment Reminder", 
        "spouse@gmail.com - Dinner plans tonight?",
        "bank@chase.com - Important Account Notice",
        "doctor@clinic.com - Appointment Confirmation"
    ]
    
    print(f"🛡️  Protected emails: {protected_count}")
    for email in protected_examples[:3]:
        print(f"   🛡️  Protected: {email}")
        time.sleep(0.3)
    
    if protected_count > 3:
        print(f"   ... and {protected_count - 3} more protected emails")
    
    return protected_count, bankruptcy_count

def simulate_sender_extraction(bankruptcy_count):
    """Simulate extracting unique senders"""
    print(f"\n👥 Extracting unique senders from {bankruptcy_count} bankruptcy emails...")
    time.sleep(1)
    
    unique_senders = random.randint(45, 127)
    
    sender_examples = [
        "newsletter@techcrunch.com",
        "updates@linkedin.com", 
        "noreply@amazon.com",
        "promotions@retailstore.com",
        "alerts@stockapp.com",
        "digest@news-site.com",
        "offers@travel-deals.com",
        "notifications@social-media.com"
    ]
    
    print(f"📊 Found {unique_senders} unique senders to notify")
    print(f"\n💸 SENDERS TO BE NOTIFIED ({min(unique_senders, 8)}):")
    
    for sender in sender_examples[:min(unique_senders, 8)]:
        print(f"   • {sender}")
        time.sleep(0.2)
    
    if unique_senders > 8:
        print(f"   ... and {unique_senders - 8} more")
    
    return unique_senders

def show_bankruptcy_message():
    """Show the bankruptcy message preview"""
    message = f"""
💌 BANKRUPTCY MESSAGE PREVIEW:
----------------------------------------
Subject: Email Bankruptcy Declaration - Action Required

Hello,

I hereby declare email bankruptcy effective {datetime.now().strftime('%B %d, %Y')}. 

All emails prior to this date are considered null and void due to inbox overload. 
If your matter requires attention, please resend your message.

This is not personal - I'm simply drowning in digital communication and need a fresh start. 
Important matters will resurface naturally.

Thank you for understanding!

Best regards,
Demo User

P.S. This is an increasingly common practice for digital wellness.
----------------------------------------
    """
    print(message)

def simulate_bankruptcy_execution(unique_senders, bankruptcy_count):
    """Simulate the actual bankruptcy execution"""
    print("\n🚀 EXECUTING EMAIL BANKRUPTCY...")
    
    # Simulate sending bankruptcy notices
    print(f"\n📤 Sending bankruptcy notices to {unique_senders} senders...")
    
    for i in range(1, min(unique_senders + 1, 6)):
        print(f"   ({i}/{unique_senders}) Sending to sender-{i}@example.com...")
        time.sleep(0.4)
    
    if unique_senders > 5:
        print(f"   ... sending to {unique_senders - 5} more senders")
        time.sleep(1)
    
    print(f"✅ All {unique_senders} bankruptcy notices sent!")
    
    # Simulate archiving emails
    print(f"\n📦 Archiving {bankruptcy_count} emails...")
    time.sleep(1.5)
    print(f"✅ All {bankruptcy_count} emails archived!")
    
    # Simulate updating bankruptcy score
    print(f"\n📈 Updating bankruptcy record...")
    time.sleep(0.5)
    print("✅ Bankruptcy score updated!")

def show_final_stats(email_count, protected_count, bankruptcy_count, unique_senders):
    """Show final bankruptcy statistics"""
    print("\n" + "="*60)
    print("🎉 EMAIL BANKRUPTCY COMPLETED!")
    print("="*60)
    
    print(f"📧 Emails processed: {email_count}")
    print(f"🛡️  Emails protected: {protected_count}")
    print(f"💸 Emails bankrupted: {bankruptcy_count}")
    print(f"📤 Bankruptcy notices sent: {unique_senders}")
    print(f"📦 Emails archived: {bankruptcy_count}")
    print(f"📊 Your bankruptcy score: 1")
    
    print(f"\n🎊 Congratulations! You've achieved inbox zen.")
    print(f"💡 Your inbox should now only contain recent and protected emails.")
    print(f"🔄 Important matters will resurface naturally.")
    
    print("\n" + "="*60)

def main():
    """Run the email bankruptcy demo"""
    demo_banner()
    
    print("🎬 This demo shows what email bankruptcy looks like")
    print("   without actually connecting to your Gmail account.\n")
    
    input("Press Enter to start the demo...")
    
    # Simulate the bankruptcy process
    simulate_gmail_connection()
    
    email_count = simulate_email_fetch()
    
    protected_count, bankruptcy_count = simulate_email_categorization(email_count)
    
    unique_senders = simulate_sender_extraction(bankruptcy_count)
    
    show_bankruptcy_message()
    
    print(f"\n⚠️  FINAL CONFIRMATION (DEMO MODE)")
    print("This would:")
    print(f"   1. Send bankruptcy notices to {unique_senders} senders")
    print(f"   2. Archive {bankruptcy_count} emails")
    print(f"   3. Update your bankruptcy score")
    
    confirm = input("\nType 'DEMO' to continue with simulation: ").strip()
    
    if confirm.upper() == 'DEMO':
        simulate_bankruptcy_execution(unique_senders, bankruptcy_count)
        show_final_stats(email_count, protected_count, bankruptcy_count, unique_senders)
        
        print("\n🌟 Demo completed!")
        print("💡 To run the real thing, use: python bankruptcy_button.py")
        print("🔧 Don't forget to set up Gmail API first!")
        
    else:
        print("❌ Demo cancelled.")
    
    print("\n📧 Remember: Your inbox doesn't define you.")
    print("🧘 Email bankruptcy is self-care, not failure.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚡ Demo interrupted.")
        print("💭 Ready to try the real thing?")
    except Exception as e:
        print(f"\n💥 Demo error: {e}")
    
    input("\nPress Enter to exit...")
