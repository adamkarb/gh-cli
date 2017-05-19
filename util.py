import sys

def prompt(question, raw):
    user_input = input(question + '\n> ')
    if raw:
        return user_input
    else:
        return user_input.lower().strip()

def debug(message):
    if '--debug' in sys.argv:
        print('+ ' + message)
