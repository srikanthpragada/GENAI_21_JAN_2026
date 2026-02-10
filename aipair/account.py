# Create Account class to store details of Savings Account 
# Details are acno, customer, balance 
# Create methods to deposit, withdraw and display details of the account and get balance 

class Account:
    def __init__(self, acno, customer, balance):
        self.acno = acno
        self.customer = customer
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance is {self.balance}.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance is {self.balance}.")

    def display_details(self):
        print(f"Account Number: {self.acno}")
        print(f"Customer Name: {self.customer}")
        print(f"Balance: {self.balance}")

    def get_balance(self):
        return self.balance
    

a = Account(12345, "John Doe", 1000)
print(a.get_balance())

