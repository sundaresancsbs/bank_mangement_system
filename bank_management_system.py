import tkinter as tk
from tkinter import messagebox
import pickle
import pathlib

class Account:
    def __init__(self, accNo=0, name='', deposit=0, type=''):
        self.accNo = accNo
        self.name = name
        self.deposit = deposit
        self.type = type

    def createAccount(self, accNo, name, type, deposit):
        self.accNo = accNo
        self.name = name
        self.type = type
        self.deposit = deposit

    def modifyAccount(self, name, type, deposit):
        self.name = name
        self.type = type
        self.deposit = deposit
#we have to deposit the amount using this button
    
    def depositAmount(self, amount):
        self.deposit += amount

    def withdrawAmount(self, amount):
        self.deposit -= amount

    def report(self):
        return f"{self.accNo} - {self.name} - {self.type} - ${self.deposit}"

def writeAccountsFile(accounts):
    try:
        with open('accounts.data', 'wb') as outfile:
            pickle.dump(accounts, outfile)
    except Exception as e:
        print(f"Error in writeAccountsFile: {e}")

def create_account():
    try:
        accNo = int(entry_accNo.get())
        name = entry_name.get()
        type = entry_type.get().upper()
        deposit = int(entry_deposit.get())
        if type not in ['C', 'S']:
            raise ValueError("Account type must be 'C' or 'S'")
        account = Account(accNo, name, type, deposit)
        accounts = read_accounts_file()
        accounts.append(account)
        writeAccountsFile(accounts)
        messagebox.showinfo("Info", "Your account is created successfully")
        display_account_details(account)
        reset_inputs()
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", "An error occurred while creating the account.")
        print(f"Error in create_account: {e}")

def read_accounts_file():
    try:
        file = pathlib.Path("accounts.data")
        if file.exists():
            with open('accounts.data', 'rb') as infile:
                return pickle.load(infile)
        else:
            return []
    except Exception as e:
        print(f"Error in read_accounts_file: {e}")
        return []

def display_account_details(account):
    details_window = tk.Toplevel(root)
    details_window.title("Account Details")
    tk.Label(details_window, text=f"Account Number: {account.accNo}").pack()
    tk.Label(details_window, text=f"Name: {account.name}").pack()
    tk.Label(details_window, text=f"Type: {account.type}").pack()
    tk.Label(details_window, text=f"Deposit: ${account.deposit}").pack()

def list_accounts():
    accounts_window = tk.Toplevel(root)
    accounts_window.title("All Accounts")
    try:
        accounts = read_accounts_file()
        if accounts:
            for account in accounts:
                tk.Label(accounts_window, text=f"{account.accNo} - {account.name} - {account.type} - ${account.deposit}").pack()
        else:
            tk.Label(accounts_window, text="No records to display").pack()
    except Exception as e:
        messagebox.showerror("Error", "An error occurred while listing the accounts.")
        print(f"Error in list_accounts: {e}")

def reset_inputs():
    entry_accNo.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_type.delete(0, tk.END)
    entry_deposit.delete(0, tk.END)

def modify_account():
    try:
        accNo = int(entry_accNo.get())
        accounts = read_accounts_file()
        for account in accounts:
            if account.accNo == accNo:
                account.name = entry_name.get()
                account.type = entry_type.get().upper()
                account.deposit = int(entry_deposit.get())
                display_account_details(account)
                break
        else:
            raise ValueError("Account not found")
        
        writeAccountsFile(accounts)
        messagebox.showinfo("Info", "Account Modified Successfully")
        reset_inputs()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

    except Exception as e:
        messagebox.showerror("Error", "An error occurred while modifying the account.")
        print(f"Error in modify_account: {e}")

def delete_account():
    try:
        accNo = int(entry_accNo.get())
        accounts = read_accounts_file()
        accounts = [account for account in accounts if account.accNo != accNo]
        writeAccountsFile(accounts)
        messagebox.showinfo("Info", "Account Deleted Successfully")
        reset_inputs()

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid account number")

    except Exception as e:
        messagebox.showerror("Error", "An error occurred while deleting the account.")
        print(f"Error in delete_account: {e}")

def deposit_amount():
    try:
        accNo = int(entry_accNo.get())
        amount = int(entry_deposit.get())
        accounts = read_accounts_file()
        for account in accounts:
            if account.accNo == accNo:
                account.depositAmount(amount)
                display_account_details(account)
                break
        else:
            raise ValueError("Account not found")
        
        writeAccountsFile(accounts)
        messagebox.showinfo("Info", "Amount Deposited Successfully")
        reset_inputs()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

    except Exception as e:
        messagebox.showerror("Error", "An error occurred while depositing the amount.")
        print(f"Error in deposit_amount: {e}")

def withdraw_amount():
    try:
        accNo = int(entry_accNo.get())
        amount = int(entry_deposit.get())
        accounts = read_accounts_file()
        for account in accounts:
            if account.accNo == accNo:
                if amount <= account.deposit:
                    account.withdrawAmount(amount)
                    display_account_details(account)
                else:
                    messagebox.showerror("Error", "Insufficient funds")
                    return
                break
        else:
            raise ValueError("Account not found")
        
        writeAccountsFile(accounts)
        messagebox.showinfo("Info", "Amount Withdrawn Successfully")
        reset_inputs()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

    except Exception as e:
        messagebox.showerror("Error", "An error occurred while withdrawing the amount.")
        print(f"Error in withdraw_amount: {e}")

root = tk.Tk()
root.title("Bank Management System")
root.geometry('900x600')
root.config(background='#fff')

tk.Label(root, text="Account Number:").grid(row=0, column=0, padx=10, pady=5)
entry_accNo = tk.Entry(root)
entry_accNo.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Account Holder Name:").grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Account Type (C/S):").grid(row=2, column=0, padx=10, pady=5)
entry_type = tk.Entry(root)
entry_type.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Amount:").grid(row=3, column=0, padx=10, pady=5)
entry_deposit = tk.Entry(root)
entry_deposit.grid(row=3, column=1, padx=10, pady=5)

createBtn = tk.Button(root, text='Create Account', command=create_account, bg='#019267', fg='white', height=1, width=20)
createBtn.grid(row=4, column=1, pady=5)

modifyBtn = tk.Button(root, text='Modify Account', command=modify_account, bg='#0172D6', fg='white', height=1, width=20)
modifyBtn.grid(row=5, column=1, pady=5)

deleteBtn = tk.Button(root, text='Delete Account', command=delete_account, bg='#FF597B', fg='white', height=1, width=20)
deleteBtn.grid(row=6, column=1, pady=5)

depositBtn = tk.Button(root, text='Deposit Amount', command=deposit_amount, bg='#019267', fg='white', height=1, width=20)
depositBtn.grid(row=7, column=1, pady=5)

withdrawBtn = tk.Button(root, text='Withdraw Amount', command=withdraw_amount, bg='#FF597B', fg='white', height=1, width=20)
withdrawBtn.grid(row=8, column=1, pady=5)

listBtn = tk.Button(root, text='List All Accounts', command=list_accounts, bg='#0172D6', fg='white', height=1, width=20)
listBtn.grid(row=9, column=1, pady=5)

root.mainloop()
