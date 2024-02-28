# Testing the Code Executor - Local Command Line - NO LLM
# Based on: https://github.com/microsoft/autogen/blob/tutorial/website/docs/getting-started/code-executors.ipynb

import os
import tempfile
import shutil
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent

# Here is an example of using the local command line code executor to run a Python code block that
# prints a random number. First we create an agent with the local command line code executor that
# uses a temporary directory to store the code files.

# Create a temporary directory to store the code files.
temp_dir = tempfile.mkdtemp()

# Create an agent with code executor configuration for a local command line
# code executor.
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={
        "executor": "commandline-local",  # Use the local command line executor.
        "commandline-local": {
            "timeout": 10,  # Timeout for each code execution in seconds.
            "work_dir": temp_dir,  # Use the temporary directory to store the code files.
        },
    },
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)

# Now we have the agent generate a reply given a message with a Python code block.

message_with_code_block = (
    "This is a message with code block. "
    "The code block is below: \n"
    "```python\n"
    "import random\n"
    "print('A Random Number: ', random.randint(1, 100))\n"
    "```\n"
    "This is the end of the message.\n"
)

# Generate a reply for the given code.
reply = code_executor_agent.generate_reply(messages=[{"role": "user", "content": message_with_code_block}])
print(reply)

# Look at the temporary file created
print("Temporary file created and contents:")
code_files = os.listdir(temp_dir)
print(code_files)
print(open(os.path.join(temp_dir, code_files[0])).read())

# Clean up the temporary directory
shutil.rmtree(temp_dir)
