import expense_tracker as et


def setup_function():
    et.transactions.clear()


# ---------------- ADD TRANSACTION TESTS ----------------


def test_add_income():
    result = et.add_transaction(
        "income",
        50000,
        "Salary"
    )

    assert result is True
    assert len(et.transactions) == 1
    assert et.transactions[0]["type"] == "income"
    assert et.transactions[0]["amount"] == 50000.0
    assert et.transactions[0]["category"] == "Salary"


def test_add_expense():
    result = et.add_transaction(
        "expense",
        1200,
        "Food"
    )

    assert result is True
    assert len(et.transactions) == 1
    assert et.transactions[0]["type"] == "expense"


def test_invalid_transaction_type():
    result = et.add_transaction(
        "transfer",
        1000,
        "Bank"
    )

    assert result is False
    assert len(et.transactions) == 0


def test_zero_amount():
    result = et.add_transaction(
        "income",
        0,
        "Salary"
    )

    assert result is False


def test_negative_amount():
    result = et.add_transaction(
        "expense",
        -500,
        "Food"
    )

    assert result is False


def test_invalid_amount_type():
    result = et.add_transaction(
        "income",
        "5000",
        "Salary"
    )

    assert result is False


def test_empty_category():
    result = et.add_transaction(
        "income",
        5000,
        ""
    )

    assert result is False


def test_empty_transaction_type():
    result = et.add_transaction(
        "",
        5000,
        "Salary"
    )

    assert result is False


# ---------------- SUMMARY TESTS ----------------


def test_calculate_summary():
    et.add_transaction("income", 50000, "Salary")
    et.add_transaction("income", 5000, "Freelancing")
    et.add_transaction("expense", 1200, "Food")
    et.add_transaction("expense", 3000, "Travel")

    summary = et.calculate_summary()

    assert summary["total_income"] == 55000
    assert summary["total_expenses"] == 4200
    assert summary["balance"] == 50800


def test_empty_summary():
    summary = et.calculate_summary()

    assert summary["total_income"] == 0
    assert summary["total_expenses"] == 0
    assert summary["balance"] == 0


def test_expenses_greater_than_income():
    et.add_transaction("income", 1000, "Salary")
    et.add_transaction("expense", 1500, "Shopping")

    summary = et.calculate_summary()

    assert summary["balance"] == -500


# ---------------- FILTER TESTS ----------------


def test_filter_by_category():
    et.add_transaction("expense", 1200, "Food")
    et.add_transaction("expense", 800, "Food")
    et.add_transaction("expense", 3000, "Travel")

    found_transactions = et.filter_transactions_by_category(
        "food"
    )

    assert len(found_transactions) == 2


def test_filter_case_insensitive():
    et.add_transaction("expense", 1200, "Food")

    found_transactions = et.filter_transactions_by_category(
        "FOOD"
    )

    assert len(found_transactions) == 1


def test_filter_partial_category():
    et.add_transaction("expense", 3000, "Travel")

    found_transactions = et.filter_transactions_by_category(
        "trav"
    )

    assert len(found_transactions) == 1


def test_filter_non_existing_category():
    et.add_transaction("expense", 1200, "Food")

    found_transactions = et.filter_transactions_by_category(
        "Gaming"
    )

    assert found_transactions == []


def test_filter_empty_category():
    found_transactions = et.filter_transactions_by_category("")

    assert found_transactions == []


# ---------------- DELETE TESTS ----------------


def test_delete_transaction():
    et.add_transaction("income", 50000, "Salary")
    et.add_transaction("expense", 1200, "Food")

    result = et.delete_transaction(1)

    assert result is True
    assert len(et.transactions) == 1
    assert et.transactions[0]["type"] == "expense"


def test_delete_invalid_zero():
    et.add_transaction("income", 50000, "Salary")

    result = et.delete_transaction(0)

    assert result is False
    assert len(et.transactions) == 1


def test_delete_out_of_range():
    et.add_transaction("income", 50000, "Salary")

    result = et.delete_transaction(5)

    assert result is False


def test_delete_invalid_type():
    et.add_transaction("income", 50000, "Salary")

    result = et.delete_transaction("1")

    assert result is False


def test_delete_from_empty_list():
    result = et.delete_transaction(1)

    assert result is False