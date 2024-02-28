# Testing the Code Executor - Local Jupyter - Local LLM
# Based on: https://github.com/microsoft/autogen/blob/tutorial/website/docs/getting-started/code-executors.ipynb

# Installed: pip install -qqq 'pyautogen[local-jupyter-exec]'

import os
import tempfile
import shutil
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent
from IPython.display import Image

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
    "Define a function or a class in a separate code block.\n"
    "Run code that produces output in a separate code block.\n"
    "Run code that involves expensive operations like download, upload, and call external APIs in a separate code block.\n"
    "\n"
    "When your code produces an output, the output will be returned to you.\n"
    "Because you have limited conversation memory, if your code creates an image,\n"
    "the output will be a path to the image instead of the image itself.\n"
)

# MS - LLM will be the one running on my machine using liteLLM, port 8801, name doesn't mean anything in this case.
# Command to run LiteLLM: litellm --model ollama/phind-codellama:34b-v2 --port 8801
code_writer_agent = ConversableAgent(
    "code_writer",
    system_message=code_writer_system_message,
    llm_config={
        "config_list": [{"model": "Local8801", "api_key": "NotRequired", "base_url": "http://192.168.0.115:8801"}],
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

# Here is an example of solving a math problem through a conversation between the code writer and the code executor:

chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message="Write Python code to calculate the 14th Fibonacci number.",
)

# Clean up the temporary directory and restart the Jupyter server to free up the kernel resources.

shutil.rmtree(temp_dir)
code_executor_agent.code_executor.restart()
