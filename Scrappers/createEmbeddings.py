import requests
import logging
from summarizer import summarize_text
def creatEmbedding(txt):
    # txt=summarize_text(txt)
    try:
        # Set up  embedding requesthttp://127.0.0.1:1234
        url = "http://127.0.0.1:1234/v1/embeddings"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "text-embedding-all-minilm-l6-v2-embedding",  # Ensure the model is correct
            "input": txt
        }
        # Send the request
        response = requests.post(url, headers=headers, json=payload)

        # Check the response status
        if response.status_code == 200:
            embedding = response.json()["data"][0]["embedding"]
            logging.info("Generated embedding successfully.")
            return embedding
        else:
            logging.error(
                "Embedding service returned an error: %s, %s",
                response.status_code,
                response.text
            )
            return None
    except Exception as e:
        logging.error("Error in embedding creation: %s", e)
        return None
print(creatEmbedding("I am so depressed Is I think about nothing but the bad things people say about me."))