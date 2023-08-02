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


class Pastor:
    def __init__(self, pdf_file="bible.pdf", txt_file="bible.txt", db_name="bible.pkl"):
        load_dotenv()
        self.pdf_file = pdf_file
        self.txt_file = txt_file
        self.db_name = db_name

        if not os.path.isfile(self.txt_file):
            print(f"Creating {self.txt_file}...")
            self.parse_pdf()
        if not os.path.isfile(self.db_name):
            print(f"Splitting {self.txt_file}...")
            chunks = self.split_txt()
            print(f"Creating {self.db_name}...")
            self.create_faiss_db(chunks)
        
        self.load_faiss_db()


    def run(self):
        while True:
            query = input("Ask you question: ")
            if not query:
                continue
            if query == "q":
                return
            res = self.search(query)
            print(res)
            query = ""


    def parse_pdf(self):
        text = textract.process(self.pdfPath)
        with open(self.outputPath, 'w+') as f:
            f.write(text.decode('utf-8'))


    def split_txt(self):
        with open(self.txtPath, "r") as f:
            text = f.read()

        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        text_splitter = CharacterTextSplitter(chunk_size=1250, separator="\n")
        chunks = []
        splits = text_splitter.split_text(text)
        chunks.extend(splits)

        return chunks


    def create_faiss_db(self, chunks):
        store = FAISS.from_texts(chunks, OpenAIEmbeddings())
        faiss.write_index(store.index, "chunks.index")
        store.index = None
        with open(db_name, "wb") as f:
            pickle.dump(store, f)


    def load_faiss_db(self):
        index = faiss.read_index("chunks.index")

        with open(self.db_name, "rb") as f:
            db = pickle.load(f)

        db.index = index
        self.db = db


    def search(self, query):
        chain = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.1), self.db.as_retriever())
        result = chain({"question": query, "chat_history": []})
        return result



p = Pastor()
p.run()
