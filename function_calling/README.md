## Function Calling

### Testing Function Calling with local LLMs using LiteLLM and Ollama

#### How to run

1. Install AutoGen (preferably in a virtual environment / dev container)

2. Install [LiteLLM](https://github.com/BerriAI/litellm) and [Ollama](https://github.com/ollama/ollama)

3. `Ollama pull <model name>` your models, suggest trying `DolphinCoder` (e.g. `Ollama pull dolphncoder`)

4. Run LiteLLM using the ollama_chat notation:

    `litellm --model ollama_chat/dolphincoder --port 8801 --debug`

5. Run `function_calling_test.py` and run it