import sys
import json
from openai import OpenAI
import configparser
import logging

# Setup logging to only display warnings or errors
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Read API key from a configuration file
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['openai']['api_key']

# Function to interact with the ChatGPT API
def chat_with_gpt(text, model, system_msg):
    try:
        client = OpenAI(api_key=api_key)
        messages = [{"role": "system", "content": system_msg}]
        messages.append({"role": "user", "content": text})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        # Accessing the response content correctly
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

# Main function to handle CLI interaction
def main():
    # Read system message from a file
    with open('system_msg.txt', 'r') as file:
        system_msg = file.read().strip()

    # Read user input from stdin
    user_input = sys.stdin.read().strip()

    response = chat_with_gpt(user_input, "gpt-4", system_msg)
    sys.stdout.write(response)

if __name__ == "__main__":
    main()