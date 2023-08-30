from abc import ABC, abstractmethod
from database import Database
import random

class BankAccount(ABC):

    def __init__(self, json_file):
        self.json_file = json_file
        self.db = Database(json_file)

    @abstractmethod
    def reset_pin(self, user):
        pass

    @abstractmethod   
    def view_account_info(self, user):
        pass

    @abstractmethod
    def main(self):
        pass

    def view_account_info(self, user):
            print("\nAccount Information:")
            print("Name:", user["first_name"], user["last_name"])
            print("Account Number:", user["account_number"])
            print("email:", user["email"])
            print("Balance: $" + str(user["balance"]) + "\n" )
            
    
    
    def authenticate(self, account_number, pin):
        self.db.load_data()
        account_number = int(account_number)

        for user in self.db.users:
            if user["account_number"] == account_number:
                if user["pin"] == pin:
                    return user
                else:
                    print("Incorrect PIN")
                    return None

    def generate_account_number(self):
        while True:
            account_number = random.randint(1000000000, 9999999999)
            if not self._is_duplicate_account(account_number):
                return account_number

    def _is_duplicate_account(self, account_number):
        for user in self.db.users:
            if user["account_number"] == account_number:
                return True
        return False
    
    def get_user(self, account_number):
        account_number = int(account_number)
        for user in self.db.users:
            if user["account_number"] == account_number:
                return user
        return None

    def _check_balance(self, user):
        print("\nBalance:")
        print(user["first_name"], user["last_name"])
        print("$" + str(user["balance"]))
        
    def is_valid_dob(self, dob):
        if len(dob) != 10 or dob[2] != "/" or dob[5] != "/":
            return False
        return True


    @abstractmethod
    def transfer(self, sender, recipient, amount):
        pass

    