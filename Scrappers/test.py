import logging
from qdrant_client import QdrantClient

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Define constants
QDRANT_URL = "http://localhost:6333"  # Update if Qdrant is running on a different host or port
COLLECTION_NAME = "Data_embeddings"  # Replace with your collection name

# Connect to Qdrant
qdrant_client = QdrantClient(QDRANT_URL)

try:
    # Retrieve all points from the specified collection
    logging.info(f"Retrieving data from collection '{COLLECTION_NAME}'...")
    result = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=None,  # No filter applied, fetch all data
        limit=10  # Adjust the limit as needed
    )

    # Extract points and scroll token
    points, _ = result  # Result contains a list of points and a scroll token

    # Print retrieved data
    if points:
        for point in points:
            print(f"ID: {point.id}")
            print(f"Vector: {point.vector}")
            print(f"Payload: {point.payload}")
            print("-----------------------------")
    else:
        print("No data found in the collection.")

except Exception as e:
    logging.error(f"Error while retrieving data: {e}")