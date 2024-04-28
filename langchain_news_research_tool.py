import os
from keys import my_key
import streamlit as st
import pickle
import time
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

os.environ['GOOGLE_API_KEY'] = my_key

st.title("News Research Tool ")
st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f'URL {i+1}')
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

main_placeholder = st.empty()

os.environ['GOOGLE_API_KEY'] = 'AIzaSyCvMuOyehJDnmWxZNF917EfEvV330EO4gA'

llm = GoogleGenerativeAI(model="gemini-pro",
                        max_output_tokens=1024,
                        google_api_key=os.environ['GOOGLE_API_KEY'],
                        temperature= 0.6)

if process_url_clicked:
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading...Started...✅✅✅")
    data = loader.load()
    if data:
    # split data
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
        )
        main_placeholder.text("Text Splitter...Started...✅✅✅")
        docs = text_splitter.split_documents(data)

        if docs:
            # create embeddings and save it to FAISS index
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            vectorstore_openai = FAISS.from_documents(docs, embeddings)
            main_placeholder.text("Embedding Vector Started Building...✅✅✅")
            time.sleep(2)

            # Save the FAISS index to a pickle file
            #vectorstore_openai.save_local(file_path)
            with open(file_path, 'wb') as f:
                pickle.dump(vectorstore_openai, f)
        else:
            main_placeholder.text("Text Splitter produced empty documents. Check data.")
    else:
        main_placeholder.text("Data loading failed. Check URLs or network connection.")


query = main_placeholder.text_input("Questions: ")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain.invoke({"question": query}, return_only_outputs=True)
            st.header("Answer")
            st.subheader(result["answer"])




    
    
