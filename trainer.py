import streamlit as st
from groq import Groq

# ---------------- SETTINGS ----------------
st.set_page_config(
    page_title="AI Gym Trainer",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔴 TEMP API KEY (replace this)
API_KEY = "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"

client = Groq(api_key=API_KEY)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "🏋️ Hello! I’m your AI Gym Trainer 💪\nAsk me about workouts or diet!"
        }
    ]

# ---------------- UI HEADER ----------------
st.markdown("<h2 style='text-align: center;'>💪 AI Gym Trainer</h2>", unsafe_allow_html=True)

# ---------------- CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
if prompt := st.chat_input("Ask about workout or diet..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate reply
    with st.chat_message("assistant"):
        with st.spinner("💭 Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional gym trainer. Only answer about workouts and diet. If unrelated, say you only help with fitness."
                        },
                        {"role": "user", "content": prompt}
                    ]
                )

                reply = response.choices[0].message.content

            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"

        st.markdown(reply)

    # Save reply
    st.session_state.messages.append({"role": "assistant", "content": reply})