import streamlit as st
import random # Used for simulating hashtag generation

# --- Page Configuration ---
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Custom CSS for enhanced aesthetics ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #0077B5; /* LinkedIn Blue */
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: background-color 0.3s ease;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #005f90;
    }
    .stTextArea, .stSelectbox {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 5px;
    }
    .header-style {
        font-family: 'Inter', sans-serif;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
    }
    .subheader-style {
        font-family: 'Inter', sans-serif;
        color: #34495e;
        margin-top: 20px;
        border-bottom: 2px solid #ccc;
        padding-bottom: 5px;
    }
    .linkedin-post-output {
        background-color: #e6f7ff; /* Light LinkedIn blue */
        border-left: 5px solid #0077B5;
        padding: 20px;
        margin-top: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        white-space: pre-wrap; /* Preserves whitespace and line breaks */
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        font-size: 1.05em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Main Application Title ---
st.markdown('<h1 class="header-style">✍️ LinkedIn Post Creator</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #555;">Transform your bullet-point ideas into engaging LinkedIn posts!</p>', unsafe_allow_html=True)

# --- Function to simulate LLM generation ---
def generate_linkedin_post(idea_points, tone):
    """
    Simulates the generation of a LinkedIn post based on bullet points and tone.
    In a real application, this would call an LLM API (e.g., Gemini API).
    """
    if not idea_points.strip():
        return "", [] # Return empty post and hashtags if no idea provided

    # Simple keyword extraction for simulated hashtags
    keywords = set()
    for point in idea_points.split('\n'):
        words = point.lower().replace('.', '').replace(',', '').split()
        for word in words:
            if len(word) > 3 and word.isalpha():
                keywords.add(word)

    # Simulated common LinkedIn hashtags
    common_hashtags = ["innovation", "career", "leadership", "business", "technology",
                       "work", "inspiration", "growth", "future", "learning", "motivation"]
    
    # Select a few relevant and common hashtags
    suggested_hashtags = [f"#{tag}" for tag in list(keywords)[:3]] + [f"#{tag}" for tag in random.sample(common_hashtags, min(3, len(common_hashtags)))]
    suggested_hashtags = list(set(suggested_hashtags)) # Remove duplicates

    # Simulate post generation based on tone
    if tone == "Professional":
        post_start = "Excited to share some thoughts on "
        post_middle = f"Here are a few key takeaways:\n{idea_points}\n\n"
        post_end = "I believe these points are crucial for fostering growth and success in today's dynamic environment. What are your perspectives on this?"
        
        # Example of how to integrate a real LLM for generation
        # try:
        #     prompt = f"Given the following bullet points:\n{idea_points}\n\nDraft a professional LinkedIn post. Include a strong opening, elaborate on the points, and end with a call to action or a question for engagement. Add relevant hashtags."
        #     # Example fetch call for Gemini API (replace with your actual implementation)
        #     # chatHistory = []
        #     # chatHistory.push({ role: "user", parts: [{ text: prompt }] });
        #     # const payload = { contents: chatHistory };
        #     # const apiKey = ""
        #     # const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
        #     # response = await fetch(apiUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        #     # result = response.json();
        #     # generated_text = result.candidates[0].content.parts[0].text;
        #     # return generated_text, suggested_hashtags
        # except Exception as e:
        #     st.error(f"Error calling LLM: {e}. Using simulated response.")
        
        generated_post_content = f"{post_start}{idea_points.splitlines()[0].strip().replace('-', '').replace('*', '') if idea_points else 'a new idea'}...\n\n{post_middle}{post_end}"

    else: # Casual
        post_start = "Just had a cool idea about "
        post_middle = f"Thinking about these points:\n{idea_points}\n\n"
        post_end = "What do you think? Let me know your thoughts!"
        
        # Example of how to integrate a real LLM for generation
        # try:
        #     prompt = f"Given the following bullet points:\n{idea_points}\n\nDraft a casual and engaging LinkedIn post. Include emojis and a conversational tone. Add relevant hashtags."
        #     # Example fetch call for Gemini API (replace with your actual implementation)
        #     # ... (similar to professional tone, but with different prompt)
        # except Exception as e:
        #     st.error(f"Error calling LLM: {e}. Using simulated response.")
        
        generated_post_content = f"👋 {post_start}{idea_points.splitlines()[0].strip().replace('-', '').replace('*', '') if idea_points else 'something exciting'}!\n\n{post_middle}{post_end} 👇"

    return generated_post_content, suggested_hashtags

# --- Input Area ---
st.markdown('<h2 class="subheader-style">💡 Your Idea (Bullet Points)</h2>', unsafe_allow_html=True)
idea_input = st.text_area(
    "Enter your idea in bullet points (e.g., - Key point 1\n- Key point 2)",
    height=150,
    placeholder="Example:\n- New AI feature for personalization\n- Improves user engagement by 20%\n- Beta testing starts next month"
)

# --- Tone Selection ---
st.markdown('<h2 class="subheader-style">🗣️ Select Tone</h2>', unsafe_allow_html=True)
tone_selected = st.selectbox(
    "Choose the tone for your LinkedIn post:",
    ("Professional", "Casual")
)

# --- Generate Button ---
if st.button("Generate LinkedIn Post"):
    if idea_input:
        with st.spinner('Crafting your LinkedIn post...'):
            generated_post, hashtags = generate_linkedin_post(idea_input, tone_selected)
            
            st.markdown('<h2 class="subheader-style">✨ Your Polished LinkedIn Post</h2>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="linkedin-post-output">
                {generated_post}
                <br><br>
                {" ".join(hashtags)}
                </div>
            """, unsafe_allow_html=True)

            st.info("""
            **Note:** This version simulates the output of an AI. For a real application, 
            you would integrate a Language Model API (e.g., Gemini API) here to generate 
            dynamic and contextually rich posts.
            """)
    else:
        st.warning("Please enter your idea in bullet points before generating the post.")

st.markdown("---")
st.caption("Powered by Gemini (simulated AI generation)")
