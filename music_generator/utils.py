import tiktoken
import openai
from ratelimiter import RateLimiter
from retrying import retry

def parse_abc_notations(input_string):
    import re
    pattern = r'```abc\s(.*?)```'
    match = re.search(pattern, input_string, re.DOTALL)
    if match:
        abc_notations = match.group(1)
        return abc_notations
    else:
        return None

def text2token(text: str, encoding: str = "gpt2"):
    """Tokenize a text into a list of tokens.
    
    Ref:
        https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        https://github.com/openai/tiktoken
    """
    encoding = tiktoken.get_encoding(encoding)
    tokens = encoding.encode(text)

    return tokens 

def token2text(tokens: list, encoding: str = "gpt2"):
    """Decode a list of tokens into a text."""
    encoding = tiktoken.get_encoding(encoding)
    text = encoding.decode(tokens)

    return text           

def count_tokens(text: str, encoding: str = "gpt2"):
    """Count the number of tokens in a text.
    
    Ref: 
        https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        https://github.com/openai/tiktoken
    """
    num_tokens = len(text2token(text, encoding))

    return num_tokens

def parse_text_response(openai_text_response, text_engine):
    """According to the text engine, parse the response content.
    
    Different text engine support different response structures
    """
    if "text" in text_engine:
        return openai_text_response.choices[0].text.strip()
    elif "gpt-3.5" in text_engine or "gpt-4" in text_engine:
        return openai_text_response['choices'][0]['message']['content']

def get_model_selection(text_engine):
    """Return the model selection according to the text engine."""
    model_seletection = {
        "gpt-3.5-turbo": {  "model": text_engine},
         "gpt-4": {  "model": text_engine},
        "text-davinci-003": {  "engine": text_engine},
    }
    return model_seletection[text_engine]

def get_engine_method(text_engine):
    """Return the engine method according to the text engine."""
    method_selected = {
        "gpt-3.5-turbo": openai.ChatCompletion.create,
        "gpt-4": openai.ChatCompletion.create,
        "text-davinci-003": openai.Completion.create,
    }
    return method_selected[text_engine]

def format_prompt(original_prompt, text_engine="gpt-3.5"):
    """Format the prompt according to the text engine."""
    if "text" in text_engine:
        return {
            "prompt": original_prompt,
        }
    elif "gpt-3.5" in text_engine or "gpt-4" in text_engine:
        return {
            "messages":[
            {"role": "system", "content": original_prompt}
            ]
        }
    return original_prompt

@retry(stop_max_attempt_number=10)
@RateLimiter(max_calls=20, period=60)
def generate_openai_completion(text_engine, api_settings):
    """Generate the completion using OpenAI API.
    
    Append the model selection and engine method according to the text engine.
    Add rate limiter and retry decorator to avoid the rate limit error.
    Ref: https://community.openai.com/t/continuous-gpt3-api-500-error-the-server-had-an-error-while-processing-your-request-sorry-about-that/42239/30?page=2
    Package: 
        https://github.com/RazerM/ratelimiter
        https://github.com/rholder/retrying
    """
    response=get_engine_method(text_engine)(**api_settings)
    return response