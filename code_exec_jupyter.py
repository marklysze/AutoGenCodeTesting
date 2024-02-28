# Testing the Code Executor - Local Jupyter - NO LLM
# Based on: https://github.com/microsoft/autogen/blob/tutorial/website/docs/getting-started/code-executors.ipynb

# Installed: pip install -qqq 'pyautogen[local-jupyter-exec]'

import os
import tempfile
import shutil
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent
from IPython.display import Image

# We create an agent with a local Jupyter code executor, and asks it to generates a reply
# with a given code block in markdown.

# Create a temporary directory to store the code files.
temp_dir = tempfile.mkdtemp()

# Create an agent with code executor configuration for a local Jupyter
# code executor.
jupyter_agent = ConversableAgent(
    name="Jupyter_Agent",
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

# Ask the agent to generate a reply for a message that contains two Python code blocks.

message_with_code_blocks_1 = (
    "First import the required libraries: \n"
    "```python\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "```\n"
    "\n"
    "Now let's generate random numbers.\n"
    "```python\n"
    "np.random.seed(0)\n"
    "x = np.random.rand(100)\n"
    "y = np.random.rand(100)\n"
    "````n"
)

# Generate a reply for the first code message.
reply = jupyter_agent.generate_reply(
    messages=[
        {
            "role": "user",
            "content": message_with_code_blocks_1,
        }
    ]
)
print(reply)

# Ask the agent to generate a reply for a message that contains a Python code block that
# generates a plot using the variables from the code block in the previous message.

message_with_code_blocks_2 = (
    "Now let's plot the random numbers. \n"
    "```python\n"
    "plt.scatter(x, y)\n"
    "plt.xlabel('X')\n"
    "plt.ylabel('Y')\n"
    "plt.title('Random Numbers')\n"
    "plt.show()\n"
    "```\n"
)

# Generate a reply for the second code message.
reply = jupyter_agent.generate_reply(
    messages=[
        {
            "role": "user",
            "content": message_with_code_blocks_2,
        }
    ]
)
print(reply)

# Look at the generated image
output_files = os.listdir(temp_dir)
print(output_files)
Image(os.path.join(temp_dir, output_files[0]))

# Clean up the temporary directory
# shutil.rmtree(temp_dir)
