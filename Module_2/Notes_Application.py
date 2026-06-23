# ============================================================================
#  NOTES APPLICATION  (command-line, powered by an SQLite database)
#  ---------------------------------------------------------------------------
#  A small "notebook" that lets you ADD, LIST, READ, SEARCH and DELETE notes.
#  Everything is stored in a real database file called "notes.db", so your
#  notes are still there the next time you run the program.
#
#  Key idea for beginners: instead of a plain text file, we use SQLite - a
#  tiny database that lives inside a single file and understands SQL commands.
# ============================================================================

# "import" pulls in extra tools (called modules) that Python provides.
#   sqlite3  -> lets us talk to an SQLite database.
#   datetime -> lets us get the current date and time (used as a timestamp).
import sqlite3, datetime

# connect(...) opens (or CREATES, if missing) the database file "notes.db".
# "conn" is our connection - the open line to the database.
conn = sqlite3.connect("notes.db")

# A "cursor" is the object we use to actually send SQL commands and read
# results back. Think of it as the pen we write database instructions with.
cur = conn.cursor()

# execute(...) runs an SQL command. The triple-quoted """ ... """ lets the SQL
# span several lines for readability.
# This command creates a table named "notes" ONLY IF it does not already exist
# (so re-running the program is safe). A table is like a spreadsheet:
#   id      -> a unique number for each note (PRIMARY KEY = auto, never repeats)
#   title   -> the note's title; NOT NULL means it can never be left empty
#   body    -> the main text of the note
#   created -> the date/time the note was made, saved as text
cur.execute("""CREATE TABLE IF NOT EXISTS notes (
                 id      INTEGER PRIMARY KEY,
                 title   TEXT NOT NULL,
                 body    TEXT,
                 created TEXT)""")


# ---------------------------------------------------------------------------
# FUNCTION: add a new note to the database.
# ---------------------------------------------------------------------------
def add_note():
    # Ask the user for a title and the note text.
    # (Two statements on one line separated by ';' - just a compact style.)
    t = input("Title: "); b = input("Note: ")

    # INSERT adds a new row. The question marks (?,?,?) are PLACEHOLDERS.
    # We never paste user text straight into SQL - instead we pass the values
    # separately as a tuple (t, b, ...). This is called a "parameterised
    # query" and it protects against a security problem called SQL injection.
    cur.execute("INSERT INTO notes (title, body, created) VALUES (?,?,?)",
                # strftime formats the current date/time as e.g. 2026-06-24 14:30
                (t, b, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

    # commit() SAVES the change permanently to the file. Without it, the new
    # note would be lost. cur.lastrowid is the id the database just assigned.
    conn.commit(); print("✅ Saved (id =", cur.lastrowid, ")")


# ---------------------------------------------------------------------------
# FUNCTION: list every note (newest first), showing id, title and date.
# ---------------------------------------------------------------------------
def list_notes():
    # SELECT reads data. We ask for three columns, ORDER BY id DESC means
    # "sort by id, highest first" - so the newest notes appear at the top.
    cur.execute("SELECT id, title, created FROM notes ORDER BY id DESC")

    # fetchall() returns ALL matching rows as a list. We loop through each row;
    # because we selected 3 columns, each row unpacks neatly into i, t, c.
    for i, t, c in cur.fetchall():
        # Print a tidy line like:  [3] Shopping list   (2026-06-24 14:30)
        print(f"[{i}] {t}   ({c})")


# ---------------------------------------------------------------------------
# FUNCTION: read (open) one full note by its id number.
# ---------------------------------------------------------------------------
def read_note():
    nid = input("Note id: ")
    # Find the one note whose id matches what the user typed.
    cur.execute("SELECT title, body, created FROM notes WHERE id = ?", (nid,))

    # fetchone() returns just the FIRST matching row, or None if nothing matched.
    row = cur.fetchone()

    # This is a one-line "if/else" (a ternary expression):
    #   if row exists -> print the formatted note (title, date, then body)
    #   else          -> print "Not found"
    # row[0]=title, row[1]=body, row[2]=created.
    print(f"\n== {row[0]} ({row[2]}) ==\n{row[1]}" if row else "❌ Not found")


# ---------------------------------------------------------------------------
# FUNCTION: search notes by a keyword in the title OR body.
# ---------------------------------------------------------------------------
def search_notes():
    kw = input("Keyword: ")
    # LIKE does partial text matching. The % signs are wildcards meaning
    # "any characters", so "%cat%" matches "category", "scatter", etc.
    cur.execute("SELECT id, title FROM notes WHERE title LIKE ? OR body LIKE ?",
                (f"%{kw}%", f"%{kw}%"))          # safe LIKE with parameters

    # Show each matching note's id and title.
    for i, t in cur.fetchall(): print(f"[{i}] {t}")


# ---------------------------------------------------------------------------
# FUNCTION: delete a note by its id.
# ---------------------------------------------------------------------------
def delete_note():
    nid = input("Delete id: ")
    # DELETE removes the row whose id matches.
    cur.execute("DELETE FROM notes WHERE id = ?", (nid,))

    # cur.rowcount tells us how many rows were affected. If it is 0, no note
    # had that id, so we report "Not found". commit() saves the deletion.
    conn.commit(); print("✅ Deleted" if cur.rowcount else "❌ Not found")


# ---------------------------------------------------------------------------
# THE MENU LOOP - keeps showing options until the user chooses to exit.
# ---------------------------------------------------------------------------
# "while True:" loops forever, until a "break" statement stops it.
while True:
    # Show the menu and read the user's choice (as text, e.g. "1").
    ch = input("\n1.Add 2.List 3.Read 4.Search 5.Delete 6.Exit : ")

    # Run the matching function based on what number was typed.
    if   ch=="1": add_note()
    elif ch=="2": list_notes()
    elif ch=="3": read_note()
    elif ch=="4": search_notes()
    elif ch=="5": delete_note()
    elif ch=="6": break          # "break" exits the while loop -> ends program

# Once the loop ends, close the database connection cleanly.
conn.close()
