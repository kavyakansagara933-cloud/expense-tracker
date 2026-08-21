import json
import os


DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "transactions.json")

transactions = []


def load_transactions():
    global transactions

    if not os.path.exists(DATA_FILE):
        transactions = []
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            transactions = json.load(file)

    except (json.JSONDecodeError, OSError):
        print(
            "Could not load saved transactions. "
            "Starting with an empty list."
        )
        transactions = []


def save_transactions():
    os.makedirs(DATA_FOLDER, exist_ok=True)

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)

    except OSError:
        print("Could not save transactions.")


def show_menu():
    print("\n" + "=" * 35)
    print("        EXPENSE TRACKER")
    print("=" * 35)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Summary")
    print("5. Filter by Category")
    print("6. Delete Transaction")
    print("7. Exit")


def get_valid_amount():
    try:
        amount = float(input("Enter amount: ").strip())

        if amount <= 0:
            print("Amount must be greater than 0.")
            return None

        return amount

    except ValueError:
        print("Please enter a valid number.")
        return None


def add_income():
    amount = get_valid_amount()

    if amount is None:
        return

    category = input("Enter income category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    transaction = {
        "type": "income",
        "amount": amount,
        "category": category
    }

    transactions.append(transaction)
    save_transactions()

    print("\nIncome added successfully!")


def add_expense():
    amount = get_valid_amount()

    if amount is None:
        return

    category = input("Enter expense category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    transaction = {
        "type": "expense",
        "amount": amount,
        "category": category
    }

    transactions.append(transaction)
    save_transactions()

    print("\nExpense added successfully!")


def view_transactions():
    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n" + "=" * 35)
    print("       ALL TRANSACTIONS")
    print("=" * 35)

    for number, transaction in enumerate(transactions, start=1):
        print(f"\nTransaction {number}")
        print(f"Type: {transaction['type'].title()}")
        print(f"Amount: ₹{transaction['amount']:.2f}")
        print(f"Category: {transaction['category']}")


def view_summary():
    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        if transaction["type"] == "income":
            total_income += transaction["amount"]

        elif transaction["type"] == "expense":
            total_expenses += transaction["amount"]

    balance = total_income - total_expenses

    print("\n" + "=" * 35)
    print("         FINANCIAL SUMMARY")
    print("=" * 35)
    print(f"Total Income: ₹{total_income:.2f}")
    print(f"Total Expenses: ₹{total_expenses:.2f}")
    print(f"Remaining Balance: ₹{balance:.2f}")


def filter_by_category():
    if not transactions:
        print("\nNo transactions found.")
        return

    category = input(
        "\nEnter category to filter: "
    ).strip().lower()

    if not category:
        print("Category cannot be empty.")
        return

    found_transactions = []

    for transaction in transactions:
        if category in transaction["category"].lower():
            found_transactions.append(transaction)

    if not found_transactions:
        print("\nNo transactions found in this category.")
        return

    print("\n" + "=" * 35)
    print(f"   TRANSACTIONS: {category.upper()}")
    print("=" * 35)

    for number, transaction in enumerate(found_transactions, start=1):
        print(f"\nTransaction {number}")
        print(f"Type: {transaction['type'].title()}")
        print(f"Amount: ₹{transaction['amount']:.2f}")
        print(f"Category: {transaction['category']}")


def delete_transaction():
    if not transactions:
        print("\nNo transactions found.")
        return

    view_transactions()

    try:
        transaction_number = int(
            input("\nEnter transaction number to delete: ").strip()
        )

        if transaction_number < 1 or transaction_number > len(transactions):
            print("Invalid transaction number.")
            return

    except ValueError:
        print("Please enter a valid transaction number.")
        return

    deleted_transaction = transactions.pop(transaction_number - 1)
    save_transactions()

    print(
        f"\n{deleted_transaction['type'].title()} transaction "
        f"of ₹{deleted_transaction['amount']:.2f} "
        "deleted successfully!"
    )


def main():
    load_transactions()

    while True:
        show_menu()

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_income()

        elif choice == "2":
            add_expense()

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_summary()

        elif choice == "5":
            filter_by_category()

        elif choice == "6":
            delete_transaction()

        elif choice == "7":
            print("\nGoodbye!")
            break

        else:
            print(
                "\nInvalid option. "
                "Please choose 1, 2, 3, 4, 5, 6, or 7."
            )


if __name__ == "__main__":
    main()