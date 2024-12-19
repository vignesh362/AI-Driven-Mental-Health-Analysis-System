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
        print(f"Error during similarity search: {e}")
        return []

# if __name__ == "__main__":
#     txt=creatEmbedding("subreddit to post this, so i had an attempt a few weeks ago (nothing serious, just took a few pills went to a hospital, and vomited for some time but i was fine), and my mom keeps saying that it's really hard for her. ")
#     top_k = 5  # Number of results to fetch
#
#     search_results = similarity_search(txt, top_k=top_k)
#
#     if search_results:
#         print("Similarity Search Results:")
#         for result in search_results:
#             print(f"ID: {result['id']}")
#             print(f"Score: {result['score']}")
#             print(f"Payload: {result['payload']}")
#             print("-" * 50)
#     else:
#         print("No results found.")
