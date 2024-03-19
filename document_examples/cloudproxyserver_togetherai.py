import autogen
import os

llm_config={
    "config_list": [
        {
            # Available together.ai model strings:
            # https://docs.together.ai/docs/inference-models
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "api_key": os.environ['TOGETHER_API_KEY'],
            "base_url": "https://api.together.xyz/v1"
        }
    ],
    "cache_seed": 42
}

# User Proxy will execute code and finish the chat upon typing 'exit'
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    system_message="A human admin",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="TERMINATE",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content"),
)

# Python Coder agent
coder = autogen.AssistantAgent(
    name="softwareCoder",
    description="Software Coder, writes Python code as required and reiterates with feedback from the Code Reviewer.",
    system_message="You are a senior Python developer, a specialist in writing succinct Python functions.",
    llm_config=llm_config,
)

# Code Reviewer agent
reviewer = autogen.AssistantAgent(
    name="codeReviewer",
    description="Code Reviewer, reviews written code for correctness, efficiency, and security. Asks the Software Coder to address issues.",
    system_message="You are a Code Reviewer, experienced in checking code for correctness, efficiency, and security. Review and provide feedback to the Software Coder until you are satisfied, then return the word TERMINATE",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content"),
    llm_config=llm_config,
)

# Establish the Group Chat and disallow a speaker being selected consecutively
groupchat = autogen.GroupChat(agents=[user_proxy, coder, reviewer], messages=[], max_round=12, allow_repeat_speaker=False)

# Manages the group of multiple agents
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start the chat with a request to write a function
user_proxy.initiate_chat(
    manager,
    message="Write a Python function for the Fibonacci sequence, the function will have one parameter for the number in the sequence, which the function will return the Fibonacci number for."
)
# type exit to terminate the chat