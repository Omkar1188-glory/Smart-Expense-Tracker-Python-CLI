
from tracker import Tracker
from models import Transaction



# main.py

def main():
    tracker = Tracker()
    tracker.load_data()

    while True:
        print("\n===== Smart Expense Tracker =====")
        print("1. Add transaction")
        print("2. View all transactions")
        print("3. View summary")
        print("4. Edit Transaction")
        print("5. Delete Transaction")
        print("6. Reprot & Analysis")
        print("7. Search/ Filter Transactions")
        print("8. Export to CSV")
        print("9. Quit")

        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            # Ask user for transaction details
            date = input("Enter date (eg. 12-05-2025): ")
            amount = input("Enter amount: ")
            type  = input("Enter type (Income/Expense): ")
            category = input("Enter the category (eg: food, rent, salary): ")
            description = input("Enter description (Optional): ")

            # Create a Transaction Object
            transaction = Transaction(date, amount, type, category, description)

            # Add to tracker

            tracker.add_transaction(transaction)
            
        elif choice == '2':
          tracker.list_transaction()
              # print("View all transactions - Not implemented yet.")
        
        elif choice == '3':
            print("\n==Expense Summary==")
            summary = tracker.get_summary()
            print(f"Total Income: ${summary['income']}")
            print(f"Total Expense: ${summary['expense']}")
            print(f"Balance: ${summary['balance']}")
            print("\n Expenses By Category: ")
            for category, amount in summary['by_category'].items():
                print(f" {category}: ${amount}")

            # print("View summary - Not implemented yet.")
    
        elif choice == '4':
            tracker.edit_transaction()

        elif choice == '5':
            tracker.dele_transactions()

        elif choice == '6':
            tracker.generate_report()
        
        elif choice == '7':
            tracker.search_filter_transactions()

        elif choice == '8':
            tracker.export_to_csv()

        elif choice == '9':
            print("Saving Data")
            tracker.save_data()
            print("Thank you for using Smart Expense Tracker! Goodbye 👋")
            break
    
        else :
            print("Invalid Input. Please enter a number between 1 to 9.")
          




if __name__ == "__main__":
    main()
 