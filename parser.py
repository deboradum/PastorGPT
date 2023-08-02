from dotenv import load_dotenv
import faiss
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
import os
import pickle
import textract
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

def parse_pdf(pdfPath, outputPath):
    text = textract.process(pdfPath)

    with open(outputPath, 'w+') as f:
        f.write(text.decode('utf-8'))


def split_txt(txtPath):
    with open(txtPath, "r") as f:
        text = f.read()

    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    text_splitter = CharacterTextSplitter(chunk_size=1250, separator="\n")
    chunks = []
    splits = text_splitter.split_text(text)
    chunks.extend(splits)

    # for d in chunks:
    #     print(d)
    #     print("--\n\n--")

    return chunks


def create_faiss_db(db_name, chunks):
    store = FAISS.from_texts(chunks, OpenAIEmbeddings())
    faiss.write_index(store.index, "chunks.index")
    store.index = None
    with open(db_name, "wb") as f:
        pickle.dump(store, f)


def load_faiss_db(db_name):
    index = faiss.read_index("chunks.index")

    with open(db_name, "rb") as f:
        store = pickle.load(f)

    store.index = index

    return store


def search(store, query):
    chain = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.1), store.as_retriever())
    result = chain({"question": query, "chat_history": []})
    return result


pdf_file = "bible.pdf"
txt_file = "bible.txt"
db_name = "bible.pkl"

if not os.path.isfile(txt_file):
    print(f"Creating {txt_file}...")
    parse_pdf(pdf_file, txt_file)

if not os.path.isfile(db_name):
    print(f"Splitting {txt_file}...")
    chunks = split_txt(txt_file)
    print(f"Creating {db_name}...")
    create_faiss_db(db_name, chunks)
print(f"Loading {db_name}...")
store = load_faiss_db(db_name)

while True:
    query = input("Ask you question: ")
    if not query:
        continue
    res = search(store, query)
    print(res)
    query = ""
