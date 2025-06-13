import streamlit as st
from langchain.agents import Tool, initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDlLD62fwrBJXFskPP4pFVqsLy7d7TNCMU"

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# Define the DuckDuckGo search tool
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=search.run,
        description="Useful for answering questions about current events or general world knowledge",
    )
]

# Memory to keep chat context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description",
    verbose=False,
    memory=memory,
)

# Streamlit UI
st.title("🔍 Gemini + DuckDuckGo Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("Ask me anything", key="input")

# Handle chat logic
if user_input:
    with st.spinner("Searching and thinking..."):
        response = agent.run(user_input)

    # Save to session history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)
