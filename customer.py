from bank_ import BankAccount
from database import Database

class Customer(BankAccount):

    def __init__(self, json_file):
        self.db = Database(json_file)  
        super().__init__(json_file)

    def is_valid_dob(self, dob):
        pass
    
    def _is_valid_dob(self, dob):
        if len(dob) != 10 or dob[2] != "/" or dob[5] != "/":
            return False
        return True

    def create_account(self):
        while True:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")

            if self.db.is_duplicate(first_name, last_name):
                print("Name already exists. Please try again.")
                continue

            break

        while True:
            dob = input("Enter DOB (DD/MM/YYYY): ")
            if not self._is_valid_dob(dob):
                print("Invalid format. Try again.")
                continue
            break

        while True:
            email = input("Enter your email (example@example.com): ")
            if "@" not in email:
                print("Invalid email. Please include '@' in the email address.")
                continue
            break
            
        pin = input("Enter 4-digit PIN: ")
        while len(pin) != 4 or not pin.isdigit():
            print("Invalid PIN. Try again.")
            pin = input("Re-enter PIN: ")

        account_number = self.generate_account_number()

        user = {
            "first_name": first_name,
            "last_name": last_name,
            "dob": dob,
            "account_number": account_number,
            "pin": pin,
            "balance": 0,
            "email": email
        }

        self.db.add_user(user)

        print("Account created!")
        print("Account Number:", account_number)

    def reset_pin(self, user):
        while True:
            print("Reset PIN")

            print("Choose a reset method:")
            print("1. Reset via Email")
            print("2. Reset via Date of Birth")

            reset_option = input("Enter your choice (1/2): ")

            if reset_option == "1":
                email = input("Enter your email (example@example.com): ")
                if str(email) != str(user["email"]):
                    print("Incorrect email")
                    return
            elif reset_option == "2":
                dob = input("Enter DOB (DD/MM/YYYY): ")
                if dob != user["dob"]:
                    print("Incorrect DOB")
                    return
            else:
                print("Invalid choice")
                return

            confirm = input("Confirm reset (yes/no): ")
            if confirm.lower() != "yes":
                return 

            new_pin = input("New 4-digit PIN: ")
            while len(new_pin) != 4 or not new_pin.isdigit():
                print("Invalid PIN")
                new_pin = input("Re-enter PIN: ") 

            user["pin"] = new_pin
            self.db.save_data()

            print("Reset successful!")
            
            choice = input("Do you want to perform another reset? (yes/no): ")
            if choice.lower() != "yes":
                print("Returning to the main menu.")
                break
        
    
    def transfer(self, sender):
        while True:
            recipient_account_number = input("Enter recipient's account number: ")
            recipient_account_number = int(recipient_account_number)
            recipient = self.db.find_user_by_account_number(recipient_account_number)
            amount = float(input("Enter the amount to transfer: $"))
            
            if not recipient:
                print("Recipient account not found.")
                continue
            print(f"Transfer {amount} from {sender['first_name']} {sender['last_name']} to {recipient['first_name']} {recipient['last_name']}?")
            confirm = input("Confirm details? (yes/no): ")
            if confirm.lower() != "yes":
                return

            if amount > sender["balance"]:
                print("Insufficient balance!")
                return

            sender_pin = input("Enter your PIN to confirm: ")
            if sender_pin != sender["pin"]:
                print("Incorrect PIN!")
                return

            sender["balance"] -= amount
            recipient["balance"] += amount
            self.db.save_data()

            print("Transfer successful!")
            
            choice = input("Do you want to perform another transaction? (yes/no): ")
            if choice.lower() != "yes":
                break

                
        
    def main(self):
        print("Welcome to the customer portal!")


        while True:
            print("1. Create Account")
            print("2. Login")
            print("3. Reset Pin")
            print("4. Quit")

            option = input("Select option: ")
            if option == "1":
                self.create_account()
            elif option == "2":
                account_number = input("Enter account number: ")
                pin = input("Enter 4-digit PIN: ")
                user = self.authenticate(account_number, pin)
                

                if user:
                    print(f"Welcome {user['first_name']} {user['last_name']}!")
                else:
                    print("Invalid credentials. Please try again.")
                    continue
                while True:
                    print("Main Menu:")
                    print("1. Check Balance")
                    print("2. Transfer")
                    print("3. Reset PIN")
                    print("4. Account Info")
                    print("5. Logout")

                    option = input("Select option: ")

                    if option == "1":
                        self._check_balance(user)

                    elif option == "2":
                        
                        self.transfer(user)
                        

                    elif option == "3":
                        self.reset_pin(user)

                    elif option == "4":
                        self.view_account_info(user)

                    elif option == "5":
                        print("Logged out!")
                        break

                    else:
                        print("Invalid option selected")
            

            elif option == "3":
                self.reset_pin(user)

            elif option == "4":
                print("Thank you for using our bank App")
                break

            else:
                print("Invalid Option Selected ")
    