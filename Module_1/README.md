# Module 1 — Python Fundamentals & Error Handling

This module is the **first step** of the journey. It focuses on one of the most
important real-world programming skills: **handling things that can go wrong**
without letting the program crash.

It contains a single, focused program — the **Robust Marks Recorder** — plus the
data file it produces.

---

## 📁 Files in this module

| File | What it is |
|------|------------|
| `Robust_Marks_Recorder.py` | The Python program (fully commented line-by-line). |
| `marks.txt` | A plain-text file where the saved marks are stored, one per line. |

---

## 🎯 What this program does

The **Robust Marks Recorder** asks the user to type an exam mark between **0 and
100**, makes sure the value is sensible, and then **saves it to `marks.txt`**.

If the user types something silly (like letters, or `250`), the program does
**not** crash. Instead it politely rejects the input and explains why. That
quality of "not breaking when given bad input" is what the word **robust**
means.

---

## 🧠 Key beginner concepts demonstrated

### 1. Functions (`def`)
A **function** is a named, reusable block of code. Here `get_marks()` bundles up
the "ask for a mark and check it" logic so the main program stays clean.

### 2. `try` / `except` — catching errors
This is the heart of the module.

- **`try`** — "attempt this code, but be ready if it fails."
- **`except`** — "if a specific error happens, run this instead of crashing."

For example, if the user types `abc`, `int("abc")` fails with a `ValueError`,
and our `except` block catches it.

### 3. `raise` — creating an error on purpose
`raise` deliberately signals "something is wrong." We use it to reject marks
that are out of the 0–100 range.

### 4. Custom exceptions
```python
class InvalidMarksError(Exception):
    pass
```
Python lets you invent your **own** error type with a meaningful name. Reading
`raise InvalidMarksError(...)` instantly tells you *what kind* of problem
occurred — much clearer than a generic error.

### 5. `try` / `except` / `else` / `finally` — the full flow
| Keyword | When it runs |
|---------|--------------|
| `try` | Always — it's the code we're attempting. |
| `except` | Only if an error happened. |
| `else` | Only if **no** error happened (the "success" path). |
| `finally` | **Always**, at the very end — perfect for clean-up messages. |

### 6. Writing to a file safely
```python
with open("marks.txt", "a") as f:
    f.write(f"{marks}\n")
```
- `"a"` means **append** — add to the end without erasing old data.
- `with ... as f` automatically **closes** the file when done (safe & tidy).
- `\n` is a **new line**, so each mark sits on its own row.

---

## ▶️ How to run it

1. Make sure you have **Python 3** installed.
2. Open a terminal in this `Module_1` folder.
3. Run:
   ```bash
   python Robust_Marks_Recorder.py
   ```
4. Type a number when prompted, e.g. `87`, and press **Enter**.

### Try these inputs to see the robustness in action
| You type | What happens |
|----------|--------------|
| `87` | ✅ `Saved successfully!` — and `87` is added to `marks.txt`. |
| `abc` | ❌ `Input rejected: Please enter a valid integer.` |
| `250` | ❌ `Input rejected: Marks must be between 0 and 100.` |

No matter what, you will always see `Session closed.` at the end — that is the
`finally` block doing its job.

---

## ✅ What you should take away

- Programs should **expect bad input** and handle it gracefully.
- `try/except/else/finally` gives you full control over success and failure.
- Custom exceptions make your code **self-explaining**.
- Files can be written to safely with `with open(...)`.
