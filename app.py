import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv



st.set_page_config(page_title="Chatbot", layout="wide")
image_url = "https://static.vecteezy.com/system/resources/thumbnails/021/615/530/small_2x/bot-3d-render-icon-illustration-png.png"
st.image(image_url, width=50)
st.title("ChatBot 💬  |  ⚡Powered by Gemini AI ⚡")  
# Load environment variables
load_dotenv()

with st.sidebar.expander("🔒 Google", expanded=False):
    st.markdown('[Click here](https://console.cloud.google.com/apis/credentials) to get your Google API key')
    google_api_key = st.text_input("🔑Enter your API Key", type="password")

# Configure API Key
if google_api_key:
    genai.configure(api_key=google_api_key)
else:
    #st.sidebar.warning("⚠️ Add a valid API Key in the sidebar to proceed.")
    st.markdown(
    """
    <div style="
        padding: 10px;
        border-radius: 8px;
        background-color: #FFDDC1; /* Light Orange */
        color: #9C2A00; /* Dark Red */
        font-weight: bold;
        text-align: center;
        font-size: 16px;">
        ⚠️ Add a valid API Key in the sidebar to proceed.
    </div>
    """,
    unsafe_allow_html=True
)
    st.stop()  # Prevent further execution if API key is missing

# Function to display chat messages
def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f" {message['content']}")
            else:
                st.markdown(f" {message['content']}")

# Function to get response from Gemini model
def get_gemini_response(messages, language):
    model = genai.GenerativeModel("gemini-pro")
    prompt = messages[-1]["content"]
    if language == "Urdu":
        prompt = f"براہ کرم اردو میں جواب دیں: {prompt} 🌟"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Main function
def main():
   

    # Sidebar for language selection
    st.sidebar.title("🛠️ Settings")
    language = st.sidebar.selectbox("Select Language", ["English", "Urdu"], index=0)

    

# Display the rest of the title
    #st.title("ChatBot 💬  |  ⚡Powered by Gemini AI ⚡")
    # Initialize session state for messages if not already initialized
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat history
    display_messages()

    # Input from user
    if prompt := st.chat_input("Ask something... ✍️"):
        # Store user input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f" {prompt}")

        # Generate and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_gemini_response(st.session_state.messages, language)
            message_placeholder.markdown(f" {full_response}")

        # Store assistant response
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Execute the app
if __name__ == "__main__":
    main()
