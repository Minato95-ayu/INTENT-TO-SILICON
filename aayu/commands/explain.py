import sys

ERROR_DICTIONARY = {
    "Unexpected token '-'": "Application names and variables cannot contain hyphens (-). Instead of 'my-app', try using underscores like 'my_app'.",
    "Expected 'end'": "Every block in AAYU (like page, row, column, action) must be closed with the 'end' keyword. Check if you missed an 'end'.",
    "Variable not found": "You tried to use a state variable that hasn't been declared yet. Make sure to define it with 'state my_var = value' at the top of your page.",
    "Maximum call depth": "Your actions are calling each other in an infinite loop! Action A calls B, and B calls A again.",
}

def handle(args):
    if not args:
        print("Usage: aayu explain \"<error message>\"")
        print("Example: aayu explain \"Unexpected token '-'\"")
        sys.exit(1)

    error_query = " ".join(args)
    print(f"Analyzing error: '{error_query}'\n")

    # Offline dictionary lookup for 1.0.0
    for key, explanation in ERROR_DICTIONARY.items():
        if key.lower() in error_query.lower():
            print(f"Explanation:")
            print(f"  {explanation}")
            print("\nTip: In future versions, this will be powered by BrainOS AI.")
            sys.exit(0)
            
    print("No specific explanation found in the offline dictionary.")
    print("If this is a bug, please report it at https://github.com/Minato95-ayu/INTENT-TO-SILICON/issues")
