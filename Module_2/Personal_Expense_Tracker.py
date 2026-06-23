# ============================================================================
#  PERSONAL EXPENSE TRACKER  (command-line, powered by an SQLite database)
#  ---------------------------------------------------------------------------
#  Record what you spend, then get reports:
#    * a monthly summary grouped by category (food, travel, books, ...)
#    * your top 5 biggest single expenses
#  All data lives in a database file called "expenses.db".
# ============================================================================

# sqlite3  -> talk to the SQLite database.
# datetime -> get today's date so we can stamp each expense.
import sqlite3, datetime

# Open (or create) the database file and get a cursor to run commands with.
conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

# Create the "expenses" table if it doesn't already exist.
#   id       -> unique auto-number for each expense (PRIMARY KEY)
#   edate    -> the date of the expense, stored as text (e.g. 2026-06-24)
#   category -> what kind of spend it was (food, travel, ...)
#   amount   -> how much money. REAL means a decimal number.
#               CHECK (amount > 0) is a rule the database enforces: the amount
#               must be greater than zero, or the insert is rejected.
cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
                 id INTEGER PRIMARY KEY,
                 edate TEXT, category TEXT, amount REAL CHECK (amount > 0))""")


# ---------------------------------------------------------------------------
# FUNCTION: record a new expense.
# ---------------------------------------------------------------------------
def add_expense():
    # Ask for the category (text).
    cat = input("Category (food/travel/books/...): ")

    # Ask for the amount. float(...) turns the typed text into a decimal number
    # so that "45.50" becomes the number 45.5 we can add up later.
    amt = float(input("Amount ₹: "))

    # Insert a new row using safe placeholders (?,?,?).
    # date.today().isoformat() gives today's date as text like "2026-06-24".
    cur.execute("INSERT INTO expenses (edate, category, amount) VALUES (?,?,?)",
                (datetime.date.today().isoformat(), cat, amt))

    # Save the change permanently and confirm to the user.
    conn.commit(); print("✅ Recorded")


# ---------------------------------------------------------------------------
# FUNCTION: print a spending summary for one chosen month.
# ---------------------------------------------------------------------------
def monthly_summary():
    # Ask which month to report on, e.g. "2026-06".
    month = input("Month (YYYY-MM): ")

    # This SELECT does three powerful things:
    #   SUM(amount)  -> add up all amounts in each category (total spent)
    #   COUNT(*)     -> count how many expenses are in each category
    #   GROUP BY category -> do the SUM/COUNT separately PER category
    # WHERE edate LIKE ? with "2026-06%" keeps only dates starting with that
    # month (% is a wildcard meaning "anything after"). ORDER BY puts the
    # biggest-spending category first.
    cur.execute("""SELECT category, SUM(amount), COUNT(*)
                   FROM expenses
                   WHERE edate LIKE ?
                   GROUP BY category ORDER BY SUM(amount) DESC""",
                (month + "%",))

    # Grab all the result rows, and start a running grand total at 0.
    rows = cur.fetchall(); total = 0

    # Print a header row. The format specifiers control column alignment:
    #   {:<12} -> left-aligned in a 12-character wide column
    #   {:>10} -> right-aligned in a 10-character wide column
    print(f"\n{'Category':<12}{'Spent':>10}{'Items':>7}")

    # Loop through each category's results: cat=name, s=sum spent, n=count.
    for cat, s, n in rows:
        # {s:>10.2f} -> right-aligned, with exactly 2 decimal places (money).
        print(f"{cat:<12}{s:>10.2f}{n:>7}"); total += s   # add s to the total

    # A separator line ("-" repeated 29 times) then the grand TOTAL row.
    print("-" * 29 + f"\n{'TOTAL':<12}{total:>10.2f}")


# ---------------------------------------------------------------------------
# FUNCTION: show the 5 most expensive individual purchases.
# ---------------------------------------------------------------------------
def biggest_expenses():
    # ORDER BY amount DESC sorts most-expensive first; LIMIT 5 keeps only the
    # top 5 rows.
    cur.execute("""SELECT edate, category, amount FROM expenses
                   ORDER BY amount DESC LIMIT 5""")

    # Print each: date, category (left-aligned 10 wide), and amount with the ₹
    # sign and 2 decimal places.
    for d, c, a in cur.fetchall(): print(f"{d}  {c:<10} ₹{a:.2f}")


# ---------------------------------------------------------------------------
# THE MENU LOOP - runs until the user picks "Exit".
# ---------------------------------------------------------------------------
while True:
    ch = input("\n1.Add 2.Monthly summary 3.Top-5 4.Exit : ")
    if   ch=="1": add_expense()
    elif ch=="2": monthly_summary()
    elif ch=="3": biggest_expenses()
    elif ch=="4": break          # leave the loop -> end the program

# Always close the database when finished.
conn.close()
