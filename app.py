import uuid
import streamlit as st
import utils
from dotenv import load_dotenv

load_dotenv()


#Creating session variables
if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] = ''

def main():
    st.set_page_config(page_title="Resume Screening Assistance")
    st.title("HR - Resume Screeaning Assistance...📝")
    st.subheader("I can help you in resume screening process")

    job_description = st.text_area("Please paste the 'Job Description' here...", key="1")
    document_count = st.text_input("No.of 'Resumes' to return",key="2")
    pdfs = st.file_uploader("Upload, resumes here, only files allowed", type=["pdf"], accept_multiple_files=True)

    submit = st.button("Help me with analysis")
    if submit:
        with st.spinner("Wait for it... "):
            st.write("Our process")
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
                st.write("**File** : "+relevant_docs[item][0].metadata['name'])

                with st.expander("Show me 👁️"):
                    st.info("***Match score**:" + str(relevant_docs[item][1]))
                    # st.write("***"+relevant_docs[item][0].page_content)

                    content = relevant_docs[item][0]
                    # st.write(type(content))
                    print(type(content))
                    summary = utils.get_summary(content)
                    # print(relevant_docs[item][0].page_content)
                    # st.write("**Summary** :"+summary)

        st.success("Hope I was able to save yout time💓")    

if __name__ == '__main__':
    main()