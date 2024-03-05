# Testing TERMINATE after a group chat - Local LLM
# Based on: (NEW)

import os
import autogen
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
#     {"model_name": "starcoder2:3b", "display_name" : "StarCoder2_3b"},
#     {"model_name": "starcoder2:7b", "display_name" : "StarCoder2_7b"},
#     {"model_name": "starcoder2:15b", "display_name" : "StarCoder2_15b"},
    {"model_name": "yi:34b-chat-q4_K_M", "display_name" : "Yi_34b_Chat_Q4"},
]


# The word we're looking for the LLM to return to terminate the chat.
# Our custom termination message function is a "contains" not "equals", so the word can be anywhere
# in the LLM response. It is, however, case-sensitive.
# If we use "TERMINATE" then it will utilise the under-lying termination check as well. Although
# that requires the whole response to be just: TERMINATE
termination_words = ["DONESKI", "BAZINGA!","AUTOGENDONE", "ACBDEGFHIKJL", "TERMINATE"]

test_prefix = "Term"

# Our termination function
def termination_msg_function(x):

    # Output the whole/part match so we've got it in the output file.
    if isinstance(x, dict) and str(x.get("content")) == {termination_word}:
        print(f"<-- Termination word '{termination_word}' matches WHOLE response -->")
    elif isinstance(x, dict) and f"{termination_word}" in str(x.get("content")):
        print(f"<-- Termination word '{termination_word}' in PART OF response -->")

    is_termination = isinstance(x, dict) and f"{termination_word}" in str(x.get("content"))
    return is_termination

for ollama_model in ollama_models:

    model_name = ollama_model["model_name"]
    display_name = ollama_model["display_name"]

    # Loop through the termination words
    for termination_word in termination_words:

        # Two iterations per model.
        for iteration in range(1, 3):

            output_file = f"/home/autogen/autogen/ms_working/results/{test_prefix}_{display_name}_{termination_word}_i{iteration}.txt"

            if not os.path.exists(output_file):

                # Clear the terminal (Unix/Linux/MacOS)
                os.system('clear')

                with Tee(output_file, 'w'):

                    # Set the config as our local model
                    llm_config={
                        "config_list": [{"model": model_name, "api_key": "NotRequired", "base_url": "http://192.168.0.115:11434/v1"}],
                        "cache_seed": None,
                    }  ## CRITICAL - ENSURE THERE'S NO CACHING FOR TESTING

                    user_proxy = autogen.UserProxyAgent(
                        name="User_proxy",
                        system_message="A human admin.",
                        is_termination_msg=termination_msg_function, # Here's our termination function
                        code_execution_config=False,
                        human_input_mode="NEVER",
                    )
                    storywriter = autogen.AssistantAgent(
                        name="Story_writer",
                        system_message="An ideas person, loves coming up with ideas for kids books.",
                        llm_config=llm_config,
                    )
                    pm = autogen.AssistantAgent(
                        name="Product_manager",
                        system_message=f"""Great in evaluating story ideas from your writers and determining whether they would be unique and interesting for kids.
                            Reply with suggested improvements if they aren't good enough, otherwise
                            reply `{termination_word}` at the end when you're satisfied there's one good story idea.""",
                        llm_config=llm_config,
                    )
                    groupchat = autogen.GroupChat(agents=[user_proxy, storywriter, pm], messages=[], max_round=8,
                        # For the purposes of the test we'll go around in circles, we're not testing the speaker selection.
                        speaker_selection_method='round_robin')
                    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

                    # Here is an example of solving a math problem through a conversation between the code writer and the code executor:

                    today = datetime.datetime.now().strftime("%Y-%m-%d")

                    print(f"-----\n\n{display_name}\n\n{today}\n\nIteration {iteration}\n\nTerminating on '{termination_word}'\n\n-----\n")

                    chat_result = user_proxy.initiate_chat(
                        manager, message="Come up with 3 story ideas for Grade 3 kids."
                    )

            else:
                print(f"{output_file} already exists, ignoring.")

        # break