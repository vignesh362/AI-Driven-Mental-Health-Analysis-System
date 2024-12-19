import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Chatbot-like Similarity Search with Qdrant")

with st.sidebar:
    st.header("Instructions")
    st.write("Enter your text and click 'Send'. The app will return similar results from the database.")

st.write("## Chat")

# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Bot:** {message['content']}")

# Create a form for input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Enter your text:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Process input: generate embedding, search Qdrant, produce bot response
    # ...
    # Append bot message:
    # st.session_state.messages.append({"role": "bot", "content": bot_response})
    # Refresh the page to show the new messages
    st.experimental_rerun()