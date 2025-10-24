'''
Main file - starting point of the application.
'''
import argparse
from view import TextGeneratorInterface
from view_text import TextGeneratorInterfaceText

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text Generator Application")
    parser.add_argument("-t", action="store_true", help="Use TextGeneratorInterfaceText")
    parser.add_argument("-g", action="store_true", help="Use TextGeneratorInterface")
    args = parser.parse_args()

    if args.t:
        interface = TextGeneratorInterfaceText()
    elif args.g:
        interface = TextGeneratorInterface()
    else:
        print("Please specify either -t or -g")
        exit(0)

    interface.launch_interface()