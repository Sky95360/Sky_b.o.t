"""
SkyBot Pro - WhatsApp Business Assistant
Made for small businesses to get paid
"""

import json
import os
from datetime import datetime

class SkyBotPro:
    def __init__(self):
        self.business_name = "Your Business Name"
        self.whatsapp_number = "0748529340"
        
        # Business features
        self.clients = []
        self.monthly_price = 500  # R500 per month
        self.services = {
            "basic": {
                "price": 500,
                "features": ["Auto-replies", "100 messages/month", "1 admin"]
            },
            "pro": {
                "price": 1500,
                "features": ["Auto-replies", "Unlimited messages", "3 admins", "Analytics"]
            },
            "enterprise": {
                "price": 3000,
                "features": ["Everything in Pro", "Custom integrations", "Priority support"]
            }
        }
        
        print("=" * 60)
        print("🤖 SKYBOT PRO - BUSINESS EDITION")
        print("=" * 60)
        print(f"Business: {self.business_name}")
        print(f"WhatsApp: {self.whatsapp_number}")
        print(f"Monthly Plans: R{self.monthly_price}+")
        print("=" * 60)
    
    def add_client(self, business_name, contact_person, phone, plan="basic"):
        """Add a new business client"""
        client = {
            "id": len(self.clients) + 1,
            "business": business_name,
            "contact": contact_person,
            "phone": phone,
            "plan": plan,
            "price": self.services[plan]["price"],
            "join_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "active"
        }
        
        self.clients.append(client)
        self.save_clients()
        
        print(f"✅ Added client: {business_name}")
        print(f"   Plan: {plan} - R{client['price']}/month")
        print(f"   Contact: {contact_person} ({phone})")
        
        # Generate welcome message for client
        self.generate_welcome_message(client)
    
    def generate_welcome_message(self, client):
        """Generate welcome message for new client"""
        print("\n" + "=" * 60)
        print("📝 WELCOME MESSAGE FOR CLIENT:")
        print("=" * 60)
        message = f"""Hello {client['contact']}! 👋

Welcome to {self.business_name}'s WhatsApp Service!

✅ Your {client['plan']} plan is activated
✅ Price: R{client['price']}/month
✅ Features included:
"""
        
        for feature in self.services[client['plan']]["features"]:
            message += f"   • {feature}\n"
        
        message += f"""
📞 Support: {self.whatsapp_number}
📅 Next billing: 30 days from now

Thank you for choosing us!"""
        
        print(message)
        print("=" * 60)
        print("\n📱 Send this message to your client on WhatsApp!")
    
    def save_clients(self):
        """Save clients to file"""
        with open("clients.json", "w") as f:
            json.dump(self.clients, f, indent=4)
    
    def load_clients(self):
        """Load clients from file"""
        if os.path.exists("clients.json"):
            with open("clients.json", "r") as f:
                self.clients = json.load(f)
    
    def show_clients(self):
        """Show all clients"""
        self.load_clients()
        
        if not self.clients:
            print("📭 No clients yet")
            return
        
        print("\n" + "=" * 60)
        print("📊 CLIENT LIST")
        print("=" * 60)
        
        total_income = 0
        
        for client in self.clients:
            print(f"\n🏢 {client['business']}")
            print(f"   👤 {client['contact']}")
            print(f"   📞 {client['phone']}")
            print(f"   📋 Plan: {client['plan'].upper()}")
            print(f"   💰 R{client['price']}/month")
            print(f"   📅 Joined: {client['join_date']}")
            print(f"   🔄 Status: {client['status']}")
            total_income += client['price']
        
        print("\n" + "=" * 60)
        print(f"💰 TOTAL MONTHLY INCOME: R{total_income}")
        print(f"👥 TOTAL CLIENTS: {len(self.clients)}")
        print("=" * 60)
    
    def calculate_income(self):
        """Calculate potential income"""
        print("\n" + "=" * 60)
        print("💰 INCOME CALCULATOR")
        print("=" * 60)
        
        basic_clients = int(input("How many BASIC clients (R500/month)? ") or "0")
        pro_clients = int(input("How many PRO clients (R1500/month)? ") or "0")
        enterprise_clients = int(input("How many ENTERPRISE clients (R3000/month)? ") or "0")
        
        total_income = (basic_clients * 500) + (pro_clients * 1500) + (enterprise_clients * 3000)
        
        print("\n" + "=" * 60)
        print("📈 INCOME PROJECTION")
        print("=" * 60)
        print(f"Basic clients: {basic_clients} × R500 = R{basic_clients * 500}")
        print(f"Pro clients: {pro_clients} × R1500 = R{pro_clients * 1500}")
        print(f"Enterprise clients: {enterprise_clients} × R3000 = R{enterprise_clients * 3000}")
        print("-" * 40)
        print(f"💰 MONTHLY INCOME: R{total_income}")
        print(f"💰 YEARLY INCOME: R{total_income * 12}")
        print("=" * 60)
    
    def show_services(self):
        """Show available services"""
        print("\n" + "=" * 60)
        print("📋 AVAILABLE SERVICES")
        print("=" * 60)
        
        for plan, details in self.services.items():
            print(f"\n{plan.upper()} PLAN - R{details['price']}/month")
            for feature in details["features"]:
                print(f"   ✓ {feature}")
    
    def sales_pitch(self):
        """Generate sales pitch for clients"""
        print("\n" + "=" * 60)
        print("🎯 SALES PITCH TEMPLATE")
        print("=" * 60)
        
        pitch = f"""Hello! I'm from {self.business_name}. 

We help businesses like yours manage WhatsApp professionally:

✅ Auto-reply to customers 24/7
✅ Send bulk announcements
✅ Organize customer chats
✅ Affordable plans from R500/month

Would you like a FREE demo?"""
        
        print(pitch)
        print("\n" + "=" * 60)
        print("📱 Send this to potential clients!")
        print("=" * 60)
    
    def main_menu(self):
        """Main menu"""
        while True:
            print("\n" + "=" * 40)
            print("🤖 SKYBOT PRO - BUSINESS MENU")
            print("=" * 40)
            print("1. ➕ Add New Client")
            print("2. 👥 View All Clients")
            print("3. 📋 Show Services/Pricing")
            print("4. 💰 Calculate Potential Income")
            print("5. 🎯 Generate Sales Pitch")
            print("6. 📝 Create Client Welcome Message")
            print("7. 📊 View Income Report")
            print("0. ❌ Exit")
            print("=" * 40)
            
            choice = input("Choose (0-7): ").strip()
            
            if choice == "1":
                print("\n" + "=" * 40)
                print("ADD NEW CLIENT")
                print("=" * 40)
                business = input("Business Name: ").strip()
                contact = input("Contact Person: ").strip()
                phone = input("WhatsApp Number: ").strip()
                print("\nAvailable Plans: basic (R500), pro (R1500), enterprise (R3000)")
                plan = input("Choose plan: ").strip().lower() or "basic"
                
                if plan in self.services:
                    self.add_client(business, contact, phone, plan)
                else:
                    print("❌ Invalid plan. Using basic.")
                    self.add_client(business, contact, phone, "basic")
            
            elif choice == "2":
                self.show_clients()
            
            elif choice == "3":
                self.show_services()
            
            elif choice == "4":
                self.calculate_income()
            
            elif choice == "5":
                self.sales_pitch()
            
            elif choice == "6":
                # Create welcome message for existing client
                self.load_clients()
                if self.clients:
                    print("\nSelect client for welcome message:")
                    for i, client in enumerate(self.clients, 1):
                        print(f"{i}. {client['business']}")
                    
                    try:
                        idx = int(input("Client number: ").strip()) - 1
                        if 0 <= idx < len(self.clients):
                            self.generate_welcome_message(self.clients[idx])
                    except:
                        print("❌ Invalid selection")
                else:
                    print("❌ No clients yet")
            
            elif choice == "7":
                self.show_clients()  # Shows income report
            
            elif choice == "0":
                print("\n" + "=" * 40)
                print("💼 Good luck with your business!")
                print(f"📞 Contact: {self.whatsapp_number}")
                print("=" * 40)
                break
            
            else:
                print("❌ Invalid choice!")

# Run the bot
if __name__ == "__main__":
    bot = SkyBotPro()
    bot.main_menu()
