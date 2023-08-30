from bank_ import BankAccount
from database import Database

class AgentApp(BankAccount):
    def __init__(self, json_file):
        self.db = Database(json_file)  
        super().__init__(json_file)

    def is_valid_dob(self, dob):
        pass

    def reset_pin(self, user):
        pass

    def _is_valid_dob(self, dob):
            pass
        
    def view_account_info(self, user):
        pass
    
    def transfer(self, user):
        pass
    
    def reset_agent_pin(self):
        while True:
            email = input("Enter your email for verification: ")
            
            agent = self.db.find_agent_by_email(email)
            if not agent:
                print("Agent not found.")
                continue

            confirm = input("Confirm reset (yes/no): ")
            if confirm.lower() != "yes":
                continue

            new_pin = input("New PIN: ")
            while len(new_pin) != 4 or not new_pin.isdigit():
                print("Invalid PIN")
                new_pin = input("Re-enter PIN: ")

            agent["pin"] = new_pin
            self.db.save_data()

            print("Reset successful!")
            break
            
    def reset_customer_pin(self):
        account_number = input("Enter Customer's Account number: ")
        account_number = int(account_number)
        customer = self.db.find_user_by_account_number(account_number)
        if customer:
            print("\nCustomer:")
            print("Name:", customer["first_name"], customer["last_name"])
        
            confirm_customer = input("Confirm Customer? (yes/no): ")
            if confirm_customer.lower() != "yes":
                print("Reset canceled.")
                return
            else:
                self._reset_pin_to_default(customer) 
                self.db.save_data()
            print("Customer's PIN reset successful!")
        else:
            print("Customer not found.")
            
        
        
        
    def perform_transaction(self):
        print("\nPerform Transaction:")
        while True:
            sender_account = input("Enter Sender's Account Number: ")
            sender_account = int(sender_account)
            sender = self.db.find_user_by_account_number(sender_account)
            
            if not sender:
                print("Sender not found, please try again.")
                continue
            
            print("\nSender:")
            print("Name:", sender["first_name"], sender["last_name"])
            
            confirm_sender = input("Confirm sender? (yes/no): ")
            if confirm_sender.lower() != "yes":
                print("Transaction canceled.")
                return
            
            while True:
                recipient_account = input("Enter Recipient's Account Number: ")
                recipient_account = int(recipient_account)
                recipient = self.db.find_user_by_account_number(recipient_account)
                
                if not recipient:
                    print("Recipient not found, please try again.")
                    continue
            
                print("\nRecipient:")
                print("Name:", recipient["first_name"], recipient["last_name"])
                
                confirm_recipient = input("Confirm recipient? (yes/no): ")
                if confirm_recipient.lower() != "yes":
                    print("Transaction canceled.")
                    return
                
                amount = float(input("Enter Amount: "))
                
                if sender["balance"] >= amount:
                    sender["balance"] -= amount
                    recipient["balance"] += amount
                    self.db.save_data()
                    print("Transaction successful!")
                else:
                    print("Insufficient balance.")
                    
                choice = input("Do you want to perform another transaction? (yes/no): ")
                if choice.lower() != "yes":
                    return

    @staticmethod
    def _reset_pin_to_default(user):
        user["pin"] = "0000"
    
    
    def fund_customer_account(self):
        print("\nFund Customer Account:")
        while True:
            account_number = input("Enter Customer's Account Number: ")
            account_number = int(account_number)
            amount = float(input("Enter Amount: "))

            customer = self.db.find_user_by_account_number(account_number)

            if customer:
                print("\nCustomer:")
                print("Name:", customer["first_name"], customer["last_name"])
            
                confirm_sender = input("Confirm sender? (yes/no): ")
                if confirm_sender.lower() != "yes":
                    print("Transaction canceled.")
                    return

                customer["balance"] += amount
                self.db.save_data()
                print("Funds added to customer's account.")
                
            else:
                print("Customer not found. Please enter valid account details.")
                
            choice = input("Do you want to perform another transaction? (yes/no): ")
            if choice.lower() != "yes":
                break


    def delete_customer_account(self):
        account_number = input("Enter customer's account number to delete: ")
        account_number = int(account_number)
        customer = self.db.find_user_by_account_number(account_number)
        if customer:
            print("Customer found:")
            print("Name:", customer["first_name"], customer["last_name"])
            confirm = input("Are you sure you want to delete this account? (yes/no): ")
            if confirm.lower() == "yes":
                self.db.users.remove(customer)
                self.db.save_data()
                print("Account deleted.")
        else:
            print("Customer not found.")
            
            
        choice = input("Do you want to check another account? (yes/no): ")
        if choice.lower() == "yes":
            self.delete_customer_account()       

    def view_customer_details(self):
        print("\nView Customer Details:")
        account_number = input("Enter Customer's Account Number: ")
        account_number = int(account_number)
        customer = self.db.find_user_by_account_number(account_number)

        if customer:
            print("\nCustomer Details:")
            print("Name:", customer["first_name"], customer["last_name"])
            print("Email:", customer["email"])
            print("Balance: $" + str(customer["balance"]) + "\n")
            
        else:
            print("Customer not found.")
            
        
            
    def create_agent_account(self):
        print("\nCreate Agent Account:")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email (example@bank.com): ")
        pin = input("Enter 4-digit PIN: ")

        if not email.endswith('@bank.com'):
            print("Invalid email format. Email must end with @bank.com.")
            return

        user = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "pin": pin,
        }

        self.db.add_agent(user)

        print("Agent account created successfully!")

    def main(self):
        while True:
            print("\nAgent App Main Menu:")
            print("1. Create Account")
            print("2. Login")
            print("3. Reset PIN")
            print("4. Quit")

            option = input("Enter your choice (1-4): ")

            if option == "1":
                self.create_agent_account()
            elif option == "2":
                email = input("Enter Email (example@bank.com): ")
                agent = self.db.find_agent_by_email(email)
                pin = input("Enter 4-digit PIN: ")
                
                if agent and agent["pin"] == pin:
                    print("Login successful!")
                else:
                    print("Invalid Login.")
                    continue
                    
                print(f"Welcome {agent['first_name']} {agent['last_name']}!")

                while True:
                    print("\nWelcome to the Agent App Menu:")
                    print("1. Reset Customer PIN")
                    print("2. View Customer Details")
                    print("3. Fund Customer Account")
                    print("4. Perform Transaction")
                    print("5. Delete Customer Account")
                    print("6. Logout")

                    option = input("Enter your choice (1-6): ")

                    if option == "1":
                        self.reset_customer_pin()
                    elif option == "2":
                        self.view_customer_details()
                        
                    elif option == "3":
                        self.fund_customer_account()
                    elif option == "4":
                        self.perform_transaction()
                    elif option == "5":
                        self.delete_customer_account()
                    elif option == "6":
                        print("Agent logged out.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        
            elif option == "3":
                self.reset_agent_pin()
            elif option == "4":
                self.db.save_data()
                print("Thank you for using the Agent App. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
