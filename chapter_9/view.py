'''
View class for the Text Generator application.
This class takes care of the user interface. 
Please note that it only interacts with the controller class. 
It is the controller class that implements the actual logic of the application.
'''
import gradio as gr
from controller import TextController

class TextGeneratorInterface:
    def __init__(self):
        # Initialize the TextController
        self.controller = TextController()

    def generate_text_interface(self, prompt):
        # Generate text using the controller
        return self.controller.generate_text(prompt)

    def launch_interface(self):
        # Create Gradio interface
        iface = gr.Interface(
            fn=self.generate_text_interface,
            inputs="text",
            outputs="text",
            title="Text Generator",
            description="Enter a prompt to generate text."
        )
        # Launch the interface
        iface.launch()