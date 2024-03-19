gemma = {
    "config_list": [
        {
            "model": "lmstudio-ai/gemma-2b-it-GGUF/gemma-2b-it-q8_0.gguf",
            "base_url": "http://192.168.0.115:1234/v1",
            "api_key": "NULL",
        },
    ],
    "cache_seed": None,  # Disable caching.
}

phi2 = {
    "config_list": [
        {
            "model": "TheBloke/phi-2-GGUF/phi-2.Q4_K_S.gguf",
            "base_url": "http://192.168.0.115:1234/v1",
            "api_key": "NULL",
        },
    ],
    "cache_seed": None,  # Disable caching.
}

from autogen.agentchat import ConversableAgent

jack = ConversableAgent(
    "Jack (Phi-2)",
    llm_config=phi2,
    system_message="Your name is Jack and you are a comedian in a two-person comedy show.",
)
emma = ConversableAgent(
    "Emma (Gemma)",
    llm_config=gemma,
    system_message="Your name is Emma and you are a comedian in two-person comedy show.",
)

chat_result = jack.initiate_chat(emma, message="Emma, tell me a joke.", max_turns=2)