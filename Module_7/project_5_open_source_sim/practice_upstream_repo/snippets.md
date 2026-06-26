# Snippets

A few handy one-liners. (Contains a deliberate typo for practice issue #1.)

## Python

### Read a file
```python
# This fucntion reads a whole file into a string.   ← typo: "fucntion" (issue #1)
def read_file(path):
    with open(path) as f:
        return f.read()
```

### Flatten a list of lists
```python
flat = [x for row in matrix for x in row]
```

<!--
  PRACTICE TASKS:
   #1  Fix the typo "fucntion" -> "function" above.
   #2  Add a "reverse a string" snippet:  reversed_str = s[::-1]
  Branch, commit with -s, and open a PR against this repo.
-->
