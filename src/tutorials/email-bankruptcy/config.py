"""
Email Bankruptcy Configuration
Settings and protected email management
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Set

class BankruptcyConfig:
    def __init__(self, config_file="bankruptcy_config.json"):
        self.config_file = config_file
        self.default_config = {
            "protected_emails": [
                # Add email addresses that should never be bankrupted
                # Example: "boss@company.com", "spouse@gmail.com"
            ],
            "protected_domains": [
                # Add domains that should be protected
                # Example: "yourcompany.com", "family.com"
            ],
            "protected_keywords": [
                # Emails containing these keywords won't be bankrupted
                "urgent", "important", "invoice", "payment", "contract"
            ],
            "grace_period_days": 30,
            "bankruptcy_message": """
Subject: Email Bankruptcy Declaration - Action Required

Hello,

I hereby declare email bankruptcy effective {date}. 

All emails prior to this date are considered null and void due to inbox overload. If your matter requires attention, please resend your message.

This is not personal - I'm simply drowning in digital communication and need a fresh start. Important matters will resurface naturally.

Thank you for understanding!

Best regards,
{name}

P.S. This is an increasingly common practice for digital wellness. Learn more about email bankruptcy at: [your blog/explanation]
            """,
            "bankruptcy_score": 0,  # How many times user has declared bankruptcy
            "last_bankruptcy_date": None,
            "user_name": "Email User",
            "max_bankruptcies_per_quarter": 1,
            "auto_archive_old_emails": True,
            "send_bankruptcy_report": True
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    merged_config = self.default_config.copy()
                    merged_config.update(config)
                    return merged_config
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.default_config.copy()
        else:
            return self.default_config.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def is_protected_email(self, email_address: str, subject: str = "", body: str = "") -> bool:
        """Check if an email should be protected from bankruptcy"""
        email_lower = email_address.lower()
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Check protected emails
        if email_lower in [e.lower() for e in self.config["protected_emails"]]:
            return True
        
        # Check protected domains
        for domain in self.config["protected_domains"]:
            if domain.lower() in email_lower:
                return True
        
        # Check protected keywords in subject and body
        for keyword in self.config["protected_keywords"]:
            if keyword.lower() in subject_lower or keyword.lower() in body_lower:
                return True
        
        return False
    
    def can_declare_bankruptcy(self) -> tuple[bool, str]:
        """Check if user can declare bankruptcy based on quarterly limits"""
        last_bankruptcy = self.config.get("last_bankruptcy_date")
        if not last_bankruptcy:
            return True, "No previous bankruptcy declarations"
        
        last_date = datetime.fromisoformat(last_bankruptcy) if isinstance(last_bankruptcy, str) else last_bankruptcy
        current_quarter_start = self.get_current_quarter_start()
        
        if last_date >= current_quarter_start:
            bankruptcies_this_quarter = 1  # Simplified - could track multiple per quarter
            max_allowed = self.config["max_bankruptcies_per_quarter"]
            
            if bankruptcies_this_quarter >= max_allowed:
                return False, f"Maximum {max_allowed} bankruptcies per quarter exceeded"
        
        return True, "Bankruptcy allowed"
    
    def get_current_quarter_start(self) -> datetime:
        """Get the start date of the current quarter"""
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        quarter_start_month = (quarter - 1) * 3 + 1
        return datetime(now.year, quarter_start_month, 1)
    
    def update_bankruptcy_score(self):
        """Increment bankruptcy score and update last bankruptcy date"""
        self.config["bankruptcy_score"] += 1
        self.config["last_bankruptcy_date"] = datetime.now().isoformat()
        self.save_config()
    
    def add_protected_email(self, email: str):
        """Add an email to the protected list"""
        if email not in self.config["protected_emails"]:
            self.config["protected_emails"].append(email)
            self.save_config()
    
    def remove_protected_email(self, email: str):
        """Remove an email from the protected list"""
        if email in self.config["protected_emails"]:
            self.config["protected_emails"].remove(email)
            self.save_config()
    
    def get_bankruptcy_message(self) -> str:
        """Get formatted bankruptcy message"""
        return self.config["bankruptcy_message"].format(
            date=datetime.now().strftime("%B %d, %Y"),
            name=self.config["user_name"]
        )
    
    def print_config_summary(self):
        """Print a summary of current configuration"""
        print("\n=== EMAIL BANKRUPTCY CONFIGURATION ===")
        print(f"Protected Emails: {len(self.config['protected_emails'])}")
        print(f"Protected Domains: {len(self.config['protected_domains'])}")
        print(f"Protected Keywords: {len(self.config['protected_keywords'])}")
        print(f"Grace Period: {self.config['grace_period_days']} days")
        print(f"Bankruptcy Score: {self.config['bankruptcy_score']}")
        print(f"Last Bankruptcy: {self.config['last_bankruptcy_date'] or 'Never'}")
        print(f"Max Bankruptcies/Quarter: {self.config['max_bankruptcies_per_quarter']}")
        print("=====================================\n")

# Example usage
if __name__ == "__main__":
    config = BankruptcyConfig()
    config.print_config_summary()
