#!/usr/bin/env python3
"""
THE EMAIL BANKRUPTCY BUTTON 🚨
One-click email freedom for the desperately drowning

Usage:
    python bankruptcy_button.py          # Interactive mode
    python bankruptcy_button.py quick    # Quick bankruptcy (minimal prompts)
    python bankruptcy_button.py dry-run  # See what would happen
    python bankruptcy_button.py report   # Check inbox status
"""

import sys
import os
import time
from datetime import datetime

# ASCII art for maximum dramatic effect
BANKRUPTCY_BANNER = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🚨 EMAIL BANKRUPTCY BUTTON 🚨                            ║
║                                                              ║
║    "I hereby declare email bankruptcy.                      ║
║     All emails prior to this date are null and void.        ║
║     If your matter requires attention, please resend."       ║
║                                                              ║
║                    Press any key to continue...              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

PANIC_MODE_BANNER = """
┌─────────────────────────────────────────────────┐
│  🆘 PANIC MODE: INSTANT EMAIL BANKRUPTCY 🆘   │
│                                                 │
│  For those drowning in digital despair...       │
│  One button press = Immediate inbox relief      │
│                                                 │
│  WARNING: This is the nuclear option!          │
└─────────────────────────────────────────────────┘
"""

def show_motivation():
    """Show motivational messages for email bankruptcy"""
    motivations = [
        "🧘 Inbox zero is a state of mind, not a number.",
        "📧 Your worth is not measured by your unread count.",
        "🔥 Sometimes you have to burn the old to plant the new.",
        "🌊 Don't drown in digital detritus - declare freedom!",
        "⚡ Email bankruptcy: The ultimate reset button.",
        "🎯 Focus on what matters. Let the rest go.",
        "🦋 From email chaos, inbox zen emerges.",
        "🚀 One small step for you, one giant leap for productivity.",
        "💎 Your attention is precious. Protect it.",
        "🌟 Today is the first day of your email-free life."
    ]
    
    import random
    return random.choice(motivations)

def panic_mode():
    """Super quick bankruptcy for those in email crisis"""
    print(PANIC_MODE_BANNER)
    print(show_motivation())
    print("\n🔥 EMERGENCY EMAIL BANKRUPTCY ACTIVATED")
    print("   This will immediately:")
    print("   • Send bankruptcy notices to ALL old email senders")
    print("   • Archive ALL old emails (except protected)")
    print("   • Reset your inbox to zen state")
    
    confirm = input("\n💥 Type 'NUCLEAR' to proceed with panic mode: ").strip()
    
    if confirm.upper() == 'NUCLEAR':
        print("\n🚨 EXECUTING PANIC MODE BANKRUPTCY...")
        
        # Import and run the main bankruptcy system
        try:
            from email_bankruptcy import EmailBankruptcy
            bankruptcy = EmailBankruptcy()
            return bankruptcy.declare_bankruptcy(dry_run=False)
        except ImportError as e:
            print(f"❌ Error: {e}")
            print("Please ensure all dependencies are installed: pip install -r requirements.txt")
            return False
    else:
        print("❌ Panic mode cancelled. Crisis continues...")
        return False

def interactive_bankruptcy():
    """Interactive bankruptcy declaration with full ceremony"""
    print(BANKRUPTCY_BANNER)
    input()  # Wait for user to press any key
    
    print("\n" + show_motivation())
    print(f"\n📅 Today is {datetime.now().strftime('%A, %B %d, %Y')}")
    print("🎯 Today could be the day you achieve inbox freedom.")
    
    print("\n🤔 How desperate is your email situation?")
    print("1. 😰 Drowning (1000+ unread emails)")
    print("2. 😅 Struggling (100-1000 unread emails)")
    print("3. 😐 Managing (10-100 unread emails)")
    print("4. 😌 Actually fine (less than 10 unread)")
    print("5. 🚨 PANIC MODE - Just make it stop!")
    
    choice = input("\nChoose your desperation level (1-5): ").strip()
    
    if choice == '5':
        return panic_mode()
    elif choice in ['1', '2', '3', '4']:
        print(f"\n📊 Assessment: Your email situation is {'critical' if choice in ['1','2'] else 'manageable'}")
        
        if choice in ['1', '2']:
            print("💡 Email bankruptcy is highly recommended for your sanity.")
        else:
            print("💡 Email bankruptcy might be overkill, but sometimes we all need a fresh start.")
        
        print("\n🎬 Proceeding to full bankruptcy ceremony...")
        
        try:
            from email_bankruptcy import EmailBankruptcy
            bankruptcy = EmailBankruptcy()
            return bankruptcy.declare_bankruptcy(dry_run=False)
        except ImportError as e:
            print(f"❌ Error: {e}")
            print("Please ensure all dependencies are installed: pip install -r requirements.txt")
            return False
    else:
        print("❌ Invalid choice. Bankruptcy cancelled.")
        return False

def quick_status_check():
    """Quick check of bankruptcy eligibility"""
    try:
        from config import BankruptcyConfig
        from gmail_api import GmailBankruptcyAPI
        
        config = BankruptcyConfig()
        gmail = GmailBankruptcyAPI()
        
        print("🔍 QUICK STATUS CHECK")
        print("=" * 30)
        
        # Check bankruptcy eligibility
        can_declare, reason = config.can_declare_bankruptcy()
        print(f"Bankruptcy Status: {'✅ ELIGIBLE' if can_declare else '❌ RESTRICTED'}")
        print(f"Reason: {reason}")
        
        # Check Gmail connection
        print(f"Gmail Connection: {'✅ CONNECTED' if gmail.test_connection() else '❌ FAILED'}")
        
        # Quick inbox count
        print("📊 Checking inbox...")
        old_emails = gmail.get_inbox_emails(days_back=30, max_results=100)
        print(f"Old emails ready for bankruptcy: {len(old_emails)}")
        
        if len(old_emails) > 20 and can_declare:
            print("\n💡 RECOMMENDATION: You're a good candidate for email bankruptcy!")
            return True
        else:
            print("\n✅ Your inbox situation is manageable.")
            return False
            
    except ImportError as e:
        print(f"❌ Status check failed: {e}")
        return False

def main():
    """The main bankruptcy button interface"""
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ['panic', 'emergency', 'help']:
            return panic_mode()
        elif command in ['quick', 'fast']:
            try:
                from email_bankruptcy import EmailBankruptcy
                bankruptcy = EmailBankruptcy()
                return bankruptcy.quick_bankruptcy()
            except ImportError as e:
                print(f"❌ Error: {e}")
                return False
        elif command in ['dry-run', 'test', 'preview']:
            try:
                from email_bankruptcy import EmailBankruptcy
                bankruptcy = EmailBankruptcy()
                return bankruptcy.declare_bankruptcy(dry_run=True)
            except ImportError as e:
                print(f"❌ Error: {e}")
                return False
        elif command in ['report', 'status', 'check']:
            return quick_status_check()
        elif command in ['full', 'complete']:
            return interactive_bankruptcy()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: panic, quick, dry-run, report, full")
            return False
    
    # No arguments - run interactive mode
    return interactive_bankruptcy()

if __name__ == "__main__":
    try:
        success = main()
        
        if success:
            print("\n🎉 Email bankruptcy process completed!")
            print("🌟 Welcome to your new, zen inbox life!")
        else:
            print("\n😔 Email bankruptcy was not completed.")
            print("💪 But you took the first step toward inbox freedom!")
            
    except KeyboardInterrupt:
        print("\n\n⚡ Bankruptcy interrupted by user.")
        print("💭 Sometimes the hardest part is just pressing the button...")
    except Exception as e:
        print(f"\n💥 Unexpected error during bankruptcy: {e}")
        print("🔧 Please check your setup and try again.")
    
    print("\n📧 Remember: Your inbox doesn't define you.")
    print("🧘 Email bankruptcy is self-care, not failure.")
    input("\nPress Enter to exit...")
