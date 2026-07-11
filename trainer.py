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

client = Groq(api_key=st.secrets["API_KEY"])

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
                            "content":You are an expert fitness trainer and nutritionist.

When users ask for workout plans:
- Ask age, gender, height, weight.
- Ask fitness goals.
- Ask available equipment.
- Ask workout days per week.
- Ask experience level.

Provide:
- Weekly workout schedule
- Exercises
- Sets and reps
- Rest periods
- Progression tips

When users ask for diet:
- Estimate calories
- Suggest protein intake
- Give meal plans
- Mention hydration advice

Keep answers practical and beginner friendly.
                        },
                        {"role": "user", "content": prompt}
                    ]
                )

                reply = response.choices[0].message.content

            except Exception as e:
                reply =  """
⚠️ Unable to connect to the AI service.
Please try again in a few moments.
"""
        st.markdown(reply)

    # Save reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
