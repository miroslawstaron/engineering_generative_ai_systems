'''
View class for the Text Generator application.
This class takes care of the user interface. 
It is a very simple one - a textual interface
'''
from controller import TextController

class TextGeneratorInterfaceText:
    def __init__(self):
        # Initialize the TextController
        self.controller = TextController()

    def generate_text_interface(self, prompt):
        # Generate text using the controller
        return self.controller.generate_text(prompt)

    def launch_interface(self):
        while (True):
            strPrompt = input("Enter a prompt to generate text: ")
            if strPrompt == "exit":
                break
            print("Generated text: ")
            print(self.generate_text_interface(strPrompt))
