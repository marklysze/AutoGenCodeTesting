# Testing the Function Calling - Local Jupyter - Local LLM
# Based on: https://github.com/microsoft/autogen/blob/main/notebook/agentchat_function_call.ipynb

# Installed: pip install -qqq 'pyautogen[local-jupyter-exec]'

import os
import tempfile
import shutil
from typing_extensions import Annotated
import autogen
from autogen.cache import Cache
from IPython.display import Image
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


ollama_models = [
    {"model_name": "codellama:7b-python", "display_name": "CodeLlama_7b_Python"},
    {"model_name": "codellama:13b-python", "display_name": "CodeLlama_13b_Python"},
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
#    {"model_name": "starcoder2:3b", "display_name" : "StarCoder2_3b"},
#    {"model_name": "starcoder2:7b", "display_name" : "StarCoder2_7b"},
#    {"model_name": "starcoder2:15b", "display_name" : "StarCoder2_15b"},
    {"model_name": "yi:34b-chat-q4_K_M", "display_name" : "Yi_34b_Chat_Q4"},
]

test_prefix = "FnctCall"

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

                chatbot = autogen.AssistantAgent(
                    name="chatbot",
                    system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
                    llm_config={
                        "config_list": [{"model": model_name, "api_key": "NotRequired", "base_url": "http://192.168.0.115:11434/v1"}],
                        "cache_seed": None,
                    },  ## CRITICAL - ENSURE THERE'S NO CACHING FOR TESTING
                )

                # create a UserProxyAgent instance named "user_proxy"
                user_proxy = autogen.UserProxyAgent(
                    name="user_proxy",
                    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
                    human_input_mode="NEVER",
                    max_consecutive_auto_reply=10,
                    code_execution_config={
                        "work_dir": "coding",
                        "use_docker": False,
                    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
                )

                # define functions according to the function description


                # one way of registering functions is to use the register_for_llm and register_for_execution decorators
                @user_proxy.register_for_execution()
                @chatbot.register_for_llm(name="python", description="run cell in ipython and return the execution result.")
                def exec_python(cell: Annotated[str, "Valid Python cell to execute."]) -> str:
                    ipython = get_ipython()
                    result = ipython.run_cell(cell)
                    log = str(result.result)
                    if result.error_before_exec is not None:
                        log += f"\n{result.error_before_exec}"
                    if result.error_in_exec is not None:
                        log += f"\n{result.error_in_exec}"
                    return log


                # another way of registering functions is to use the register_function
                def exec_sh(script: Annotated[str, "Valid Python cell to execute."]) -> str:
                    return user_proxy.execute_code_blocks([("sh", script)])


                autogen.agentchat.register_function(
                    exec_python,
                    caller=chatbot,
                    executor=user_proxy,
                    name="sh",
                    description="run a shell script and return the execution result.",
                )

                # Finally, we initialize the chat that would use the functions defined above:

                with Cache.disk() as cache:

                    today = datetime.datetime.now().strftime("%Y-%m-%d")

                    print(f"-----\n\n{display_name}\n\n{today}\n\nIteration {iteration}\n\n-----\n")

                    # start the conversation
                    user_proxy.initiate_chat(
                        chatbot,
                        message="Draw two agents chatting with each other with an example dialog. Don't add plt.show().",
                        cache=cache,
                    )

        else:
            print(f"{output_file} already exists, ignoring.")

    # break