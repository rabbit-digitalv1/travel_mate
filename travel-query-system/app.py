
import streamlit as st

st.set_page_config(page_title="Travel Query AI Demo", layout="centered")

st.title("🧳 AI-Powered Travel Query Assistant")
st.markdown("Enter your travel-related query below, and we'll fetch relevant recommendations using our AI backend.")

query = st.text_input("🔍 Your Travel Query", placeholder="e.g., Best budget hotels near Thamel with good hygiene")

if query:
    st.write("🚀 Query submitted:", query)
    
    # Simulated response (in real use, call FastAPI backend here)
    st.markdown("### 🧠 AI Response")
    st.success(f'''
    **Top Result:**
    - 🏨 *Hotel Green Tara*
    - 📍 Location: Thamel, Kathmandu
    - 💰 Price: NPR 1800/night
    - 🧼 Hygiene Score: 9.2/10
    - 🔗 [Book on Booking.com](https://booking.com)

    _Recommended based on user reviews from Reddit, travel blogs, and internal route database._
    ''')

    st.markdown("---")
    st.markdown("Powered by Retrieval-Augmented Generation (RAG) + Neo4j + FAISS + LLM")

