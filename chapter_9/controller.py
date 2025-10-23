'''
Controller class, which takes care of the user input.
It checks if the input is correct and then calls the model to generate the text.

This implementation uses the requests library to make a GET request to the web service.
The web service is now created as the new model.py
'''

import requests

class TextController:
    def __init__(self, api_url="http://localhost:5000/prompt"):
        # Initialize the API URL
        self.api_url = api_url

    def generate_text(self, prompt):
        # Check if the prompt is less than 512 words
        if len(prompt.split()) > 512:
            raise ValueError("Prompt is too long. Please provide a prompt with less than 512 words.")
        
        # Make a GET request to the web service
        response = requests.get(self.api_url, params={'seed_text': prompt})
        
        # Check if the request was successful
        if response.status_code != 200:
            raise ValueError(f"Error: {response.json().get('error', 'Unknown error')}")
        
        # Return the generated text
        return response.json().get('generated_text', '')