import streamlit as st
from qdrant_client import QdrantClient
from createEmbeddings import creatEmbedding

# Configuration
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "Data_embeddings"

# Initialize Qdrant client
client = QdrantClient(QDRANT_URL)

def similarity_search(query_vector, top_k=5):

    try:
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k
        )
        # Format the results
        formatted_results = [
            {
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            }
            for result in results
        ]
        return formatted_results
    except Exception as e:
        st.error(f"Error during similarity search: {e}")
        return []

# Streamlit Interface
st.title("Chatbot-like Similarity Search with Qdrant")

# Chat messages history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for instructions
with st.sidebar:
    st.header("Instructions")
    st.write("Enter your text in the chat input below. The app will return the most similar results from the Qdrant database.")

# Main interface
st.write("## Chat")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    elif message["role"] == "bot":
        st.write(f"**Bot:** {message['content']}")

# Input text box
user_input = st.text_input("Enter your text:")

# Handle user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate embedding and search for similar entries
    try:
        query_vector = creatEmbedding(user_input)
        search_results = similarity_search(query_vector, top_k=5)

        if search_results:
            bot_response = "Here are the most similar results:\n"
            for result in search_results:
                payload = result['payload']
                label = payload.get('description', {}).get('Analysis', {}).get('moderation_result', [{}])[0].get('label', 'N/A')
                content = payload.get('description', {}).get('details', {}).get('content', 'N/A')
                score = result['score']

                bot_response += (
                    f"- **Label:** {label}\n"
                    f"  **Content:** {content}\n"
                    f"  **Score:** {score}\n"
                    "---\n"
                )
        else:
            bot_response = "No similar results found."
    except Exception as e:
        bot_response = f"An error occurred: {e}"

    # Add bot response to chat history
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    st.rerun()  # Rerun the app to refresh chat.