'''
This is a model module. It contains the logic of using the generative AI model
In particular it contains the following class:
    - TextGenerator: a class to load the model and generate text

This version of the module uses flask to make it into a web service
'''
from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer
import torch

# this is the new part - flask app
app = Flask(__name__)

# this part is the same as the previous model.py
class TextGenerator:
    def __init__(self, model="meta-llama/Llama-3.2-1B"):
        '''
        Initializes the TextGenerator with the given model and tokenizer
        '''
        # Load the model and tokenizer
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        tokenizer = AutoTokenizer.from_pretrained(model)

        self.pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=self.device
        )

    def generate_text(self, seed_text):
        '''
        Generates text using the model
        '''
        # Generate text using the model
        prompt = seed_text

        messages = [
            {"role": "user", "content": prompt},
        ]

        generation_args = {
            "max_new_tokens": 50,
            "return_full_text": False,
            "do_sample": False,
        }

        output = self.pipe(messages, **generation_args)
        
        return output[0]['generated_text']
    
# Here comes the new part - the flask app

'''
Create an instance of the TextGenerator
which is needed as the model is loaded only once
and then used to generate text
'''
text_generator = TextGenerator()


@app.route('/prompt', methods=['GET'])
def generate():
    '''
    Creating the standard route
    which we call prompt and which accepts POST requests
    with a JSON body containing the seed_text
    and returns the generated text
    '''
    # we get the prompt as a parameter
    seed_text = request.args.get('seed_text', '')

    # if it is empty, then we return an error
    if not seed_text:
        return jsonify({'error': 'No prompt provided, use ?seed_text as the parameter'}), 400

    # use the model to generate the text based on the prompt
    generated_text = text_generator.generate_text(seed_text)

    # and return it to the user
    return jsonify({'generated_text': generated_text})

 
@app.route('/')
def home():
    '''
    The / endpoint which returns a simple message
    '''
    return 'Text generator service, please use the /prompt endpoint to generate text. It is a GET endpoint so use ?seed_text=your_prompt'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)