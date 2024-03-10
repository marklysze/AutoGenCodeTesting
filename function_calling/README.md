## Function Calling

### Testing Function Calling with local LLMs using LiteLLM and Ollama

#### How to run

1. Install AutoGen (preferably in a virtual environment / dev container)

2. Install [LiteLLM](https://github.com/BerriAI/litellm) and [Ollama](https://github.com/ollama/ollama)

3. `Ollama pull <model name>` your models, suggest trying `DolphinCoder` (e.g. `Ollama pull dolphincoder`)

4. Run LiteLLM using the ollama_chat notation:

    `litellm --model ollama_chat/dolphincoder --port 8801 --debug`

5. Open, `function_calling_test.py`, change `network_address` variable and comment/uncomment under `llm_config` accordingly

6. Run it!