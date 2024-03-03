import openai
import pinecone
from pypdf import PdfReader
from langchain_community.llms.openai import OpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
# from langchain.vectorstores import pinecone
from langchain_community.vectorstores import pinecone
from langchain.chains.summarize import load_summarize_chain
# from langchain import HuggingFaceHub
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_community.vectorstores.chroma import Chroma
from dotenv import load_dotenv
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
        #Adding items to our list - Adding data & its metadata
        docs.append(Document(
            page_content=chunks, 
            metadata={"name": filename.name, "id":filename.file_id, "type":filename.type, "size":filename.size, "unique_id":unique_id}
        ))
    return docs

def create_embeddings_load_data():
    embeddings = OpenAIEmbeddings()
    # embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-V2")
    return embeddings

#Function to push data to vetor store -Pinecone
def get_vectorstore(documents, embeddings):

    vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
    return vectorstore

def similar_docs(query, number_response_docs, vectorstore, unique_id):
    similar_docs = vectorstore.similarity_search_with_score(query, int(number_response_docs), {"unique_id":unique_id})
    # print(similar_docs)
    return similar_docs


def get_summary(current_doc):
    from langchain_openai import ChatOpenAI
    # llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    llm = OpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    # chain = load_summarize_chain(llm, chain_type="stuff")
    summary = chain.run(current_doc)
    return summary
