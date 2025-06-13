import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Set your API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDlLD62fwrBJXFskPP4pFVqsLy7d7TNCMU"

# Initialize model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

# Streamlit UI
st.set_page_config(page_title="English to French Translator")
st.markdown("<h1>🌐 English to French Translator</h1>", unsafe_allow_html=True)

sentence = st.text_area("Enter an English sentence to translate:", height=150)

if st.button("Translate"):
    if sentence.strip() == "":
        st.error("Please enter a sentence to translate.")
    else:
        # Call the LLM
        user_prompt = f"Translate the following English sentence into French: '{sentence}'"
        response = llm.invoke([HumanMessage(content=user_prompt)])
       
        # Show result
        st.success("✅ Translation successful!")
        st.markdown("### French Translation:")
        st.write(response.content)