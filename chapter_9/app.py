'''
Web service for text generation using a generative AI model -- chapter 9 version.

It extends the previous version from Chapter 5, by adding more primitives for the web service


This is a model module. It contains the logic of using the generative AI model
In particular it contains the following class:
    - TextGenerator: a class to load the model and generate text

This version of the module uses flask to make it into a web service
'''
from flask import Flask, request, jsonify, abort
from transformers import pipeline, AutoTokenizer
import torch

# this is the new part - flask app
app = Flask(__name__)

# this part is the same as the previous model.py
class TextGenerator:
    def __init__(self, model="Qwen/Qwen3-0.6B"):
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

        self.__model__ = model
        self.__tokenizer__ = tokenizer

    def get_model_name(self):
        '''
        Returns the name of the model
        '''
        return self.__model__
    
    def get_tokenizer_name(self):
        '''
        Returns the name of the tokenizer
        '''
        return self.__tokenizer__.name_or_path
    

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
            "max_new_tokens": 200,
            "return_full_text": True,
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

# security via API keys
VALID_API_KEYS = {'AAAAAA', 'BBBBB', 'CCCCC'}

def authenticate():
    api_key = request.headers.get('MS-API-Key')
    if api_key not in VALID_API_KEYS:
        abort(401, 'Unauthorized: Invalid API Key')

# Basic endpoint
@app.route('/')
def home():
    '''
    The / endpoint which returns a simple message
    '''
    return 'Text generator service, please use the /v1/prompt endpoint to generate text, /v1/heartbeat for the heartbeat and /v1/capabilities for info. It is a GET endpoint so use ?seed_text=your_prompt'

# Heartbeat endpoint
@app.route('/v1/heartbeat', methods=['GET'])
def heartbeat():
    '''
    A simple heartbeat endpoint to check if the service is running
    '''
    return jsonify({'status': 'ok', 'message': 'Text generator service is running'}), 200

# capability endpoint
@app.route('/v1/capabilities', methods=['GET'])
def capabilities():
    '''
    A simple endpoint to return the capabilities of the service
    '''
    return jsonify({
        'message': 'Available models',
        'capabilities': {
            'generate_text': 'Generates text based on the provided seed text, enpoint /v1/prompt',
            'model_name': text_generator.get_model_name(),
        }
    }), 200 

@app.route('/v1/restart', methods=['GET'])
def restart():
    '''
    A simple endpoint to restart the service
    '''
    authenticate()  # Ensure the request is authenticated

    text_generator = TextGenerator()
    
    return jsonify({'status': 'ok', 'message': 'Service is restarting...'}), 200


@app.route('/v1/prompt', methods=['GET'])
def generate():
    '''
    Creating the standard route
    which we call prompt and which accepts POST requests
    with a JSON body containing the seed_text
    and returns the generated text
    '''

    # Authenticate the request
    authenticate()  # Ensure the request is authenticated

    # we get the prompt as a parameter
    seed_text = request.args.get('seed_text', '')

    # if it is empty, then we return an error
    if not seed_text:
        return jsonify({'error': 'No prompt provided, use ?seed_text as the parameter'}), 400

    # use the model to generate the text based on the prompt
    generated_text = text_generator.generate_text(seed_text)

    # and return it to the user
    return jsonify({'generated_text': generated_text})

# second version of the endpoint, where we use POST requests
# and accept a JSON payload with the seed_text and optional parameters
@app.route('/v2/prompt', methods=['POST'])
def generate_v2():
    '''
    Version 2 of the generation endpoint that accepts POST requests
    with a JSON payload containing the seed_text and optional generation parameters
    '''

    # Authenticate the request
    authenticate()  # Ensure the request is authenticated

    # Get the JSON payload
    data = request.get_json()
    
    # Check if the payload exists and contains seed_text
    if not data or 'seed_text' not in data:
        return jsonify({
            'error': 'Invalid request',
            'message': 'Please provide a JSON payload with seed_text field'
        }), 400

    seed_text = data['seed_text']

    # Optional parameters with defaults
    generation_params = {
        'max_new_tokens': data.get('max_tokens', 50),
        'return_full_text': data.get('return_full_text', False),
        'do_sample': data.get('do_sample', False),
    }

    try:
        # Generate text with custom parameters
        messages = [{"role": "user", "content": seed_text}]
        output = text_generator.pipe(messages, **generation_params)
        
        return jsonify({
            'generated_text': output[0]['generated_text'],
            'parameters_used': generation_params
        })
    except Exception as e:
        return jsonify({
            'error': 'Generation failed',
            'message': str(e)
        }), 500 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')