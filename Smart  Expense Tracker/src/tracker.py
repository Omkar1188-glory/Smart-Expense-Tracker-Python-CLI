import json
import os
from models import Transaction
from collections import defaultdict
from datetime import datetime
import csv


class Tracker:
    def __init__(self):
        self.transactions = [] # list to store all transactions
        # self.data_file = os.path.join(os.path.dirname(__file__), "data.json")
    
    def add_transaction(self,transaction):
        """"add a new transaction object to the list"""
        self.transactions.append(transaction)
        print(" Transaction added Succesfully!")
    
    def list_transaction(self):
        """"Display all transactions in simple table format"""
        if not self.transactions:
            print("No transaction found yet")
            return
        
        print("\n==All Transactions==")
        for t in self.transactions:
            print(f"ID:{t.id}")
            print(f"Date:{t.date}")
            print(f"Amount:{t.amount}")
            print(f"Type:{t.type}")
            print(f"Category:{t.category}")
            print(f"Description:{t.description}")
            print("-"*30)

        
    def get_summary(self):
        income = sum(t.amount for t in self.transactions if t.type.lower() == "income")
        expense = sum(t.amount for t in self.transactions if t.type.lower() == "expense" )
        balance = income-expense

        by_category = {}
        for t in self.transactions:
                if t.type.lower() == "expense":
                    by_category[t.category] = by_category.get(t.category,0) + t.amount

        return{
                "income": income,
                "expense": expense,
                "balance": balance,
                "by_category":by_category
            }
        

    # Saved data JSON file
    def save_data(self):
        data= [t.to_dict() for t in self.transactions]
        with open("data.json","w")as f:
            json.dump(data,f,indent=4)
        print("Data Saved Succesully")

    # Load Data From Josn file
    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json","r") as f:
                data = json.load(f)
                self.transactions = [Transaction(**t)for t in data]
            print("Data Loaded Succesfully")
        else:
            print("No Previous Data Found. Starting Fresh")

    def find_transaction_by_id(self,trans_id):
        """Find a trasaction object by its ID"""
        for t in self.transactions:
            if t.id == trans_id:
                return t
            print("Transaction Not Found")
            return None
    
    def edit_transaction(self):
        trans_id = input("Enter the transaction id to edit: ")
        transaction = self.find_transaction_by_id(trans_id)

        if transaction:
            print("\n Which field do you want to edit?")
            print("1. Date")
            print("2. Amount")
            print("3. Category")
            print("4. Type")
            print("5. Description")

            choice = int(input("Enter you choice between (1-5): "))

            if choice == 1:
                new_date = input("Enter new Date(yyyy-mm-dd): ")
                transaction.date = new_date

            elif choice == 2:
                new_amou = float(input("Enter new amount: "))
                transaction.amount= new_amou

            elif choice == 3:
                new_cate = input("Enter new category: ")
                transaction.category = new_cate
            
            elif choice == 4:
                new_ty = input("Change the type: ")
                transaction.type = new_ty

            elif choice == 5:
                new_desc = input("Enter new Description: ")
                transaction.description = new_desc
            
            else:
                print("Invalid choice")
                
            
            self.save_data()
            print("Transaction Updated Successfully")

    def dele_transactions(self):
            trans_id = input("Enter the transaction id to delete: ")
            transaction = self.find_transaction_by_id(trans_id)

            if transaction:
                confirm = input("Are you sure you want to delete this transaction? (y/n): ")
                if confirm.lower()== 'y':
                    self.transactions.remove(transaction)
                    self.save_data()
                    print("Transaction Deleted Sucessfully!")
                else:
                    print("Deletion Cancelled.") 

    # Adding Data analysis part
    
    def generate_report(self):
        if not self.transactions:
            print("No Transaction to Analyze.")
            return
        
        monthly_summary = defaultdict(lambda: {"income" : 0, "expense": 0})
        category_summary = defaultdict(float)

        for t in self.transactions:
            # convert data string like dd-mm-yy into month year format

            date_obj = datetime.strptime(t.date, "%d-%m-%Y")
            month_year = date_obj.strftime("%B %Y")

            if t.type.lower() == "income":
                monthly_summary[month_year]["income"] += t.amount
            else:
                monthly_summary[month_year]["expense"] += t.amount
                category_summary[t.category] += t.amount

        # Show monthly summary
        print ("\n Monthly summary: ")
        for month,data in monthly_summary.items():
            print(f"{month}: Income ${data['income']} | Expense ${data['expense']}")

        # Show spending by Cateogry
        print("\n📊 Spending by Category:")
        for category, total in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
            print(f"{category}: ₹{total}")

        # Highest Expense Month
        highest_month = max(monthly_summary.items(), key=lambda x: x[1]["expense"])
        print(f"\n💸 Highest Expense Month: {highest_month[0]} (₹{highest_month[1]['expense']})")

        
    def search_filter_transactions(self):
        print("\n== Search & Filter==")
        keyword = input("Enter Keyword (leave blank to skip): ").strip().lower()
        min_amount = input("Enter min amount(leave blank to skip): ").strip()
        max_amount = input("Enter max amount(leave blank to skip): ").strip()
        start_date = input("Enter start date[DD-MM_YY](leave blank to skip): ").strip()
        end_date = input("Enter end date[DD-MM-YY](leave blank to skip): ").strip()
        category = input("Enter the category(leave blank to skip): ").strip().lower()

        results = self.transactions

        # keyword filter
        if keyword: 
            results = [t for t in results if keyword in t.trasactions.lower() or keyword in t.category.lower()]

        # Amount Filter
        if min_amount:
            results = [t for t in results if t.amount >= float(min_amount)]

        if max_amount:
            results = [t for t in results if t.amount <= float(max_amount)]

        # Date Filter
        if start_date:
            start_date = datetime.strptime(start_date, "%d-%m-%Y")
            reuslts = [t for t in results if datetime.strptime(t.date, "%d-%m-%Y") >= start_date]

        if end_date:
            end_date = datetime.strptime(end_date, "%d-%m-%Y")
            results = [t for t in results if datetime.strptime(t.date, "%d-%m-%Y") <= end_date ]

        # Category filter

        if category:
            results = [ t for t in results if t.category.lower() == category]

        # ✅ Show results
        if results:
            print(f"\nFound {len(results)} transaction(s):")
            for t in results:
                print(f"Date: {t.date} | Type: {t.type} | Amount: ₹{t.amount} | Category: {t.category} | Description: {t.description}")
                print("-" * 60)
        else:
            print("No matching transactions found.")

    def export_to_csv(self, filename= "transactions_export.csv"):
        if not self.transactions:
            print("No Trasactions Found! ")
            return
        
        # Convert Transaction Into Dictionaries

        data = [t.to_dict() for t in self.transactions]

        # Define the field name (columns)

        fieldnames = ["id", "date", "amount", "type", "category", "description"]

        # Wrie to CSV File
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"Data Exported successfully to {filename}")
