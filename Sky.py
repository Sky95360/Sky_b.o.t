import pywhatkit as kit
import requests
from datetime import datetime, timedelta
import time
import schedule
import json
import os
import logging
from typing import List, Dict, Optional
import pandas as pd
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SkyWhatsAppBot:
    def __init__(self):
        """Initialize Sky WhatsApp Bot"""
        # Your contact information
        self.your_number = "0748529340"  # South Africa number
        self.country_code = "27"  # South Africa country code
        self.github_url = "https://github.com/Sky95360/Sky_b.o.t"
        
        # WhatsApp Web configuration
        self.wait_time = 20  # seconds for WhatsApp Web to load
        self.close_tab = True
        self.tab_close_delay = 3
        
        # Data storage
        self.contacts_file = "contacts.json"
        self.messages_file = "messages.json"
        self.scheduled_tasks = []
        
        # Create data files if they don't exist
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Create necessary data files"""
        default_contacts = [
            {
                "name": "Sky Bot Admin",
                "phone": self.your_number,
                "country_code": self.country_code,
                "group": "admin"
            }
        ]
        
        default_messages = [
            {
                "id": 1,
                "content": "Hello from Sky Bot! 🤖",
                "category": "greeting"
            },
            {
                "id": 2,
                "content": "Your GitHub repository: https://github.com/Sky95360/Sky_b.o.t",
                "category": "info"
            },
            {
                "id": 3,
                "content": "Sky Bot is online and ready to help!",
                "category": "status"
            }
        ]
        
        # Create contacts file
        if not os.path.exists(self.contacts_file):
            with open(self.contacts_file, 'w') as f:
                json.dump(default_contacts, f, indent=4)
            logger.info(f"Created {self.contacts_file}")
        
        # Create messages file
        if not os.path.exists(self.messages_file):
            with open(self.messages_file, 'w') as f:
                json.dump(default_messages, f, indent=4)
            logger.info(f"Created {self.messages_file}")
    
    def format_phone_number(self, phone_number: str) -> str:
        """
        Format phone number for WhatsApp
        
        Args:
            phone_number: Phone number to format
            
        Returns:
            Formatted phone number with country code
        """
        # Remove any non-digit characters
        phone_digits = re.sub(r'\D', '', phone_number)
        
        # If number starts with 0, replace with country code
        if phone_digits.startswith('0'):
            phone_digits = self.country_code + phone_digits[1:]
        
        # Ensure it starts with country code
        if not phone_digits.startswith(self.country_code):
            phone_digits = self.country_code + phone_digits
        
        return phone_digits
    
    def send_instant_message(self, phone_number: str, message: str) -> bool:
        """
        Send instant message using pywhatkit
        
        Args:
            phone_number: Recipient's phone number
            message: Message to send
            
        Returns:
            bool: Success status
        """
        try:
            formatted_number = self.format_phone_number(phone_number)
            
            # Send message immediately
            kit.sendwhatmsg_instantly(
                phone_no=f"+{formatted_number}",
                message=message,
                wait_time=self.wait_time,
                tab_close=self.close_tab,
                close_time=self.tab_close_delay
            )
            
            logger.info(f"Message sent to {formatted_number}: {message[:50]}...")
            
            # Log the message
            self.log_message(formatted_number, message, "instant")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message to {phone_number}: {str(e)}")
            return False
    
    def send_scheduled_message(self, phone_number: str, message: str, hour: int, minute: int) -> bool:
        """
        Schedule a message for specific time
        
        Args:
            phone_number: Recipient's phone number
            message: Message to send
            hour: Hour (0-23)
            minute: Minute (0-59)
            
        Returns:
            bool: Success status
        """
        try:
            formatted_number = self.format_phone_number(phone_number)
            
            # Calculate time (today or tomorrow if time has passed)
            now = datetime.now()
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if target_time < now:
                target_time += timedelta(days=1)
            
            # Send scheduled message
            kit.sendwhatmsg(
                phone_no=f"+{formatted_number}",
                message=message,
                time_hour=hour,
                time_min=minute,
                wait_time=self.wait_time,
                tab_close=self.close_tab,
                close_time=self.tab_close_delay
            )
            
            logger.info(f"Scheduled message to {formatted_number} at {hour:02d}:{minute:02d}")
            
            # Schedule task for recurring if needed
            task_id = f"{formatted_number}_{hour}_{minute}"
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(
                self.send_instant_message, formatted_number, message
            ).tag(task_id)
            
            self.scheduled_tasks.append({
                "id": task_id,
                "phone": formatted_number,
                "message": message,
                "time": f"{hour:02d}:{minute:02d}",
                "scheduled_at": datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to schedule message: {str(e)}")
            return False
    
    def send_to_multiple_contacts(self, phone_numbers: List[str], message: str) -> Dict[str, bool]:
        """
        Send message to multiple contacts
        
        Args:
            phone_numbers: List of phone numbers
            message: Message to send
            
        Returns:
            Dict with results for each number
        """
        results = {}
        
        for phone in phone_numbers:
            success = self.send_instant_message(phone, message)
            results[phone] = success
            
            # Add delay between messages to avoid rate limiting
            time.sleep(5)
        
        return results
    
    def send_with_attachment(self, phone_number: str, message: str, file_path: str) -> bool:
        """
        Send message with file attachment
        
        Args:
            phone_number: Recipient's phone number
            message: Message to send
            file_path: Path to file
            
        Returns:
            bool: Success status
        """
        try:
            formatted_number = self.format_phone_number(phone_number)
            
            # Check if file exists
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False
            
            # Send image with caption
            kit.sendwhats_image(
                receiver=f"+{formatted_number}",
                img_path=file_path,
                caption=message,
                wait_time=self.wait_time,
                tab_close=self.close_tab,
                close_time=self.tab_close_delay
            )
            
            logger.info(f"Sent attachment to {formatted_number}: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send attachment: {str(e)}")
            return False
    
    def log_message(self, phone_number: str, message: str, msg_type: str):
        """
        Log sent message
        
        Args:
            phone_number: Recipient's number
            message: Message content
            msg_type: Type of message
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "phone": phone_number,
            "message": message,
            "type": msg_type,
            "status": "sent"
        }
        
        # Append to log file
        log_file = "message_log.json"
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=4)
    
    def add_contact(self, name: str, phone_number: str, group: str = "general"):
        """
        Add new contact to database
        
        Args:
            name: Contact name
            phone_number: Phone number
            group: Contact group
        """
        try:
            formatted_number = self.format_phone_number(phone_number)
            
            with open(self.contacts_file, 'r') as f:
                contacts = json.load(f)
            
            # Check if contact already exists
            for contact in contacts:
                if contact["phone"] == formatted_number:
                    logger.warning(f"Contact already exists: {formatted_number}")
                    return False
            
            # Add new contact
            new_contact = {
                "name": name,
                "phone": formatted_number,
                "country_code": self.country_code,
                "group": group,
                "added_at": datetime.now().isoformat()
            }
            
            contacts.append(new_contact)
            
            with open(self.contacts_file, 'w') as f:
                json.dump(contacts, f, indent=4)
            
            logger.info(f"Added contact: {name} ({formatted_number})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add contact: {str(e)}")
            return False
    
    def broadcast_to_group(self, group: str, message: str) -> Dict[str, bool]:
        """
        Broadcast message to specific group
        
        Args:
            group: Group name
            message: Message to broadcast
            
        Returns:
            Dict with results
        """
        try:
            with open(self.contacts_file, 'r') as f:
                contacts = json.load(f)
            
            # Filter contacts by group
            group_contacts = [c for c in contacts if c.get("group") == group]
            
            if not group_contacts:
                logger.warning(f"No contacts found in group: {group}")
                return {}
            
            # Get phone numbers
            phone_numbers = [contact["phone"] for contact in group_contacts]
            
            # Send to all contacts in group
            results = self.send_to_multiple_contacts(phone_numbers, message)
            
            logger.info(f"Broadcast to group '{group}': {len(results)} contacts")
            return results
            
        except Exception as e:
            logger.error(f"Failed to broadcast to group: {str(e)}")
            return {}
    
    def check_github_status(self):
        """
        Check GitHub repository status
        """
        try:
            # Extract username and repo from URL
            url = "https://api.github.com/repos/Sky95360/Sky_b.o.t"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                repo_data = response.json()
                status_msg = f"GitHub Status: ✅ Online\nRepository: {repo_data['full_name']}\nStars: {repo_data['stargazers_count']}\nLast Updated: {repo_data['updated_at']}"
                return status_msg
            else:
                return "GitHub Status: ❌ Cannot access repository"
                
        except Exception as e:
            return f"GitHub Status: ❌ Error: {str(e)}"
    
    def send_bot_status(self, phone_number: str):
        """
        Send bot status information
        """
        try:
            formatted_number = self.format_phone_number(phone_number)
            
            # Create status message
            status_message = f"""🤖 *Sky Bot Status Report* 🤖

📞 Bot Phone: {self.your_number}
🌍 Country Code: +{self.country_code}
🔗 GitHub: {self.github_url}
🕒 Local Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 Total Contacts: {self.get_contact_count()}
📨 Messages Sent Today: {self.get_today_message_count()}
🔧 Bot Version: 1.0.0
✅ Status: Operational

{self.check_github_status()}

_Sky Bot - Automated WhatsApp Assistant_"""
            
            # Send status
            self.send_instant_message(formatted_number, status_message)
            
        except Exception as e:
            logger.error(f"Failed to send status: {str(e)}")
    
    def get_contact_count(self) -> int:
        """
        Get total number of contacts
        """
        try:
            with open(self.contacts_file, 'r') as f:
                contacts = json.load(f)
            return len(contacts)
        except:
            return 0
    
    def get_today_message_count(self) -> int:
        """
        Get number of messages sent today
        """
        try:
            log_file = "message_log.json"
            if not os.path.exists(log_file):
                return 0
            
            with open(log_file, 'r') as f:
                logs = json.load(f)
            
            today = datetime.now().date()
            today_logs = [
                log for log in logs 
                if datetime.fromisoformat(log["timestamp"]).date() == today
            ]
            
            return len(today_logs)
        except:
            return 0
    
    def menu(self):
        """
        Display interactive menu
        """
        print("=" * 50)
        print("🤖 SKY WHATSAPP BOT 🤖")
        print("=" * 50)
        print(f"Your Number: {self.your_number}")
        print(f"GitHub: {self.github_url}")
        print("=" * 50)
        
        while True:
            print("\n" + "=" * 30)
            print("📱 MAIN MENU")
            print("=" * 30)
            print("1. Send Instant Message")
            print("2. Schedule Message")
            print("3. Send to Multiple Contacts")
            print("4. Send with Attachment")
            print("5. Add New Contact")
            print("6. Broadcast to Group")
            print("7. Send Bot Status")
            print("8. View Statistics")
            print("9. Check GitHub Status")
            print("10. Exit")
            print("=" * 30)
            
            choice = input("Select option (1-10): ").strip()
            
            if choice == "1":
                phone = input("Enter phone number: ").strip()
                message = input("Enter message: ").strip()
                self.send_instant_message(phone, message)
                
            elif choice == "2":
                phone = input("Enter phone number: ").strip()
                message = input("Enter message: ").strip()
                time_input = input("Enter time (HH:MM): ").strip()
                try:
                    hour, minute = map(int, time_input.split(":"))
                    self.send_scheduled_message(phone, message, hour, minute)
                except:
                    print("Invalid time format!")
                    
            elif choice == "3":
                phones_input = input("Enter phone numbers (comma-separated): ").strip()
                phones = [p.strip() for p in phones_input.split(",")]
                message = input("Enter message: ").strip()
                results = self.send_to_multiple_contacts(phones, message)
                print(f"Sent to {sum(results.values())}/{len(phones)} contacts")
                
            elif choice == "4":
                phone = input("Enter phone number: ").strip()
                message = input("Enter message: ").strip()
                file_path = input("Enter file path: ").strip()
                self.send_with_attachment(phone, message, file_path)
                
            elif choice == "5":
                name = input("Enter contact name: ").strip()
                phone = input("Enter phone number: ").strip()
                group = input("Enter group (default: general): ").strip() or "general"
                self.add_contact(name, phone, group)
                
            elif choice == "6":
                group = input("Enter group name: ").strip()
                message = input("Enter message: ").strip()
                results = self.broadcast_to_group(group, message)
                print(f"Broadcasted to {len(results)} contacts in group '{group}'")
                
            elif choice == "7":
                phone = input("Enter phone number for status: ").strip()
                self.send_bot_status(phone)
                
            elif choice == "8":
                print(f"\n📊 Bot Statistics:")
                print(f"Total Contacts: {self.get_contact_count()}")
                print(f"Messages Sent Today: {self.get_today_message_count()}")
                print(f"Scheduled Tasks: {len(self.scheduled_tasks)}")
                
            elif choice == "9":
                status = self.check_github_status()
                print(f"\n{status}")
                
            elif choice == "10":
                print("Goodbye! 👋")
                break
                
            else:
                print("Invalid option!")

# Example usage and demonstration
def main():
    """Main function to run the bot"""
    bot = SkyWhatsAppBot()
    
    print("\n" + "=" * 50)
    print("INITIALIZING SKY WHATSAPP BOT")
    print("=" * 50)
    
    # Example: Send welcome message to yourself
    print("\nSending test message to yourself...")
    bot.send_instant_message(bot.your_number, f"🤖 Sky Bot Activated!\nGitHub: {bot.github_url}\nTime: {datetime.now().strftime('%H:%M:%S')}")
    
    # Start interactive menu
    bot.menu()

if __name__ == "__main__":
    # Check requirements
    try:
        import pywhatkit
        import schedule
        print("✓ All dependencies are installed")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nInstall missing packages:")
        print("pip install pywhatkit schedule requests pandas")
        exit(1)
    
    main()
