import json

class Database():

    def __init__(self, json_file):
        self.json_file = json_file
        self.users = []
        self.Agents =[]
        self.load_data()

    def load_data(self):       
        try:
            with open(self.json_file) as f:
                data = json.load(f)
                self.users = data.get('users', [])
                self.Agents = data.get('Agents', [])
        except FileNotFoundError:
            print("File not found, creating new file")
            data = {'users': [], 'Agents': []}
            with open(self.json_file, 'w') as f:
                json.dump(data, f, indent=2)
            self.users = []
            self.Agents = []


    def save_data(self):
        data = {
            "users": self.users,
            "Agents": self.Agents
            }
        with open(self.json_file, 'w') as f:  
            json.dump(data, f, indent=2)
            

    def find_user_by_account_number(self, account_number):
        for user in self.users:
            if user["account_number"] == account_number:
                return user
        return None

    def find_user_by_email(self, email):
        for user in self.users:
            if user["email"] == email:
                return user
        return None
    
    def find_agent_by_email(self, email):
        for user in self.Agents:
            if user["email"] == email:
                return user
        return None

    def add_user(self, user):
        self.users.append(user)
        self.save_data()
        
    def add_agent(self, user):
        self.Agents.append(user)
        self.save_data()
    

    def is_duplicate(self, fname, lname):
            for user in self.users:
                if user["first_name"] == fname and user["last_name"] == lname:
                    return True
            return False
