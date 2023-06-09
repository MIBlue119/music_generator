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
    TEXT_ENGINE = text_engine_choices["gpt-3.5-turbo"]
    TEXT_ENGINE_TEMPERATURE = 0.5
    TEXT_ENGINE_MAX_TOKENS = 2048

    @classmethod    
    def set_text_engine(cls, text_engine):
        cls.TEXT_ENGINE = text_engine_choices[text_engine]

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY', None)
openai.api_key = openai_api_key