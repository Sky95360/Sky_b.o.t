"""
Simpler WhatsApp Bot for Pydroid 3 - No SQLite needed
"""

import json
import os
from datetime import datetime
import time

class SimpleWhatsAppBot:
    def __init__(self):
        self.your_number = "0748529340"
        self.country_code = "27"
        self.github_url = "https://github.com/Sky95360/Sky_b.o.t"
        
        # Files for storage
        self.contacts_file = "contacts.txt"
        self.messages_file = "messages.txt"
        
        print("=" * 50)
        print("🤖 SIMPLE WHATSAPP BOT")
        print("=" * 50)
        print(f"Your Number: {self.your_number}")
        print(f"GitHub: {self.github_url}")
        print("=" * 50)
    
    def save_contact(self, name, phone):
        """Save contact to file"""
        with open(self.contacts_file, "a") as f:
            f.write(f"{name}|{phone}|{datetime.now()}\n")
        print(f"✅ Contact saved: {name}")
    
    def show_contacts(self):
        """Show all contacts"""
        if not os.path.exists(self.contacts_file):
            print("📭 No contacts yet")
            return
        
        with open(self.contacts_file, "r") as f:
            contacts = f.readlines()
        
        print("📒 CONTACTS:")
        print("=" * 40)
        for i, contact in enumerate(contacts, 1):
            name, phone, date = contact.strip().split("|")
            print(f"{i}. {name}")
            print(f"   📞 {phone}")
            print(f"   📅 {date[:10]}")
            print("-" * 30)
    
    def create_message(self):
        """Create and save a message"""
        print("\n📝 CREATE MESSAGE")
        print("=" * 40)
        
        phone = input("Enter phone number: ").strip()
        message = input("Enter your message: ").strip()
        
        print(f"\n📤 READY TO SEND:")
        print(f"To: {phone}")
        print(f"Message: {message}")
        print("\n📱 INSTRUCTIONS:")
        print("1. Open WhatsApp on your phone")
        print(f"2. Send to: {phone}")
        print(f"3. Copy this message: {message}")
        print("=" * 40)
        
        # Save to file
        with open(self.messages_file, "a") as f:
            f.write(f"{datetime.now()}|{phone}|{message}\n")
        
        input("\nPress Enter to continue...")
    
    def broadcast_message(self):
        """Send same message to multiple contacts"""
        print("\n📢 BROADCAST MESSAGE")
        print("=" * 40)
        
        message = input("Enter broadcast message: ").strip()
        
        if not os.path.exists(self.contacts_file):
            print("❌ No contacts to broadcast to")
            return
        
        with open(self.contacts_file, "r") as f:
            contacts = f.readlines()
        
        print(f"\n📤 Broadcasting to {len(contacts)} contacts...")
        print("=" * 40)
        
        for contact in contacts:
            name, phone, _ = contact.strip().split("|")
            print(f"\nTo: {name} ({phone})")
            print(f"Message: {message}")
            print("-" * 30)
            time.sleep(0.5)
        
        print(f"\n✅ Broadcast ready for {len(contacts)} contacts")
        print("\n📱 INSTRUCTIONS:")
        print("1. Open WhatsApp on your phone")
        print("2. Send individually to each contact")
        print(f"3. Message: {message}")
        print("=" * 40)
        
        input("\nPress Enter to continue...")
    
    def show_stats(self):
        """Show statistics"""
        contact_count = 0
        if os.path.exists(self.contacts_file):
            with open(self.contacts_file, "r") as f:
                contact_count = len(f.readlines())
        
        message_count = 0
        if os.path.exists(self.messages_file):
            with open(self.messages_file, "r") as f:
                message_count = len(f.readlines())
        
        print("\n📊 STATISTICS")
        print("=" * 40)
        print(f"📞 Contacts: {contact_count}")
        print(f"📨 Messages Created: {message_count}")
        print(f"🤖 Bot Number: {self.your_number}")
        print(f"🔗 GitHub: {self.github_url}")
        print("=" * 40)
    
    def show_menu(self):
        """Show main menu"""
        while True:
            print("\n" + "=" * 40)
            print("🤖 WHATSAPP BOT MENU")
            print("=" * 40)
            print("1. 📞 Add New Contact")
            print("2. 📤 Create Message")
            print("3. 📢 Broadcast Message")
            print("4. 📒 View Contacts")
            print("5. 📊 View Statistics")
            print("6. 🆘 Help")
            print("0. ❌ Exit")
            print("=" * 40)
            
            choice = input("Choose (0-6): ").strip()
            
            if choice == "1":
                print("\n" + "=" * 40)
                print("ADD CONTACT")
                print("=" * 40)
                name = input("Enter name: ").strip()
                phone = input("Enter phone: ").strip()
                self.save_contact(name, phone)
            
            elif choice == "2":
                self.create_message()
            
            elif choice == "3":
                self.broadcast_message()
            
            elif choice == "4":
                self.show_contacts()
            
            elif choice == "5":
                self.show_stats()
            
            elif choice == "6":
                print("\n" + "=" * 40)
                print("HELP")
                print("=" * 40)
                print("This bot helps you manage WhatsApp messages.")
                print("It stores contacts and messages in files.")
                print("You need to send messages manually in WhatsApp.")
                print("=" * 40)
                input("\nPress Enter to continue...")
            
            elif choice == "0":
                print("\n👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice!")

# Run the bot
if __name__ == "__main__":
    bot = SimpleWhatsAppBot()
    bot.show_menu()
