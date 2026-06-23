# ============================================================================
#  CONTACT MANAGER  (command-line address book, powered by SQLite)
#  ---------------------------------------------------------------------------
#  A simple phone book that lets you ADD, SEARCH, UPDATE and DELETE contacts.
#  It demonstrates two extra database ideas beyond the other apps:
#    1. UNIQUE columns (no two contacts may share the same phone number)
#    2. Catching the IntegrityError that the database raises when a rule breaks
#  Data is saved in "contacts.db".
# ============================================================================

# We only need sqlite3 here (no dates are stored).
import sqlite3

# Open / create the database file.
conn = sqlite3.connect("contacts.db")

# By default SQLite returns each row as a plain tuple, where you access values
# by POSITION (row[0], row[1], ...). Setting row_factory to sqlite3.Row lets us
# access values by COLUMN NAME instead (row['name']), which is much clearer.
conn.row_factory = sqlite3.Row          # rows accessible by column NAME

cur = conn.cursor()

# Create the "contacts" table if it doesn't exist.
#   id    -> unique auto-number (PRIMARY KEY)
#   name  -> NOT NULL, so every contact must have a name
#   phone -> UNIQUE, so the SAME number can never be stored twice
#   email -> the contact's email address
cur.execute("""CREATE TABLE IF NOT EXISTS contacts (
                 id INTEGER PRIMARY KEY,
                 name  TEXT NOT NULL,
                 phone TEXT UNIQUE,      -- no duplicate numbers!
                 email TEXT)""")


# ---------------------------------------------------------------------------
# FUNCTION: add a new contact.
# ---------------------------------------------------------------------------
def add_contact():
    # Ask for all three fields at once and unpack them into n, p, e.
    n, p, e = input("Name: "), input("Phone: "), input("Email: ")

    # The phone column is UNIQUE. If we try to add a number that already
    # exists, the database refuses and raises sqlite3.IntegrityError - so we
    # wrap the insert in try/except to handle that gracefully.
    try:
        cur.execute("INSERT INTO contacts (name,phone,email) VALUES (?,?,?)",
                    (n, p, e))
        conn.commit(); print("✅ Added")
    except sqlite3.IntegrityError:
        # This runs when the UNIQUE rule was broken (duplicate phone number).
        print("❌ That phone number already exists!")


# ---------------------------------------------------------------------------
# FUNCTION: search contacts by (part of) their name.
# ---------------------------------------------------------------------------
def search_contact():
    # Wrap the typed text in % wildcards so a partial name matches.
    # e.g. searching "an" finds "Anita", "Daniel", "Ananya", etc.
    q = "%" + input("Search name: ") + "%"

    # SELECT * means "all columns". ORDER BY name sorts results alphabetically.
    cur.execute("SELECT * FROM contacts WHERE name LIKE ? ORDER BY name", (q,))

    # Loop through each matching row. Thanks to row_factory above, we can read
    # columns by name. The format specifiers line everything up in neat columns:
    #   {r['id']:>3}    -> id right-aligned, 3 wide
    #   {r['name']:<15} -> name left-aligned, 15 wide
    #   {r['phone']:<12}-> phone left-aligned, 12 wide
    for r in cur.fetchall():
        print(f"{r['id']:>3}. {r['name']:<15} {r['phone']:<12} {r['email']}")


# ---------------------------------------------------------------------------
# FUNCTION: update a contact's phone number.
# ---------------------------------------------------------------------------
def update_contact():
    # Ask which contact (by id) and what the new number should be.
    cid = input("Contact id: "); newp = input("New phone: ")

    try:
        # UPDATE changes existing data. SET phone = ? puts the new number in,
        # WHERE id = ? picks the single contact to change.
        cur.execute("UPDATE contacts SET phone = ? WHERE id = ?", (newp, cid))
        conn.commit()

        # cur.rowcount is how many rows changed. If it's 0, no contact had that
        # id, so we report it was not found.
        print("✅ Updated" if cur.rowcount else "❌ Id not found")
    except sqlite3.IntegrityError:
        # Triggered if the new number already belongs to a DIFFERENT contact
        # (the UNIQUE rule again).
        print("❌ Number belongs to another contact")


# ---------------------------------------------------------------------------
# FUNCTION: delete a contact by id.
# ---------------------------------------------------------------------------
def delete_contact():
    cid = input("Delete id: ")
    cur.execute("DELETE FROM contacts WHERE id = ?", (cid,))
    # rowcount of 0 means nothing matched that id.
    conn.commit(); print("✅ Deleted" if cur.rowcount else "❌ Id not found")


# ---------------------------------------------------------------------------
# THE MENU LOOP - runs until the user chooses "Exit".
# ---------------------------------------------------------------------------
while True:
    ch = input("\n1.Add 2.Search 3.Update 4.Delete 5.Exit : ")
    if   ch=="1": add_contact()
    elif ch=="2": search_contact()
    elif ch=="3": update_contact()
    elif ch=="4": delete_contact()
    elif ch=="5": break          # exit the loop -> end the program

# Always close the connection when finished.
conn.close()
