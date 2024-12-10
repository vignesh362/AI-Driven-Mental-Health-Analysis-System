from kafka import KafkaConsumer
import json
import logging
from pymongo import MongoClient
from datetime import datetime, timezone
import aiohttp
import asyncio
from qdrantStorage import QdrantEmbeddingStorage
# Logging configuration
logging.basicConfig(
    filename="systemLogs.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG  # Set to DEBUG for better visibility during development
)

async def process_message(message):
    """
    Asynchronously process a Kafka message, send it for text moderation, and optionally save to MongoDB.
    """
    print("--------------------------------------------------------------------------------------")
    print(f"Processing message: {message}")

    # API URL
    url = "http://127.0.0.1:8080/moderate"

    async with aiohttp.ClientSession() as session:
        try:
            # Prepare data for API
            text_data = message.get("content", "")
            data = {"text":text_data}

            # Send to moderation API
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    moderation_result = await response.json()
                    # print("Moderation result:", moderation_result)
                    print("Moderation label:", moderation_result)
                    if moderation_result['moderation_result'][0]['label']!="OK":
                        print("+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+")
                        storage = QdrantEmbeddingStorage()
                        metadata = {
                            "source": "reddit",
                            "description": {
                                "Analysis": moderation_result,
                                "details": message
                            }
                        }

                        success = storage.store_embedding(text_data, metadata)
                        if success:
                            logging.info("Embedding successfully stored.")
                        else:
                            logging.error("Failed to store embedding.")

                else:
                    logging.error(f"Moderation API error {response.status}: {await response.text()}")
                    print(f"Moderation API error {response.status}: {await response.text()}")

            # Example MongoDB integration (commented out):
            # Connect to MongoDB
            # client = MongoClient('mongodb://localhost:27017/')
            # db = client['Scrapped']
            # collection = db['BigData']

            # Document to save
            # document = {
            #     "data": message,
            #     "ScrappedTime": datetime.now(timezone.utc)
            # }
            # Insert the document
            # result = collection.insert_one(document)
            # print(f"Document inserted with ID: {result.inserted_id}")

        except aiohttp.ClientError as e:
            logging.error(f"AIOHTTP error: {e}")
            print(f"AIOHTTP error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in process_message: {e}")
            print(f"Unexpected error in process_message: {e}")

async def consume_kafka_messages():

    kafka_broker = 'localhost:29092'
    topic = 'scraped-data'

    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=kafka_broker,
            group_id="scraped-content-consumer-group",
            auto_offset_reset='earliest',
            value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v.strip() else None
        )

        print(f"Listening for messages on topic '{topic}'...\n")

        for message in consumer:
            try:
                if message.value is None:
                    logging.error("Received an empty or invalid message. Skipping...")
                    continue

                # Process each message asynchronously
                await process_message(message.value)
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {e}. Raw message: {message.value}")
                continue
            except Exception as e:
                logging.error(f"Unexpected error: {e}. Raw message: {message.value}")
                continue

    except Exception as e:
        logging.error(f"Error while setting up Kafka Consumer: {e}")
        print(f"Failed to start consumer. Error: {e}")

if __name__ == "__main__":
    asyncio.run(consume_kafka_messages())