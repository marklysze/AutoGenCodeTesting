Testing Code Generation using alt-models (Local LLMs)

See the results folder for outputs and summaries.

Testing so far...

## Code Executors

### Juypter Notebook (local)
[Basis for testing code here](https://github.com/microsoft/autogen/blob/tutorial/website/docs/getting-started/code-executors.ipynb)

#### Fibonacci
[More detail here](results/2024-02-08%20Jupyter%20Fibonacci%20Summary.txt) and see [results](results) folder for code outputs.
**Model** | **Success** | **Notes**
---|---|---|
DeepSeek Coder 6.7b| :white_check_mark:|
Llama2 7b Chat| :x:| Added dependency that didn't work
Llama2 13b Chat| :white_check_mark:|
Mistral 7b 0.2 Instruct| :white_check_mark:|
Mixtral 8x7b Q4| :white_check_mark:|
Mixtral 8x7b Q5| :white_check_mark:| Tidier than Q4
Neural Chat 7b Chat| :white_check_mark:| Fast
Nexus Raven| :x:| Tried twice
Orca2 13b| :x:| Tried twice
Phi-2| :x:| Correct function, incorrect parameter
Phind-CodeLlama34b| :white_check_mark:|
Qwen 14b| :white_check_mark:|
Solar 10.7b Instruct| :x:| Function not correct
Yi-34b Chat| :white_check_mark:|
