import os
from typing import Literal
from pydantic import BaseModel, Field
from typing_extensions import Annotated
import autogen

# Requires LiteLLM which supports function calling (though not exactly as OpenAI)
# Running on port 8801 (set in LiteLLM command)
# Run LiteLLM with ollama-chat:
# E.g. $ litellm --model ollama_chat/dolphincoder --port 8801 --debug

# Update to match address for LiteLLM, use "0.0.0.0" if in same environment
network_address = "192.168.0.115"

# LOCAL LOCAL
llm_config={
    # Ollama API (doesn't support function calling)
    # Insert model_name as Ollama model name
#     "config_list": [{"model": model_name, "api_key": "NotRequired", "base_url": f"http://{network_address}:11434/v1"}], 

    # LiteLLM (supports function calling but may have Ollama function calling bug)
#    "config_list": [{"model": "litellmnotneeded", "api_key": "NotRequired", "base_url": f"http://{network_address}:8801"}], 
    
    # Gorilla OpenFunctions
    "config_list": [{"model": "gorilla-7b-hf-v1", "api_key": "EMPTY", "base_url": f"http://zanino.millennium.berkeley.edu:8000/v1"}],

    # Functionary (not tested)
#    "config_list": [{"model": "litellmnotneeded", "api_key": "NotRequired", "base_url": f"http://{network_address}:8000/v1"}], 

    # LM Studio (doesn't support function calling)
#    "config_list": [{"model": "litellmnotneeded", "api_key": "NotRequired", "base_url": f"http://{network_address}:1234/v1"}],

    # Together.ai (supports function calling, requires API key in environment variable "TOGETHER_API_KEY")
    # More info here: https://docs.together.ai/docs/function-calling including the models it supports
#    "config_list": [{"model": "mistralai/Mistral-7B-Instruct-v0.1", "api_key": os.environ['TOGETHER_API_KEY'], "base_url": f"https://api.together.xyz/v1"}],

    "cache_seed": None,
}  ## CRITICAL - ENSURE THERE'S NO CACHING FOR TESTING

'''
# OPENAI OPENAI OPENAI API
# COMMENT OUT WHEN NOT USING OPENAI
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo-0125", "gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
    },
)

# OPENAI OPENAI OPENAI API
# COMMENT OUT WHEN NOT USING OPENAI
llm_config = {
    "config_list": config_list,
    "timeout": 120,
}
'''

chatbot = autogen.AssistantAgent(
    name="chatbot",
# Iteration 1 prompt
#    system_message="""For currency exchange tasks, 
#        only use the functions you have been provided with. 
#        Output 'BAZINGA!' when an answer has been provided. 
#        Include the function name in the JSON. """, # MS - this was needed to ensure the function name was returned

# Iteration 1 prompt
#    system_message="""For currency exchange tasks, 
#        only use the functions you have been provided with. 
#        Output 'BAZINGA!' when an answer has been provided. 
#        Include the function name in the JSON. An example of the return JSON is: 
#        {
#            "function": "the_function_name",
#            "parameters":
#            {                
#                "parameter1": 100.00,
#                "parameter2": "ABC",
#                "parameter3": "DEF",
#                "parameter4": "GHI"
#            } 
#        }.""", # MS - this was needed to ensure the function name was returned

# Iteration 3 prompt
#    system_message="""For currency exchange tasks, 
#        only use the functions you have been provided with. 
#        Output 'BAZINGA!' when an answer has been provided. 
#        An example of the return JSON is: 
#        {
#            "litellmfunction": "the_function_name",
#            "parameters":
#            {                
#                "parameter1": 100.00,
#                "parameter2": "ABC",
#                "parameter3": "DEF",
#            } 
#        }. """, # MS - this was needed to ensure the function name was returned

# Iteration 4, two examples to help guide LLM on response
    system_message="""For currency exchange tasks, 
        only use the functions you have been provided with. 
        Output 'BAZINGA!' when an answer has been provided. 
        Do not include the function name or result in the JSON.
        Example of the return JSON is: 
        {
            "parameter_1_name": 100.00,
            "parameter_2_name": "ABC",
            "parameter_3_name": "DEF",
        }. 
        Another example of the return JSON is: 
        {
            "parameter_1_name": "GHI",
            "parameter_2_name": "ABC",
            "parameter_3_name": "DEF",
            "parameter_4_name": 123.00,
        }. """, # MS - this was needed to ensure the function name was returned

    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    # MS updated to search for BAZINGA! to terminate
    is_termination_msg=lambda x: x.get("content", "") and "BAZINGA!" in x.get("content", ""), # and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=4,
)


CurrencySymbol = Literal["USD", "EUR"]

def exchange_rate(base_currency: CurrencySymbol, quote_currency: CurrencySymbol) -> float:
    if base_currency == quote_currency:
        return 1.0
    elif base_currency == "USD" and quote_currency == "EUR":
        return 1 / 1.1
    elif base_currency == "EUR" and quote_currency == "USD":
        return 1.1
    else:
        raise ValueError(f"Unknown currencies {base_currency}, {quote_currency}")


@user_proxy.register_for_execution()
@chatbot.register_for_llm(description="Currency exchange calculator.")
def currency_calculator(
    base_amount: Annotated[float, "Amount of currency in base_currency"],
    base_currency: Annotated[CurrencySymbol, "Base currency"] = "USD",
    quote_currency: Annotated[CurrencySymbol, "Quote currency"] = "EUR",
) -> str:
    quote_amount = exchange_rate(base_currency, quote_currency) * base_amount
    return f"{format(quote_amount, '.2f')} {quote_currency}"

# print(chatbot.llm_config["tools"])

# Test that the function map is the function
assert user_proxy.function_map["currency_calculator"]._origin == currency_calculator

# start the conversation
res = user_proxy.initiate_chat(
    chatbot,
    message="How much is 123.45 EUR in USD?",
    summary_method="reflection_with_llm",
)