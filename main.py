from agent import AgentApp 
from customer import Customer
from database import Database

if __name__ == "__main__":
    db = Database("data.json")

    while True:
        print("\nBank App Main Menu:")
        print("1. Agent")
        print("2. Customer")
        print("3. Quit")

        option = input("Enter your choice (1-3): ")

        if option == "1":
            agent = AgentApp("data.json") 
            agent.main()

        elif option == "2":
            customer = Customer("data.json")
            customer.main()
            
        elif option == "3":
            print("Thank you for using the Bank App. Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")
