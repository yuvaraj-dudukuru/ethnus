# Module 2 — Python + Databases (SQLite CRUD Applications)

This module takes the next big step: storing data in a **real database** instead
of plain text files. It contains **three command-line applications**, each built
on **SQLite** — a lightweight database that lives inside a single file and needs
no separate server to install.

Together these apps teach the four operations that almost every real program
performs, known by the nickname **CRUD**:

> **C**reate · **R**ead · **U**pdate · **D**elete

---

## 📁 Files in this module

| File | What it is | Database file it creates |
|------|------------|--------------------------|
| `Notes_Application.py` | A note-taking app (add / list / read / search / delete notes). | `notes.db` |
| `Personal_Expense_Tracker.py` | Track spending and generate monthly + top-5 reports. | `expenses.db` |
| `Contact_Manager.py` | A phone book with unique phone numbers. | `contacts.db` |

> The `.db` files are created automatically the first time you run each program.

---

## 🧠 The core database concepts (explained simply)

### What is SQLite?
A database stored in **one file**. You talk to it using a language called **SQL**
(Structured Query Language). Python's built-in `sqlite3` module lets us send SQL
commands from our code.

### The 3-step pattern every app uses
```python
conn = sqlite3.connect("data.db")   # 1. open (or create) the database file
cur  = conn.cursor()                # 2. get a "cursor" to run commands with
cur.execute("CREATE TABLE ...")     # 3. run SQL commands
```
- **`conn`** (connection) = the open line to the database.
- **`cur`** (cursor) = the "pen" we use to write commands and read results.
- **`conn.commit()`** = **SAVE** changes permanently. Forgetting this means your
  data is lost!
- **`conn.close()`** = close the database cleanly when finished.

### The key SQL commands you'll see
| SQL | Meaning | CRUD letter |
|-----|---------|-------------|
| `INSERT INTO ...` | Add a new row | **C**reate |
| `SELECT ...` | Read rows back out | **R**ead |
| `UPDATE ... SET ...` | Change an existing row | **U**pdate |
| `DELETE FROM ...` | Remove a row | **D**elete |

### ⭐ Safe queries with `?` placeholders (very important!)
Notice we **never** glue user text directly into SQL. Instead:
```python
cur.execute("SELECT * FROM contacts WHERE name LIKE ?", (q,))
```
The `?` is a **placeholder**, and the real value is passed separately. This is a
**parameterised query**, and it protects against a famous security hole called
**SQL injection**. Every app in this module follows this rule.

### `fetchone()` vs `fetchall()`
- `fetchone()` → returns just the **first** matching row (or `None`).
- `fetchall()` → returns **all** matching rows as a list you can loop over.

---

## 📒 App 1 — Notes Application (`Notes_Application.py`)

A personal notebook. Each note has a title, body, and an automatic timestamp.

| Menu option | What it does | SQL behind it |
|-------------|--------------|---------------|
| 1. Add | Save a new note with the current date/time | `INSERT` |
| 2. List | Show all notes, newest first | `SELECT ... ORDER BY id DESC` |
| 3. Read | Open one full note by its id | `SELECT ... WHERE id = ?` |
| 4. Search | Find notes by keyword in title or body | `SELECT ... WHERE ... LIKE ?` |
| 5. Delete | Remove a note by id | `DELETE` |

**New ideas introduced:** timestamps with `datetime`, the `LIKE '%keyword%'`
wildcard search, and `cur.lastrowid` (the id the database just assigned).

---

## 💸 App 2 — Personal Expense Tracker (`Personal_Expense_Tracker.py`)

Log every expense, then get useful reports.

| Menu option | What it does | SQL behind it |
|-------------|--------------|---------------|
| 1. Add | Record category + amount with today's date | `INSERT` |
| 2. Monthly summary | Total + count **per category** for a chosen month | `SUM`, `COUNT`, `GROUP BY` |
| 3. Top-5 | The 5 most expensive single purchases | `ORDER BY amount DESC LIMIT 5` |

**New ideas introduced:**
- **Aggregate functions** — `SUM()` adds values up, `COUNT()` counts rows.
- **`GROUP BY`** — do those calculations *separately for each category*.
- A **`CHECK (amount > 0)`** rule in the table so negative amounts are rejected.
- **Formatted output** — f-string alignment like `{s:>10.2f}` to print neat,
  right-aligned money columns.

---

## 📇 App 3 — Contact Manager (`Contact_Manager.py`)

A phone book where every phone number must be unique.

| Menu option | What it does | SQL behind it |
|-------------|--------------|---------------|
| 1. Add | Add a contact (rejects duplicate phone numbers) | `INSERT` |
| 2. Search | Find contacts by part of their name | `SELECT ... LIKE ?` |
| 3. Update | Change a contact's phone number | `UPDATE` |
| 4. Delete | Remove a contact by id | `DELETE` |

**New ideas introduced:**
- **`UNIQUE` columns** — the database itself forbids duplicate phone numbers.
- **`sqlite3.IntegrityError`** — the error raised when a `UNIQUE`/`NOT NULL`
  rule is broken; we catch it with `try/except` to show a friendly message.
- **`conn.row_factory = sqlite3.Row`** — lets us read columns by **name**
  (`row['name']`) instead of by position (`row[0]`).

---

## ▶️ How to run any app

1. Make sure **Python 3** is installed (`sqlite3` is included with Python — no
   extra installation needed).
2. Open a terminal in this `Module_2` folder.
3. Run the one you want:
   ```bash
   python Notes_Application.py
   python Personal_Expense_Tracker.py
   python Contact_Manager.py
   ```
4. Follow the on-screen number menu. Choose the **Exit** option to quit safely.

---

## ✅ What you should take away

- Databases store data **permanently** and let you query it powerfully.
- The **connect → cursor → execute → commit → close** cycle is the backbone of
  every database program.
- Always use **`?` placeholders** for user input (safety first).
- SQL can **search, sort, group, and summarise** data far more easily than hand-
  written loops.
- Catching `IntegrityError` lets the database enforce rules while your program
  stays friendly.
