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

# Demo
.
