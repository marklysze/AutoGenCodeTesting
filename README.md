Testing Code Generation using alt-models (Local LLMs)

Two tests so far - Fibonacci function and stock market chart. More to come.

## Code Executors

### Juypter Notebook (local)
[Basis for testing code here](https://github.com/microsoft/autogen/blob/tutorial/website/docs/getting-started/code-executors.ipynb)

#### Fibonacci
Prompt for LLM: **Write Python code to calculate the 14th Fibonacci number.**

Code should generate: **233** or **377**

Note: Fn for n = 14 is 377. If we start at n = 0 the 14th number is 233, so n = 14 is actually the 15th Fibonacci number in the sequence. Therefore, some LLM's code will generate 233 and some 377. We will accept both as the question is ambiguous.

See the [results](results) folder for code outputs.

See what [ChatGPT 3.5 generated](results/Fib_ChatGPT_3.5.txt) (which output 377).

| | Key |
| --- | --- |
| :white_check_mark: | Valid code and formatting |
| :x: | Invalid code, formatting, or didn't understand task |

**Model** | **Run 1** | **Run 2** | **Notes**
---|---|---|---|
CodeLlama 7b Python | :x: | :x: |
CodeLlama 13b Python | :x: | :x: |
CodeLlama 34b Instruct | :white_check_mark: | :white_check_mark: |
CodeLlama 34b Python | :x: | :x: |
DeepSeek Coder 6.7b | :white_check_mark:| :white_check_mark:|
Llama2 7b Chat | :white_check_mark: | :x: |
Llama2 13b Chat | :white_check_mark: | :white_check_mark: |
Mistral 7b 0.2 Instruct | :white_check_mark: | :white_check_mark: |
Mixtral 8x7b Q4 | :white_check_mark: | :white_check_mark:|
Mixtral 8x7b Q5 | :white_check_mark: | :white_check_mark: |
Neural Chat 7b Chat | :white_check_mark: | :white_check_mark: |
Nexus Raven | :x: | :white_check_mark: |
OpenHermes 7b Mistral | :white_check_mark: | :white_check_mark: |
Orca2 13b | :white_check_mark: | :x: |
Phi-2 | :white_check_mark: | :x: |
Phind-CodeLlama34b | :white_check_mark: | :white_check_mark: |
Qwen 14b | :white_check_mark: | :white_check_mark: |
Solar 10.7b Instruct | :x: | :white_check_mark: |
StarCoder2 3b |  |  |
StarCoder2 7b |  |  |
StarCoder2 15b |  |  |
Yi-34b Chat | :white_check_mark: | :white_check_mark: |

#### Stock market chart
Prompt for LLM: **Today is {today}. Write Python code to plot TSLA's and META's stock prices YTD.**

Code should generate: An image for each stock OR an image including both stocks. If it tries to display it (Jupyter notebook) it's a bonus (but doesn't affect whether it's correct or not).

See the [results](results) folder for code outputs.

See what [ChatGPT 3.5 generated](results/Stocks_ChatGPT_3.5.txt) (which was correct).

| | Key |
| --- | --- |
| :white_check_mark: | Valid code and formatting |
| :large_orange_diamond: | Almost correct |
| :x: | Invalid code, formatting, or didn't understand task |

**Model** | **Run 1** | **Run 2** | **Notes**
---|---|---|---|
CodeLlama 7b Python | :x: | :x: |
CodeLlama 13b Python | :large_orange_diamond: | :x: | Just missing "import pandas as pd"
CodeLlama 34b Instruct | :white_check_mark: | :white_check_mark: |
CodeLlama 34b Python | :x: | :x: | Expected a CSV file
DeepSeek Coder 6.7b | :large_orange_diamond: | :white_check_mark: | Out of date library usage
Llama2 7b Chat | :x: | :large_orange_diamond: | Close, showed price change instead of price
Llama2 13b Chat | :x: | :x: |
Mistral 7b 0.2 Instruct | :large_orange_diamond: | :large_orange_diamond: | Minor string formatting error, used "FB" instead of "META" as ticker symbol
Mixtral 8x7b Q4 | :white_check_mark: | :x: |
Mixtral 8x7b Q5 | :white_check_mark: | :large_orange_diamond: | Not quite right on second run
Neural Chat 7b Chat | :x: | :x: |
Nexus Raven | :x: | :x: | First run no code, second is a blank chart
OpenHermes 7b Mistral | :x: | :x: |
Orca2 13b | :x: | :x: | No code
Phi-2 | :x: | :x: | Off the track
Phind-CodeLlama34b | :white_check_mark: | :x: |
Qwen 14b | :large_orange_diamond: | :x: | Timeframe out
Solar 10.7b Instruct | :x: | :x: |
StarCoder2 3b |  |  |
StarCoder2 7b |  |  |
StarCoder2 15b |  |  |
Yi-34b Chat | :x: | :x: | Old retired library use

#### Function Calling
Prompt for LLM: **Draw two agents chatting with each other with an example dialog. Don't add plt.show().**

Code should generate: Python code that creates a diagram with two agents on it (E.g. two circles and speech bubbles)

See the [results](results) folder for code outputs.

See what [OpenAI's API generated](https://github.com/microsoft/autogen/blob/main/notebook/agentchat_function_call.ipynb).

| | Key |
| --- | --- |
| :white_check_mark: | Valid code and formatting |
| :large_orange_diamond: | Almost correct |
| :x: | Invalid code, formatting, or didn't understand task |

**Model** | **Run 1** | **Run 2** | **Notes**
---|---|---|---|
CodeLlama 7b Python | :x: | :x: |
CodeLlama 13b Python | :x: | :x: |
CodeLlama 34b Instruct | :x: | :large_orange_diamond: | Coded an animation with speech bubbles, bug in function parameters, once fixed produced animated text.
CodeLlama 34b Python | :x: | :x: |
DeepSeek Coder 6.7b | :x: | :x: | Produced a chat conversation
Llama2 7b Chat | :x: | :x: | Produced a chat conversation
Llama2 13b Chat | :x: | :x: | Produced a chat conversation
Mistral 7b 0.2 Instruct | :x: | :x: | Produced a chat conversation
Mixtral 8x7b Q4 | :x: | :x: | Produced a chat conversation
Mixtral 8x7b Q5 | :x: | :x: | Produced a chat conversation
Neural Chat 7b Chat | :x: | :x: | Tried to create visual animation but failed and ended up producing a chat conversation
Nexus Raven | :x: | :x: | 
OpenHermes 7b Mistral | :x: | :x: | Produced a chat conversation
Orca2 13b | :x: | :x: |
Phi-2 | :x: | :x: |
Phind-CodeLlama34b | :large_orange_diamond: | :large_orange_diamond: | Valid visual generation of two agents' text chat (no imagery just text on a figure)
Qwen 14b | :x: | :x: | Produced a chat conversation
Solar 10.7b Instruct | :x: | :x: | Produced a chat conversation
StarCoder2 3b |  |  |
StarCoder2 7b |  |  |
StarCoder2 15b |  |  |
Yi-34b Chat | :large_orange_diamond: | :large_orange_diamond: | Close to a valid drawing, outdated libraries

---
---

### Non-coding tests

#### Termination word
Background: Tests the ability for an LLM to incorporate a termination word into their response.

Scenario: Uses a Group Chat with a Story_writer and a Product_manager. Story_writer is to write some story ideas and the Product_manager is to review and terminate when satisified by outputting a specific word (e.g. "TERMINATE", "BAZINGA", etc.).

Store_writer's system message: **An ideas person, loves coming up with ideas for kids books.**

Product_manager's system message: **Great in evaluating story ideas from your writers and determining whether they would be unique and interesting for kids. Reply with suggested improvements if they aren't good enough, otherwise reply `{termination_word}` at the end when you're satisfied there's one good story idea.**

Prompt for the chat manager: **Come up with 3 story ideas for Grade 3 kids.**

See the [results](results) folder for code outputs.

Note 1: `TERMINATE` is the standard used by AutoGen.
Note 2: Some LLMs included the terminating word but the quality of the full response was not perfect.

| | Key |
| --- | --- |
| :white_check_mark: | Included termination word correctly |
| :x: | Performed task, didn't output termination word |
| :thumbsdown: | Didn't understand/participate in task |

There were two runs for each word.

**Model** | **TERMINATE** | **ACBDEGFHIKJL** | **AUTOGENDONE** | **BAZINGA!** | **DONESKI** | **Notes**
---|---|---|---|---|---|---|
CodeLlama 7b Python | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | |
CodeLlama 13b Python | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | |
CodeLlama 34b Instruct | :white_check_mark: :white_check_mark: | :x: :white_check_mark: | :x: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :x: | |
CodeLlama 34b Python | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | |
DeepSeek Coder 6.7b | :x: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | |
Llama2 7b Chat | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Llama2 13b Chat | :x: :white_check_mark: | :x: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Mistral 7b 0.2 Instruct | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Mixtral 8x7b Q4 | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Mixtral 8x7b Q5 | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Neural Chat 7b Chat | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Nexus Raven | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | :thumbsdown: :thumbsdown: | Tried to call a python function to create the stories |
OpenHermes 7b Mistral | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Orca2 13b | :white_check_mark: :white_check_mark: | :x: :white_check_mark: | :x: :white_check_mark: | :x: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Phi-2 | :thumbsdown: :thumbsdown: | :thumbsdown: :x: | :x: :x: | :x: :x: | :x: :thumbsdown: | |
Phind-CodeLlama34b | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Qwen 14b | :x: :x: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
Solar 10.7b Instruct | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
StarCoder2 3b | | | | | | |
StarCoder2 7b | | | | | | |
StarCoder2 15b | | | | | | |
Yi-34b Chat | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | :white_check_mark: :white_check_mark: | |
