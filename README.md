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
Yi-34b Chat | :white_check_mark: | :white_check_mark: |

#### Stock market chart
Prompt for LLM: **Today is {today}. Write Python code to plot TSLA's and META's stock prices YTD.**

Code should generate: An image for each stock OR an image including both stocks. If it tries to display it (Jupyter notebook) it's a bonus (but doesn't affect whether it's correct or not).

See the [results](results) folder for code outputs.

See what [ChatGPT 3.5 generated](results/Stocks_ChatGPT_3.5.txt) (which was correct).

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
Yi-34b Chat | :x: | :x: | Old retired library use