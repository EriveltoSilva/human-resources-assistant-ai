import uuid
import streamlit as st
import utils
from dotenv import load_dotenv
from langchain.schema import Document

load_dotenv()


#Creating session variables
if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] = ''

def main():
    st.set_page_config(page_title="Assistente de RH")
    st.title("RH - Assistente de Triagem de Candidatos...📝")
    st.subheader("Posso ajudá-lo no processo de triagem de currículos")

    job_description = st.text_area("Por favor, cole a 'Descrição do trabalho' aqui...", key="1")
    document_count = st.text_input("Nº de 'Currículos' a serem retornados",key="2")
    pdfs = st.file_uploader('Upload, currículos aqui, somente arquivos "pdf" permitidos', type=["pdf"], accept_multiple_files=True)

    submit = st.button("Analisar Curriculos 📄")
    if submit:
        with st.spinner("Analisando... "):
            st.write("Nosso processo")
            #Creating a unique ID, so that we can use to query and get only the user uploade
            st.session_state['unique_id'] = uuid.uuid4().hex

            #Create a documents list out od all the user uploaded pdf files
            docs = utils.create_docs(pdfs, st.session_state['unique_id'])
            # st.write(docs)

            #Displaying the count of resumes that have been upload
            st.write(f"Documentos a processar:{len(docs)}")

            #Create embeddings instance
            embeddings = utils.create_embeddings_load_data()

            #Create vectorstore
            vectorstore = utils.get_vectorstore(docs, embeddings)
            
            # Fetch relevant documents from vectorstore
            relevant_docs = utils.similar_docs(job_description, document_count, vectorstore, st.session_state['unique_id'])
            # st.write("Resposta:")
            # st.write(relevant_docs)

            #Introducing a line separator
            st.write(":heavy_minus_sign:"*30)

            #For each relavant doc - display some info 
            for item in range(len(relevant_docs)):
                st.subheader("👉 "+ str(item+1))
                st.write("**Ficheiro** : "+relevant_docs[item][0].metadata['name'])

                with st.expander("Mostrar Detalhes 👁️"):
                    st.info(f"***Taxa de compatibilidade**:{float(relevant_docs[item][1])*100}%")
                    summary = utils.get_summary([relevant_docs[item][0]])
                    st.write("**Pequeno Resumo do candidato** :"+summary)

        st.success("Espero ter conseguido ajudar a economizar o seu tempo💓")    

if __name__ == '__main__':
    main()