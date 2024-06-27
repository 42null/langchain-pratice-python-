from colorama import Fore, Back, Style

option_style = Fore.GREEN


def color_test():
    printstr = "ABCDEFGHIJKLMNOPQRSTUVWZYZ0123456789abcdefghijklmnopqrstuvwzyz"
    line = ""
    foreColors = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
    backColors = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
    ci = 0
    for c in printstr:
        if(ci == len(foreColors) - 1):
            ci = 0
        else:
            ci += 1
        line += f"{foreColors[ci]}{c}"
    print(line)
    for b in backColors:
        print(f"{b}{line}{Back.RESET}")

    

def select_one_from_array(message, options):
    print(message, end='')
    i = 1
    generated_options = ""
    for option in options:
        generated_options += f"\n{i}: {option_style}{option}{Style.RESET_ALL}"
        i += 1
    while True:
        print(generated_options)
        rawInput = input(f"Please enter your choice (1-{i-1}): ");
        pick = int(rawInput) if rawInput.isdecimal() else -1
        if(pick in range(1,i)):
            return pick-1
        else:
            print(f"Sorry but you have to pick a number (1-{i-1}). Please try again.", end='')

def get_int_in_range(start, end, for_message="a number", default=None):
    if default is None:
        askMessage = f"Please enter {for_message} as an integer between {start} and {end}"
    else:
        askMessage = f"Please enter {for_message} as an integer between {start} and {end} or leave blank to use {default}"
    while True:
        rawInput = input(askMessage)
        if len(rawInput) == 0 and not default is None:
            return default
        rawInput = int(rawInput) if isinstance(rawInput, int) else None
        if rawInput is None or rawInput < start or rawInput > end:
            print(f"Sorry, {askMessage}. Please try again.", end='')
        else:
            return rawInput

def display_header_text(text):
    print(f"{Back.BLACK}{Fore.BLUE}{Style.BRIGHT}{text}{Style.RESET_ALL}")
def display_update_text(text):
    print(f"{Back.BLACK}{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}")
def display_variable_value(variableName, variableValue):
    print(f"{Style.DIM}{Fore.CYAN}{variableName}{Style.RESET_ALL}: {Style.BRIGHT}{Fore.CYAN}{variableValue}{Style.RESET_ALL}")


def print_debugging_variables(fields):
    print()

    # TODO: Make less repetitive
    max_field_name_width = 0
    max_field_value_width = 0
    for field in fields:
        max_field_name_width = max(max_field_name_width, len(field[0]))
        max_field_value_width = max(max_field_value_width, len(field[1]))

    divider_line = f"{'-' * (max_field_name_width + max_field_value_width + 5)}"
    print(f"-{divider_line}-")
    print(f"| Variables for debugging {' ' * (max_field_name_width + max_field_value_width - 20)}|")
    print(f"|{divider_line}|")

    for field_name, field_value in fields:
        print(f"| {field_name} {'.' * (max_field_name_width - len(field_name))}: {field_value} {' ' * (max_field_value_width - len(field_value))}|")

    print(f"-{divider_line}-\n")
