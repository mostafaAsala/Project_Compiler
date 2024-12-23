import importlib.util
import subprocess

libs = ['colorama']
for lib in libs:
    imported = importlib.util.find_spec(lib)
    if imported is None:
        try:
            subprocess.check_call(['pip','install',lib])
        except subprocess.CalledProcessError:
            pass


from colorama import Fore, Style, init
init(autoreset=True)
def is_simple_grammar(rules):
    """Check if the grammar is simple based on the given conditions."""
    for non_terminal, rule_list in rules.items():
        start_chars = set()
        for rule in rule_list:
            if not rule or rule[0].islower() == False:
                return False  # Rule must start with a lowercase character.
            if rule[0] in start_chars:
                return False  # Rules of the same non-terminal must start with different characters.
            start_chars.add(rule[0])
    return True

def input_grammar ():
    print("\n\U0001F447 Grammars \U0001F447")
    rules = {"S": [], "B": []}

    # Get rules for non-terminals from user
    for non_terminal in rules.keys():
        for i in range(2):
            rule = input(f"Enter rule number {i + 1} for non-terminal '{non_terminal}': ").strip()
            rules[non_terminal].append(rule)

    if is_simple_grammar(rules):
        return rules
    else:
        return None


def check_input(rules):
    input_string = input("Enter the string you want to be checked: ").strip()
    stack = list("S")
    is_accepted,newStack,newInput = parse_string(rules, list(input_string), "S", stack.copy())

    print(f"{Fore.LIGHTYELLOW_EX}The input String: {list(input_string)}")
    print(f"{Fore.LIGHTBLUE_EX}Stack after checking: {newStack}")
    # print(f"Remain Input unchecked: {remain_input}")

    print(f"The rest of unchecked string: {newInput}")
    print(f"{Fore.LIGHTGREEN_EX}Your input String is Accepted. (:" if is_accepted else f"{Fore.LIGHTRED_EX}Your input String is Rejected. ):")


def parse_string(rules, input_string, non_terminal, stack):
    """Recursively parse the input string based on grammar rules."""

    if not input_string and not stack:
        return True,stack,input_string

    if not input_string or not stack:
        return False,stack,input_string


    print(f"{Fore.LIGHTCYAN_EX} --- 1. content of stack : {stack}")
    print(f"{Fore.LIGHTMAGENTA_EX} --- 2. content of input : {input_string}")

    top = stack.pop()  ## pop


    if top.islower():  # Terminal symbol
        if input_string[0] == top:
            ## advance
            return parse_string(rules, input_string[1:], non_terminal, stack)
        else:
            return False,stack,input_string  # Reject

    if top.isupper():  # Non-terminal symbol
        for rule in rules[top]:
            if rule[0] == input_string[0]:
                ## Replace( reversed rule ) and retain
                new_stack = stack + list(reversed(rule))  # Add rule to stack in reverse order
                return parse_string(rules, input_string, non_terminal, new_stack)
    return False,stack,input_string

def main():
    while True:
        rules = input_grammar()
        # Check if the grammar is simple
        if not rules:
            print(f"{Fore.RED}The Grammar isn't simple. Try again.")
            continue
        else:
            print(f"{Fore.GREEN}it is simple")
            check_input(rules)

        while True:
            print("\n1-Another Grammar.\n2-Another String.\n3-Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                break  # Exit to define another grammar

            elif choice == "2":
                check_input(rules)

            elif choice == "3":
                print("Exiting...")
                return

            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
