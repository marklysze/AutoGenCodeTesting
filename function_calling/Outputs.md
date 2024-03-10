### LiteLLM + Ollama serving DolphinCoder

Successfully formulated function call with name and parameters. Didn't put in termination keyword, so just looped.
```
user_proxy (to chatbot):

How much is 123.45 EUR in USD?

--------------------------------------------------------------------------------
chatbot (to user_proxy):

***** Suggested tool Call (call_484a553c-02db-48b3-b802-8ff754928b68): currency_calculator *****
Arguments: 
{
  "base_amount": 123.45, 
  "base_currency": "EUR", 
  "quote_currency": "USD"
}


************************************************************************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION currency_calculator...
user_proxy (to chatbot):

user_proxy (to chatbot):

***** Response from calling tool "call_484a553c-02db-48b3-b802-8ff754928b68" *****
135.80 USD
**********************************************************************************

--------------------------------------------------------------------------------
chatbot (to user_proxy):

***** Suggested tool Call (call_db1de933-ae79-4f6a-864f-f29f29e61147): currency_calculator *****
Arguments: 
{
  "base_amount": 123.45,
  "base_currency": "EUR",
  "quote_currency": "USD"
}


************************************************************************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION currency_calculator...
user_proxy (to chatbot):

user_proxy (to chatbot):

***** Response from calling tool "call_db1de933-ae79-4f6a-864f-f29f29e61147" *****
135.80 USD
**********************************************************************************

--------------------------------------------------------------------------------
chatbot (to user_proxy):

***** Suggested tool Call (call_c178f754-bab0-4e1f-8898-045005ebd24c): currency_calculator *****
Arguments: 
{
  "base_amount": 123.45,
  "base_currency": "EUR",
  "quote_currency": "USD"
}


************************************************************************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION currency_calculator...
user_proxy (to chatbot):

user_proxy (to chatbot):

***** Response from calling tool "call_c178f754-bab0-4e1f-8898-045005ebd24c" *****
135.80 USD
**********************************************************************************

--------------------------------------------------------------------------------
chatbot (to user_proxy):

***** Suggested tool Call (call_e6ea5ed8-d1e6-4b77-886a-0363239bd6a9): currency_calculator *****
Arguments: 
{
  "base_amount": 123.45,
  "base_currency": "EUR",
  "quote_currency": "USD"
}


************************************************************************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION currency_calculator...
user_proxy (to chatbot):

user_proxy (to chatbot):

***** Response from calling tool "call_e6ea5ed8-d1e6-4b77-886a-0363239bd6a9" *****
135.80 USD
**********************************************************************************

--------------------------------------------------------------------------------
chatbot (to user_proxy):

***** Suggested tool Call (call_4df478a3-94bf-4d9f-bd4e-6f82730a46c3): currency_calculator *****
Arguments: 
{
  "base_amount": 123.45,
  "base_currency": "EUR",
  "quote_currency": "USD"
}
************************************************************************************************

--------------------------------------------------------------------------------```

### together.ai serving Mistral-7B-Instruct-v0.1

Successfully formulated function call with name and parameters. Didn't put in termination keyword, so just looped.
```
user_proxy (to chatbot):

How much is 123.45 EUR in USD?

--------------------------------------------------------------------------------
chatbot (to user_proxy):

***** Suggested tool Call (call_03ge36wpqxvxq20uuc9jcc7c): currency_calculator *****
Arguments: 
{"base_amount":123.45,"base_currency":"EUR","quote_currency":"USD"}
************************************************************************************

--------------------------------------------------------------------------------

>>>>>>>> EXECUTING FUNCTION currency_calculator...
user_proxy (to chatbot):

user_proxy (to chatbot):

***** Response from calling tool "call_03ge36wpqxvxq20uuc9jcc7c" *****
135.80 USD
**********************************************************************

--------------------------------------------------------------------------------
chatbot (to user_proxy):

 To convert 135.80 USD to EUR, you can use the following formula:

1 USD = 0.85 EUR

So, to convert 135.80 USD to EUR, you can multiply it by 0.85:

135.80 USD x 0.85 = 114.24 EUR

Therefore, 135.80 USD is equivalent to 114.24 EUR.

--------------------------------------------------------------------------------
user_proxy (to chatbot):



--------------------------------------------------------------------------------
chatbot (to user_proxy):

 To convert 135.80 USD to EUR, you can use the following formula:

1 USD = 0.85 EUR

So, to convert 135.80 USD to EUR, you can multiply it by 0.85:

135.80 USD x 0.85 = 114.24 EUR

Therefore, 135.80 USD is equivalent to 114.24 EUR.

--------------------------------------------------------------------------------
user_proxy (to chatbot):



--------------------------------------------------------------------------------
chatbot (to user_proxy):

 To convert 135.80 USD to EUR, you can use the following formula:

1 USD = 0.85 EUR

So, to convert 135.80 USD to EUR, you can multiply it by 0.85:

135.80 USD x 0.85 = 114.24 EUR

Therefore, 135.80 USD is equivalent to 114.24 EUR.

--------------------------------------------------------------------------------
user_proxy (to chatbot):



--------------------------------------------------------------------------------
chatbot (to user_proxy):

 To convert 135.80 USD to EUR, you can use the following formula:

1 USD = 0.85 EUR

So, to convert 135.80 USD to EUR, you can multiply it by 0.85:

135.80 USD x 0.85 = 114.24 EUR

Therefore, 135.80 USD is equivalent to 114.24 EUR.

--------------------------------------------------------------------------------
```