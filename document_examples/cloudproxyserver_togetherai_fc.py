import os
from typing import Literal
from pydantic import BaseModel, Field
from typing_extensions import Annotated
import autogen

llm_config={
    # Together.ai (supports function calling, requires API key in environment variable "TOGETHER_API_KEY")
    # More info here: https://docs.together.ai/docs/function-calling including the models it supports
    "config_list": [{"model": "mistralai/Mixtral-8x7B-Instruct-v0.1", "api_key": os.environ['TOGETHER_API_KEY'], "base_url": f"https://api.together.xyz/v1"}],

    "cache_seed": None,
}

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="""For currency exchange tasks, 
        only use the functions you have been provided with. 
        Output 'TERMINATE' with the answer to indicate an answer has been provided. 
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
        }.
        When finished, return a non-JSON format string of 'TERMINATE'""",

    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", ""),
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=1,
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

# Test that the function map is the function
# assert user_proxy.function_map["currency_calculator"]._origin == currency_calculator

# start the conversation
res = user_proxy.initiate_chat(
    chatbot,
    message="How much is 123.45 EUR in USD?",
    summary_method="reflection_with_llm",
)