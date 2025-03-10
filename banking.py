import csv
import os

FILE_NAME = "bank.csv"

def create_customer_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings"])
            print("Customer data file created")

def generate_account_id():
    max_id = 10000  
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader) 
            for row in reader:
                if len(row) > 0 and row[0].isdigit():
                    max_id = max(max_id, int(row[0]))  
    except (FileNotFoundError, ValueError):
        pass  
    return str(max_id + 1)

class Add_new_customer:
    def __init__(self, first_name, last_name, password, balance_checking=0.0, balance_savings=0.0):
        self.account_id = generate_account_id() 
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = float(balance_checking)
        self.balance_savings = float(balance_savings)
    
    def save_to_csv(self):
        with open(FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([self.account_id, self.first_name, self.last_name, self.password, self.balance_checking, self.balance_savings])

class Login:
    def __init__(self):
        self.logged_in_user = None  

    def authenticate(self, account_id, password):
        with open(FILE_NAME, mode='r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                if row["account_id"] == account_id and row["password"] == password:
                    self.logged_in_user = row  
                    return True  
        return False  

class Withdraw:
    def __init__(self, account_id, password, amount, account_type="checking"):
        self.account_id = account_id
        self.password = password
        self.amount = float(amount)
        self.account_type = account_type
        self.process_withdrawal()

    def process_withdrawal(self):
        accounts = []
        found = False
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file, delimiter=';')
            accounts = list(reader)
        
        for row in accounts[1:]:
            if row[0] == self.account_id and row[3] == self.password:
                balance_index = 4 if self.account_type == "checking" else 5
                current_balance = float(row[balance_index])
                if 0 < self.amount <= current_balance:
                    row[balance_index] = str(current_balance - self.amount)
                    found = True
                    print(f"Withdrawal successful! New {self.account_type} balance: {row[balance_index]}")
                else:
                    print("Insufficient balance or invalid amount!")
        
        if found:
            with open(FILE_NAME, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(accounts)
        else:
            print("Account not found or incorrect password!")

class Deposit:
    def __init__(self, account_id, password, amount, account_type="checking"):
        self.account_id = account_id
        self.password = password
        self.amount = float(amount)
        self.account_type = account_type
        self.process_deposit()

    def process_deposit(self):
        accounts = []
        found = False
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file, delimiter=';')
            accounts = list(reader)
        
        for row in accounts[1:]:
            if row[0] == self.account_id and row[3] == self.password:
                balance_index = 4 if self.account_type == "checking" else 5
                row[balance_index] = str(float(row[balance_index]) + self.amount)
                found = True
                print(f"Deposit successful! New {self.account_type} balance: {row[balance_index]}")
        
        if found:
            with open(FILE_NAME, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(accounts)
        else:
            print("Account not found or incorrect password!")

class Transfer:
    def __init__(self, from_account, password, to_account, amount, from_account_type="checking"):
        self.from_account = from_account
        self.password = password
        self.to_account = to_account
        self.amount = float(amount)
        self.from_account_type = from_account_type
        self.process_transfer()

    def process_transfer(self):
        accounts = []
        found = False
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file, delimiter=';')
            accounts = list(reader)
        
        from_index = None
        to_index = None
        
        for row in accounts[1:]:
            if row[0] == self.from_account and row[3] == self.password:
                from_index = 4 if self.from_account_type == "checking" else 5
                current_balance = float(row[from_index])
                if self.amount > 0 and current_balance >= self.amount:
                    row[from_index] = str(current_balance - self.amount)
                    found = True
                else:
                    print("Insufficient balance or invalid amount!")
            if row[0] == self.to_account:
                to_index = 4 
                row[to_index] = str(float(row[to_index]) + self.amount)
        
        if found:
            with open(FILE_NAME, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(accounts)
            print(f"Transfer successful! {self.amount} transferred from {self.from_account} to {self.to_account}.")
        else:
            print("Transfer failed! Check your credentials and balance.")

create_customer_file()

is_running = True
while is_running:
    print("\n===== Welcome to the Bank App =====")
    print("1. Register New Account")
    print("2. Withdraw")
    print("3. Deposit")
    print("4. Transfer Money")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':  
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        password = input("Enter your password: ")
        balance_checking = input("Enter your checking account balance (default 0): ") or 0.0
        balance_savings = input("Enter your savings account balance (default 0): ") or 0.0
        new_customer = Add_new_customer(first_name, last_name, password, balance_checking, balance_savings)
        new_customer.save_to_csv()
        print(f"Account for {first_name} {last_name} has been created.")
    
    elif choice == '2':  
        account_id = input("Enter your account ID: ")
        password = input("Enter your password: ")
        amount = float(input("Enter amount to withdraw: "))
        account_type = input("Withdraw from (checking/savings): ").strip().lower()
        Withdraw(account_id, password, amount, account_type)
    
    elif choice == '3':  
        account_id = input("Enter your account ID: ")
        password = input("Enter your password: ")
        amount = float(input("Enter amount to deposit: "))
        account_type = input("Deposit into (checking/savings): ").strip().lower()
        Deposit(account_id, password, amount, account_type)
    
    elif choice == '4':  
        account_id = input("Enter your account ID: ")
        password = input("Enter your password: ")
        to_account = input("Enter recipient's account ID: ")
        amount = float(input("Enter amount to transfer: "))
        account_type = input("Transfer from (checking/savings): ").strip().lower()
        Transfer(account_id, password, to_account, amount, account_type)
    
    elif choice == '5':  
        is_running = False
        print("Thank you for using the Bank App!")

