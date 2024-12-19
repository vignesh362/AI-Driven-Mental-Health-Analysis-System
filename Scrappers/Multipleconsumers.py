from kafka import KafkaConsumer, TopicPartition
import json
import logging
from datetime import datetime, timezone
import aiohttp
import asyncio

# Logging configuration
logging.basicConfig(
    filename="systemLogs.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

async def process_message(message, consumer_id):
    print(f"Consumer {consumer_id} - Processing message: {message}")

    url = "http://127.0.0.1:8080/moderate"

    async with aiohttp.ClientSession() as session:
        try:
            text_data = message.get("content", "")
            data = {"text": text_data}

            async with session.post(url, json=data) as response:
                if response.status == 200:
                    moderation_result = await response.json()
                    print(f"Consumer {consumer_id} - Moderation result: {moderation_result}")
                else:
                    logging.error(f"Consumer {consumer_id} - Moderation API error {response.status}: {await response.text()}")

        except aiohttp.ClientError as e:
            logging.error(f"Consumer {consumer_id} - AIOHTTP error: {e}")
        except Exception as e:
            logging.error(f"Consumer {consumer_id} - Unexpected error in process_message: {e}")

async def consume_kafka_messages(consumer_id, partition, offset):
    kafka_broker = 'localhost:29092'
    topic = 'scraped-data'

    try:
        consumer = KafkaConsumer(
            bootstrap_servers=kafka_broker,
            group_id=None,  # Manual partition assignment
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v.strip() else None
        )

        # Manually assign partition
        tp = TopicPartition(topic, partition)
        consumer.assign([tp])
        consumer.seek(tp, offset)

        print(f"Consumer {consumer_id} - Listening on topic '{topic}', partition {partition}, offset {offset}...\n")

        for message in consumer:
            try:
                if message.value is None:
                    logging.error(f"Consumer {consumer_id} - Received an empty or invalid message. Skipping...")
                    continue

                await process_message(message.value, consumer_id)
            except json.JSONDecodeError as e:
                logging.error(f"Consumer {consumer_id} - JSON decode error: {e}. Raw message: {message.value}")
            except Exception as e:
                logging.error(f"Consumer {consumer_id} - Unexpected error: {e}. Raw message: {message.value}")

    except Exception as e:
        logging.error(f"Consumer {consumer_id} - Error while setting up Kafka Consumer: {e}")
        print(f"Consumer {consumer_id} - Failed to start consumer. Error: {e}")

if __name__ == "__main__":
    # Offsets for each consumer
    offset_consumer_1 = 0  # Partition 0
    offset_consumer_2 = 0  # Partition 1
    offset_consumer_3 = 0  # Partition 2

    loop = asyncio.get_event_loop()
    tasks = [
        consume_kafka_messages(consumer_id=1, partition=0, offset=offset_consumer_1),  # Consumer 1 for Partition 0
        consume_kafka_messages(consumer_id=2, partition=1, offset=offset_consumer_2),  # Consumer 2 for Partition 1
        consume_kafka_messages(consumer_id=3, partition=2, offset=offset_consumer_3),  # Consumer 3 for Partition 2
    ]
    loop.run_until_complete(asyncio.gather(*tasks))