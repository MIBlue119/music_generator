"""Define the app's configuration.
"""
import os
import openai
from dotenv import load_dotenv

text_engine_choices = {
    "text-davinci-003": "text-davinci-003",
    "gpt-3.5-turbo": "gpt-3.5-turbo",
    "gpt-4": "gpt-4",
}  
class AppConfig:
    TEXT_ENGINE = text_engine_choices["gpt-4"]
    TEXT_ENGINE_TEMPERATURE = 0.5

    def set_text_engine(self, text_engine):
        self.TEXT_ENGINE = text_engine_choices[text_engine]

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY', None)
if openai_api_key is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")
openai.api_key = openai_api_key