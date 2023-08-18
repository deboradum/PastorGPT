# PastorGPT
Query the Bible using Faiss. This tool allows you to chat with the Bible using Langchain and the OpenAI api. A chat history memory is kept, so asking follow up questions is supported.
When the answer to the asked question is not to be found in the document, the model responds with "I don't know".

# Usage
To use PastorGPT, first download the requirements by running:
```
python3 -m pip install -r requirements.txt
```
Next, you need an [OpenAI api key](https://platform.openai.com/overview). Add this key to your .env file, and you can start the client using:
```
python3 PastorGPT.py
```
With parameters:
```
-h, --help            show this help message and exit
--local               Run a local embedder and chat model in stead of the OpenAI api.
--save                Save chat history, including the source of the answer, to a local json file.
```

# Local inference
Besides using OpenAI's Davinci-003 model, local inference is also supported. For local inference to work, you'll need [llama.cpp](https://github.com/ggerganov/llama.cpp) installed and you will need valid GGML model weights placed in the `models/` directory. These models can be downloaded [here (7B)](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main), [here (13B)](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/tree/main) or [here (70B)](https://huggingface.co/TheBloke/Llama-2-70B-Chat-GGML/tree/main). You can also [request access](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) and convert the weights to GGML yourself. Keep in mind that the llama chat model weights are needed, not the regular weights.

# Similar projects
I made some other projects based on this project. These other projects do mostly the same thing, but the documents are static and focussed on a specific niche.
- [pdfGPT](https://github.com/deboradum/pdfGPT), chat with any pdf to your choosing.
- [uvaGPT](https://github.com/deboradum/uvaGPT), chat with CS textbooks used at the University of Amsterdam.
- [imamGPT](https://github.com/deboradum/ImamGPT), chat with the Quran.

# Demo
.
