from kafka import KafkaConsumer
import json
import logging
from pymongo import MongoClient
from datetime import datetime, timezone
import requests

logging.basicConfig(
    filename="systemLogs.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.ERROR
)



def process_message(message):
    print("--------------------------------------------------------------------------------------")
    print(message)
    url = "http://127.0.0.1:8080/moderate"

    txt="I tried every single thing for so many years. I became a runner. Got tons of sun. Had cold showers almost every day. Found purpose. Found meaning. Changed my thinking. Even CBT worksheets. Believed in the future. Find hope. All of it. At some point I finally realized none of it did shit. The moment it got quiet, how I truly felt would show up; deep sadness for no reason. It was all self-gaslighting and repressing. It took so many years but I finally realize I'm not creating the depression, it's not my fault, and it's so relieving to realize I'm not the one doing it. I realized even the negative thoughts is a symptom of depression and you can't think different your way out of depression. I'm now working on trauma healing. That's another possibility I will exhaust and I had some of the least depressed days of my life. Its like I could taste the weather. My self-blame or internal shame for no reason is gone. If a hurtful thing happens I'll quickly be back to being emotionally regulated again. Sad for no reason and emptiness? it is also lower. I work on creating feelings of safety and body scan/awareness. It creates weird shaking releases in my body and I believe it's either fight or flight energy releases or trauma release. Anyone has experience with this?"
    data = {"text": message.content}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")
    # # Connect to the local MongoDB instance
    # client = MongoClient('mongodb://localhost:27017/')
    # db = client['Scrapped']
    # collection = db['BigData']
    #
    # # Create a document with the current date and time in UTC
    # document = {
    #     "data": message,
    #     "ScrappedTime": datetime.now(timezone.utc)
    # }
    #
    # # Insert the document into the collection
    # result = collection.insert_one(document)
    #
    # print(f"Document inserted with ID: {result.inserted_id}")

# Kafka consumer setup
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

            process_message(message.value)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}. Raw message: {message.value}")
            continue
        except Exception as e:
            logging.error(f"Unexpected error: {e}. Raw message: {message.value}")
            continue

except Exception as e:
    logging.error(f"Error while setting up Kafka Consumer: {e}")
    print(f"Failed to start consumer. Error: {e}")