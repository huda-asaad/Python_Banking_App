import csv
import os


FILE_NAME = "bank.csv"

def create_customer_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings", "status"])
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
    def __init__(self, first_name, last_name, password, balance_checking=0.0, balance_savings=0.0, ):
        self.account_id = generate_account_id() 
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = float(balance_checking)
        self.balance_savings = float(balance_savings)
        
          ###  ــــ show the balance ــــــ 
    def balance_checking():
        print(f"Your balance = {balance_checking}")

   
    def save_to_csv(self):
        with open(FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([self.account_id, self.first_name, self.last_name, self.password, self.balance_checking, self.balance_savings, self.status])

   
    @staticmethod
    def find_customer(account_id):
        with open(FILE_NAME, mode='r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                if row["account_id"] == account_id:
                    return Add_new_customer(row["first_name"], row["last_name"], row["password"], row["balance_checking"], row["balance_savings"], row["status"])
        return None
    
  

create_customer_file()  

first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
password = input("Enter password: ")
balance_checking = float(input("Enter initial checking balance: "))
balance_savings = float(input("Enter initial savings balance: "))

new_customer = Add_new_customer(first_name, last_name, password, balance_checking, balance_savings)
new_customer.save_to_csv()

print(f"Account created successfully! Your account ID is {new_customer.account_id}")

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
   def __init__(self, amount, balance):
     if 0 < amount <= balance:
      self.nwe_balance = balance - amount
      print("withdrae successfully")
     else:
        print("the amount must be greater than 0 and less than or equal to the balance")       

account_id = input ("Enter Your ID: ")
password = input ("Enter the password: ")
if account_id == account_id:
 password == password
 print("ENTER successfully")

else:
    print("Enter Number correct")


 
class Deposit:
    def __init__(self, amount):
        self.balance = self.balance + amount
        amount = float(input("venter amount deposit "))

        if amount < 0:
            print(" that is not a valid amount")
        else:
            return amount


is_running = True

while is_running:
   print("Welcome to in the Bank App")
   print("1. Login")
   print("2. show balance. ")
   print("3. show savings account. ")
   print("4. Withdraw. ")
   print("5. Deposit. ")
   print("6.Exit. ")

choice = input ("Enter your choice (1-6): ")
if choice  == '1':
    Login()
    
create_customer_file()  
bank = Add_new_customer()

