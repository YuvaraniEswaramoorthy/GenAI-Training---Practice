from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Set your Google API Key
os.environ["GOOGLE_API_KEY"] = "your-api-key-here"

# Load the PDF
loader = PyPDFLoader("example.pdf")
documents = loader.load()

# Split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Create embeddings
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create vectorstore from documents
vectorstore = FAISS.from_documents(docs, embedding)

# Example: Search for a similar document
query = "What is LangChain?"
docs_with_scores = vectorstore.similarity_search_with_score(query)

for doc, score in docs_with_scores:
    print(f"Score: {score}\nContent: {doc.page_content}\n")
