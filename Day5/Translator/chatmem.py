import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile

# --- API Key Setup ---
os.environ["GOOGLE_API_KEY"] = "AIzaSyDlLD62fwrBJXFskPP4pFVqsLy7d7TNCMU"  # ← Replace with your actual Gemini API key

# --- Streamlit UI ---
st.set_page_config(page_title="RAG + Memory with Gemini", layout="centered")
st.title("RAG with Memory using Google Gemini")

# --- Session State for Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- File Upload ---
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

# --- Question Form ---
with st.form("question_form"):
    user_question = st.text_input("Ask a question based on the uploaded PDFs:")
    submitted = st.form_submit_button("Submit")

# --- Core Logic ---
if submitted and uploaded_files and user_question.strip():
    try:
        with st.spinner("Processing files and querying Gemini..."):

            # --- Load & Split Documents ---
            all_docs = []
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    loader = PyPDFLoader(tmp.name)
                    docs = loader.load()
                    all_docs.extend(docs)

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_docs = splitter.split_documents(all_docs)

            # --- Embedding & Vector Store (FAISS) ---
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            vectorstore = FAISS.from_documents(split_docs, embedding=embeddings)

            # --- Memory Setup ---
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            # --- Chat Model ---
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

            # --- Retrieval QA Chain ---
            rag_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(),
                memory=memory
            )

            # --- Run the Chain ---
            response = rag_chain.run(user_question)

            # --- Store & Display Chat History ---
            st.session_state.chat_history.append(("User", user_question))
            st.session_state.chat_history.append(("Gemini", response))

            st.success("✅ Answer:")
            st.write(response)

            with st.expander("🧠 Chat History"):
                for role, msg in st.session_state.chat_history:
                    st.write(f"**{role}:** {msg}")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")

elif submitted and not uploaded_files:
    st.warning("Please upload at least one PDF file.")
elif submitted and not user_question.strip():
    st.warning("Please enter a valid question.")
