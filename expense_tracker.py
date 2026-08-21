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


# ---------------- CORE LOGIC ----------------


def add_transaction(transaction_type, amount, category):
    transaction_type = transaction_type.strip().lower()
    category = category.strip()

    if transaction_type not in ["income", "expense"]:
        return False

    if not isinstance(amount, (int, float)) or amount <= 0:
        return False

    if not category:
        return False

    transaction = {
        "type": transaction_type,
        "amount": float(amount),
        "category": category
    }

    transactions.append(transaction)
    save_transactions()

    return True


def get_transactions():
    return transactions


def calculate_summary():
    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        if transaction["type"] == "income":
            total_income += transaction["amount"]

        elif transaction["type"] == "expense":
            total_expenses += transaction["amount"]

    balance = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance
    }


def filter_transactions_by_category(category):
    category = category.strip().lower()

    if not category:
        return []

    found_transactions = []

    for transaction in transactions:
        if category in transaction["category"].lower():
            found_transactions.append(transaction)

    return found_transactions


def delete_transaction(transaction_number):
    if not isinstance(transaction_number, int):
        return False

    if (
        transaction_number < 1
        or transaction_number > len(transactions)
    ):
        return False

    transactions.pop(transaction_number - 1)
    save_transactions()

    return True


# ---------------- USER INTERFACE ----------------


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


def add_income_menu():
    amount = get_valid_amount()

    if amount is None:
        return

    category = input("Enter income category: ").strip()

    if add_transaction("income", amount, category):
        print("\nIncome added successfully!")
    else:
        print("Category cannot be empty.")


def add_expense_menu():
    amount = get_valid_amount()

    if amount is None:
        return

    category = input("Enter expense category: ").strip()

    if add_transaction("expense", amount, category):
        print("\nExpense added successfully!")
    else:
        print("Category cannot be empty.")


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
    summary = calculate_summary()

    print("\n" + "=" * 35)
    print("         FINANCIAL SUMMARY")
    print("=" * 35)
    print(f"Total Income: ₹{summary['total_income']:.2f}")
    print(f"Total Expenses: ₹{summary['total_expenses']:.2f}")
    print(f"Remaining Balance: ₹{summary['balance']:.2f}")


def filter_by_category_menu():
    if not transactions:
        print("\nNo transactions found.")
        return

    category = input(
        "\nEnter category to filter: "
    ).strip()

    found_transactions = filter_transactions_by_category(category)

    if not found_transactions:
        print("\nNo transactions found in this category.")
        return

    print("\n" + "=" * 35)
    print(f"   TRANSACTIONS: {category.upper()}")
    print("=" * 35)

    for number, transaction in enumerate(
        found_transactions,
        start=1
    ):
        print(f"\nTransaction {number}")
        print(f"Type: {transaction['type'].title()}")
        print(f"Amount: ₹{transaction['amount']:.2f}")
        print(f"Category: {transaction['category']}")


def delete_transaction_menu():
    if not transactions:
        print("\nNo transactions found.")
        return

    view_transactions()

    try:
        transaction_number = int(
            input(
                "\nEnter transaction number to delete: "
            ).strip()
        )

    except ValueError:
        print("Please enter a valid transaction number.")
        return

    if delete_transaction(transaction_number):
        print("\nTransaction deleted successfully!")
    else:
        print("Invalid transaction number.")


def main():
    load_transactions()

    while True:
        show_menu()

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_income_menu()

        elif choice == "2":
            add_expense_menu()

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_summary()

        elif choice == "5":
            filter_by_category_menu()

        elif choice == "6":
            delete_transaction_menu()

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