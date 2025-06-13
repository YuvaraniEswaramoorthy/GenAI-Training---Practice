import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
google_api_key = os.getenv("AIzaSyDlLD62fwrBJXFskPP4pFVqsLy7d7TNCMU")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=google_api_key
)

# Create a prompt template
prompt = ChatPromptTemplate.from_template(
    "Translate the following English sentence to French:\n\n{sentence}"
)

# Create the chain using LangChain's | operator
chain: Runnable = prompt | llm | StrOutputParser()

# Get input from user
english_sentence = input("Enter an English sentence: ")

# Run the chain
result = chain.invoke({"sentence": english_sentence})

# Output the result
print("French Translation:", result)
