Testing Code Generation using alt-models (Local LLMs)

See the results folder for outputs and summaries.

Testing so far...

## Code Executors

### Juypter Notebook (local)
[Basis for testing code here](https://github.com/microsoft/autogen/blob/tutorial/website/docs/getting-started/code-executors.ipynb)

#### Fibonacci
**Model** | **Success** | **Notes**
---|---|---|
DeepSeek Coder 6.7b| :white_check_mark:|
Llama2 7b Chat| :x:| Created code that required "fibonacci" library to be installed and gave instructions on how to install. Tried it and the library and code didn't work, returned 0
Llama2 13b Chat| :white_check_mark:|
Mistral 7b 0.2 Instruct| :white_check_mark:|
Mixtral 8x7b Q4| :white_check_mark:|
Mixtral 8x7b Q5| :white_check_mark:| Tidier than Q4
Neural Chat 7b Chat| :white_check_mark:| Fast
Nexus Raven| :x:| Tried twite
Orca2 13b| :x:| Tried twite
Phi-2| :x:| Created correct function but incorrect parameter
Phind-CodeLlama34b| :white_check_mark:|
Qwen 14b| :white_check_mark:|
Solar 10.7b Instruct| :x:| Function not correct
Yi-34b Chat| :white_check_mark:|
