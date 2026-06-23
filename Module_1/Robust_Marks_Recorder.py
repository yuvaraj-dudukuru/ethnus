# ============================================================================
#  ROBUST MARKS RECORDER
#  ---------------------------------------------------------------------------
#  A tiny program that asks the user for an exam mark (0-100), checks that the
#  value is sensible, and then saves it to a text file called "marks.txt".
#
#  The word "robust" means "strong / hard to break". This program is robust
#  because it uses ERROR HANDLING (try / except) so that a wrong input or a
#  file problem does not crash the whole program with an ugly error message.
# ============================================================================


# ---------------------------------------------------------------------------
# STEP 1: Create our own custom error type.
# ---------------------------------------------------------------------------
# Python already has built-in errors like ValueError. Sometimes we want our
# OWN error with a meaningful name so the code reads clearly. We make one by
# creating a class that "inherits from" (is based on) the built-in Exception.
class InvalidMarksError(Exception):
    # "pass" simply means "this class has no extra code of its own".
    # It is enough on its own - we only needed the name "InvalidMarksError".
    pass


# ---------------------------------------------------------------------------
# STEP 2: A function that gets a mark from the user and validates it.
# ---------------------------------------------------------------------------
# "def" defines a function. A function is a reusable block of code we can
# "call" by its name later. This one is named get_marks.
def get_marks():
    # "try" means: "attempt to run the code below, but be ready to catch an
    # error if one happens" - instead of letting the program crash.
    try:
        # input(...) shows a message and waits for the user to type something.
        # Whatever the user types always comes back as TEXT (a string).
        # int(...) converts that text into a whole number (an integer).
        # If the user types letters like "abc", int() cannot convert it and
        # Python raises a ValueError.
        m = int(input("Enter marks (0-100): "))

    # "except ValueError" runs ONLY if the int() conversion above failed.
    except ValueError:
        # "raise" deliberately triggers an error so the calling code knows
        # something went wrong. We give a friendly message inside it.
        raise ValueError("Please enter a valid integer.")

    # This is a "guard" check. A mark should be between 0 and 100.
    # "0 <= m <= 100" reads as "is m between 0 and 100 (inclusive)?".
    # "not" flips the answer, so this whole line means:
    # "if the mark is NOT between 0 and 100..."
    if not 0 <= m <= 100:
        # ...then raise OUR custom error with a clear explanation.
        raise InvalidMarksError("Marks must be between 0 and 100.")

    # If we reached this line, the mark is a valid number in range.
    # "return" sends that value back to whoever called this function.
    return m


# ---------------------------------------------------------------------------
# STEP 3: The main program - get the mark, then save it.
# ---------------------------------------------------------------------------
# We wrap the whole flow in another try block so we can react to any problem.
try:
    # Call our function. If it raises an error, the matching "except" below
    # will catch it. If it succeeds, "marks" holds the validated number.
    marks = get_marks()

# This single "except" catches TWO possible error types (listed in brackets):
# a built-in ValueError OR our custom InvalidMarksError.
# "as e" saves the actual error object into a variable named e so we can print
# its message.
except (ValueError, InvalidMarksError) as e:
    # Tell the user their input was not accepted, and show the reason (e).
    print("Input rejected:", e)

# "else" runs ONLY if the try block above finished WITHOUT any error.
# In other words: "the mark was good, so now let's save it."
else:
    # Saving to a file can also fail (disk full, no permission, etc.),
    # so we use another try / except just for the file work.
    try:
        # open(...) opens the file. "a" means "append" - add to the END of the
        # file without erasing what is already there. If the file does not
        # exist yet, Python creates it.
        # "with ... as f" is the safe way to open files: it automatically
        # closes the file for us when the block finishes.
        with open("marks.txt", "a") as f:
            # Write the mark followed by "\n", which means "new line", so each
            # mark sits on its own line in the file.
            # f"{marks}\n" is an f-string: it drops the value of marks inside.
            f.write(f"{marks}\n")
        # If writing worked, let the user know.
        print("Saved successfully!")

    # OSError covers operating-system / file related problems.
    except OSError as e:
        print("File error:", e)

# "finally" ALWAYS runs at the very end, whether there was an error or not.
# It is perfect for clean-up or a closing message.
finally:
    print("Session closed.")
