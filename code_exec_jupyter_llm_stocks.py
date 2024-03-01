# Testing the Code Executor - Local Jupyter - Local LLM - Stock Prices
# Based on: https://github.com/microsoft/autogen/blob/tutorial/website/docs/getting-started/code-executors.ipynb

# Installed: pip install -qqq 'pyautogen[local-jupyter-exec]'

import os
import tempfile
import shutil
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent
import datetime
import sys # Redirecting standard output to a file instead


# Duplicate output to file and screen
class Tee:
    def __init__(self, file_name, mode='w'):
        self.file = open(file_name, mode)
        self.stdout = sys.stdout

    def __enter__(self):
        sys.stdout = self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.file.flush()

    def close(self):
        if self.file:
            self.file.close()
        sys.stdout = self.stdout

# The code writer agent can be powered by an LLM such as GPT-4 with code-writing capability.
# And the code executor agent is powered by a code executor.

# The following is an agent with a code writer role specified using system_message.

# The code writer agent's system message is to instruct the LLM on how to
# use the Jupyter code executor with IPython kernel.
code_writer_system_message = (
    "You have been given coding capability to solve tasks using Python code in a stateful IPython kernel.\n"
    "You are responsible for writing the code, and the user is responsible for executing the code.\n"
    "\n"
    "When you write Python code, put the code in a markdown code block with the language set to Python.\n"
    "For example:\n"
    "```python\n"
    "x = 3\n"
    "```\n"
    "You can use the variable `x` in subsequent code blocks.\n"
    "```python\n"
    "print(x)\n"
    "```\n"
    "\n"
    "Write code incrementally and leverage the statefulness of the kernel to avoid repeating code.\n"
    "Import libraries in a separate code block.\n"
    "Pip install any required libraries.\n" # MS ADDED
    "Define a function or a class in a separate code block.\n"
    "Run code that produces output in a separate code block.\n"
    "Run code that involves expensive operations like download, upload, and call external APIs in a separate code block.\n"
    "\n"
    "When your code produces an output, the output will be returned to you.\n"
    "Because you have limited conversation memory, if your code creates an image,\n"
    "the output will be a path to the image instead of the image itself.\n"
)

ollama_models = [
    {"model_name": "codellama:34b-instruct", "display_name": "CodeLlama_34b_Instruct"},
    {"model_name": "codellama:34b-python", "display_name": "CodeLlama_34b_Python"},
    {"model_name": "deepseek-coder:6.7b-instruct-q6_K", "display_name": "DeepSeek_Coder"},
    {"model_name": "llama2:13b-chat", "display_name" : "Llama2_13b_Chat"},
    {"model_name": "llama2:7b-chat-q6_K", "display_name": "Llama2_7b_Chat"},
    {"model_name": "mistral:7b-instruct-v0.2-q6_K", "display_name" : "Mistral_7b_Instruct_v2"},
    {"model_name": "mixtralq4", "display_name" : "Mixtral_8x7b_Q4"},
    {"model_name": "mixtralq5", "display_name" : "Mixtral_8x7b_Q5"},
    {"model_name": "neural-chat:7b-v3.3-q6_K", "display_name" : "Neural_Chat_7b"},
    {"model_name": "nexusraven", "display_name" : "Nexus_Raven"},
    {"model_name": "openhermes:7b-mistral-v2.5-q6_K", "display_name" : "OpenHermes_7b_Mistral_v25"},
    {"model_name": "orca2:13b-q5_K_S", "display_name" : "Orca2_13b"},
    {"model_name": "phi", "display_name" : "Phi"},
    {"model_name": "phind-codellama:34b-v2", "display_name" : "Phind_CodeLlama_34b_v2"},
    {"model_name": "qwen:14b-chat-q6_K", "display_name" : "Qwen_14b_Chat"},
    {"model_name": "solar:10.7b-instruct-v1-q5_K_M", "display_name" : "Solar_107b_Instruct"},
    {"model_name": "yi:34b-chat-q4_K_M", "display_name" : "Yi_34b_Chat_Q4"},
]

test_prefix = "Stocks"

for ollama_model in ollama_models:

    model_name = ollama_model["model_name"]
    display_name = ollama_model["display_name"]

    # Two iterations per model.
    for iteration in range(1, 3):

        output_file = f"/home/autogen/autogen/ms_working/results/{test_prefix}_{display_name}_i{iteration}.txt"

        if not os.path.exists(output_file):

            # Clear the terminal (Unix/Linux/MacOS)
            os.system('clear')

            with Tee(output_file, 'w'):

                # MS - LLM will be the one running on the host machine (Ollama)
                code_writer_agent = ConversableAgent(
                    "code_writer",
                    system_message=code_writer_system_message,
                    llm_config={
                        "config_list": [{"model": model_name, "api_key": "NotRequired", "base_url": "http://192.168.0.115:11434/v1"}],
                        "cache_seed": None,
                    },  ## CRITICAL - ENSURE THERE'S NO CACHING FOR TESTING
                    code_execution_config=False,  # Turn off code execution for this agent.
                )

                # Create a temporary directory to store the output images.
                temp_dir = tempfile.mkdtemp()

                # Create an agent with code executor configuration for a local Jupyter
                # code executor.
                code_executor_agent = ConversableAgent(
                    name="code_executor_agent",
                    llm_config=False,
                    code_execution_config={
                        "executor": "jupyter-local",  # Use the local Jupyter executor.
                        # On Windows use "ipython-embedded" instead of "jupyter-local"
                        # due to a known issue with Jupyter Kernel Gateway on Windows.
                        "jupyter-local": {
                            "timeout": 60,  # Timeout for each code execution in seconds.
                            "kernel_name": "python3",  # Use the Python 3 kernel, which is the default.
                            "output_dir": temp_dir,  # Use the temporary directory to store output images.
                        },
                    },
                    human_input_mode="ALWAYS",
                )

                # Now we can try a more complex example that involves querying the web. Let's say we want to get the the stock
                # prices year-to-date for Tesla and Meta (formerly Facebook). We can also use the two agents with several iterations
                # of conversation.

                today = datetime.datetime.now().strftime("%Y-%m-%d")

                print(f"-----\n\n{display_name}\n\n{today}\n\nIteration {iteration}\n\n-----\n")

                chat_result = code_executor_agent.initiate_chat(
                    code_writer_agent, message=f"Today is {today}. Write Python code to plot TSLA's and META's stock prices YTD."
                )
                # Clean up the temporary directory and restart the Jupyter server to free up the kernel resources.

                # Clean up for next round
                shutil.rmtree(temp_dir)
                code_executor_agent.code_executor.restart()

        else:
            print(f"{output_file} already exists, ignoring.")
        # break