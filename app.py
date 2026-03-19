import streamlit as st
import google.generativeai as genai
import time

# Get API Key from Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

st.set_page_config(page_title="PPR 2025 Online Search", page_icon="📑")
st.title("📑 PPR 2025 Search Engine")

uploaded_file = st.file_uploader("Upload PPR 2025 PDF", type=['pdf'])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if 'file_ref' not in st.session_state:
        with st.spinner("Processing PDF..."):
            st.session_state.file_ref = genai.upload_file(path="temp.pdf")
            while st.session_state.file_ref.state.name == "PROCESSING":
                time.sleep(2)
                st.session_state.file_ref = genai.get_file(st.session_state.file_ref.name)
        st.success("Ready to search!")

    query = st.text_input("Ask about any Rule (বিধি):")
    if query:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([st.session_state.file_ref, f"Answer in Bengali from PDF: {query}"])
        st.write(response.text)
