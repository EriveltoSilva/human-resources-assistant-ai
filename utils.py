import openai
import pinecone
from pypdf import PdfReader
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms.openai import OpenAI
from langchain_community.vectorstores import pinecone
from langchain_community.vectorstores.chroma import Chroma
from langchain.chains.summarize import load_summarize_chain
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain import HuggingFaceHub
# from langchain.vectorstores import pinecone
# from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text +=  page.extract_text()
    return text

def create_docs(user_pdf_list, unique_id):
    docs = []
    for filename in user_pdf_list:
        chunks = get_pdf_text(filename)
        docs.append(Document(
            page_content=chunks, 
            metadata={
                "name": filename.name, 
                "id":filename.file_id, 
                "type":filename.type, 
                "size":filename.size, 
                "unique_id":unique_id
            }
        ))
    return docs

def create_embeddings_load_data():
    embeddings = OpenAIEmbeddings()
    # embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-V2")
    return embeddings


def get_vectorstore(documents, embeddings):
    vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
    return vectorstore

def similar_docs(query, number_response_docs, vectorstore, unique_id):
    return vectorstore.similarity_search_with_score(query, int(number_response_docs), {"unique_id":unique_id})


def get_summary(current_doc):
    # llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    llm = OpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(current_doc)
    return summary

def get_summary_str(text):
    # llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    llm = OpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(Document(page_content=text))
    return summary

