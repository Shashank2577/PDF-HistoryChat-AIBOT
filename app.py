import streamlit as st
import pickle
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import RetrievalQA


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_vectors():
            store_name = 'online_help'
            st.write("from pickle")
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
            st.write("Loaded from pickle")
            return VectorStore

template = """You are an Umantis AI assistant which helps with the customer support, your response should start with greeting the user apraising of there question and the providing the answer, it truthfully says it does not know.
Human: {question}
AI Assistant:"""
prompt = PromptTemplate(input_variables=["question"], template=template)



condense_prompt = PromptTemplate.from_template(
    ('You are an AI assistant for Umantis Customer Care, and you should greet the user and answer the this question ({question}), and you can scan this chat history  ({chat_history}).')
)

combine_docs_custom_prompt = PromptTemplate.from_template(
    ('Write a haiku about a dolphin.\n\n'
     'Completely ignore any context, such as {context}, or the question ({question}).')
)

def get_conversation_chain(vectorstore, user_question):
    
    llm = ChatOpenAI()
    # PROMPT=template.format(input=user_question)
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = "" + st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                # raw_text = get_pdf_text(pdf_docs)

                # # get the text chunks
                # text_chunks = get_text_chunks(raw_text)

                # create vector store
                # vectorstore = get_vectorstore(text_chunks)
                vectorstore = get_vectors()

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore,user_question)


if __name__ == '__main__':
    main()
