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
    def __init__(self, account_id, password):
        self.account_id = account_id
        self.password = password
        self.first_name = None
        self.last_name = None
        self.balance_checking = 0.0
        self.balance_savings = 0.0

    def load_customer_info(self):
        if not os.path.exists(FILE_NAME):
            print("Customer file not found!")
            return False

        try:
            with open(FILE_NAME, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=";")

                found = False 
                
                for row in reader:
                    print(f" Checking: {row}")  

                    if "account_id" not in row or "password" not in row:
                        print("⚠️ ملف CSV لا يحتوي على الأعمدة الصحيحة!")
                        return False
                    
                    if row["account_id"].strip() == self.account_id.strip() and row["password"].strip() == self.password.strip():
                        self.first_name = row["first_name"]
                        self.last_name = row["last_name"]
                        self.balance_checking = float(row["balance_checking"])
                        self.balance_savings = float(row["balance_savings"])
                        found = True
                        break  
                if found:
                    print(f"Welcome {self.first_name} {self.last_name}!")
                    return True
                else:
                    print(" The account does not exist, or the password is incorrect.")
                    return False

        except Exception as e:
            print(f" Error reading the file: {e}")
            return False

# هناا
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
        overdraft_fee = 35  
        overdraft_limit = -100  

        with open(FILE_NAME, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            accounts = list(reader)

        for i, row in enumerate(accounts[1:]): 
            if len(row) < 5: 
                print(f"Warning: Skipping invalid row {row}")
                continue  

            if row[0] == self.account_id and row[3] == self.password:
                balance_index = 4 if self.account_type == "checking" else 5
                
                try:
                    current_balance = float(row[balance_index])  
                except ValueError:
                    print(f"Error: Invalid balance value in row {row}. Skipping transaction.")
                    return

                while len(row) < 7:
                    row.append("0")  
                
                overdraft_count = int(row[6])  
                account_status = row[7] if len(row) > 7 else "active"  

                if account_status == "deactivated":
                    print("Your account has been deactivated due to excessive overdrafts.")
                    return 
                
                new_balance = current_balance - self.amount
                
                if new_balance < 0:
                    if current_balance <= overdraft_limit:
                        print(f"Your account cannot be overdrawn by more than {overdraft_limit} USD.")
                        return
                    else:
                        row[balance_index] = str(new_balance - overdraft_fee)
                        overdraft_count += 1
                        row[6] = str(overdraft_count)  
                        print(f"Overdraft detected! A fee of {overdraft_fee} USD has been deducted.")
                        
                        if overdraft_count >= 2:
                            row[7] = "deactivated"  
                            print("Your account has been deactivated due to excessive overdrafts.")
                            return
                else:
                    row[balance_index] = str(new_balance)
                
                found = True
                print(f"Withdrawal successful! New balance in {self.account_type} account: {row[balance_index]}")
                accounts[i + 1] = row  
                break

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
    print("5. Access My Info")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == '1':  
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        password = input("Enter your password: ")
        balance_checking = float(input("Enter your checking account balance (default 0): ") or 0.0)
        balance_savings = float(input("Enter your savings account balance (default 0): ") or 0.0)
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
        account_id = input("Enter your ID: ")
        password = input("Enter your password: ")

        customer = Login(account_id, password)  

        if customer.load_customer_info():
            print("\n===== Your Bank Information =====")
            print(f" Account ID: {customer.account_id}")
            print(f" Name: {customer.first_name} {customer.last_name}")
            print(f"Checking Account Balance: ${customer.balance_checking}")
            print(f"Savings Account Balance: ${customer.balance_savings}")
        else:
            print("\nThe account does not exist, or the password is incorrect. Please check and try again.")


    elif choice == '6':  
        is_running = False
        print("Thank you for using the Bank App!")  

    else:
        print("Invalid choice! Please enter a number between 1 and 6.")




        




