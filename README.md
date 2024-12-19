# AI-Driven Mental Health Analysis System

## Overview

This project aims to classify, analyze, and retrieve semantically similar mental health-related content from large-scale textual data, focusing on identifying sensitive topics such as self-harm, violence, and depression. By leveraging **Kafka**, **Flask**, **KoalaAI**, **PySpark**, **Qdrant**, and a **Streamlit-based UI**, this system processes data in real-time, enabling scalable and efficient Big Data workflows for mental health analysis.

---

## Features

- **Real-Time Data Processing**: Utilizes Kafka for ingesting and streaming Reddit posts in real-time.
- **Text Classification**: Deployed KoalaAI model on a Flask server for classifying text into predefined categories like *Self-Harm* (SH), *Violence* (V), and *Hate Speech* (H).
- **Data Analysis with PySpark**: Processes classified data to generate insights such as label frequency distributions.
- **Semantic Similarity Search**: Qdrant vector database enables storing embeddings and querying for similar content efficiently.
- **Streamlit-Based UI**: A user-friendly interface for querying data and retrieving semantically similar results.

---

## System Architecture

1. **Kafka Pipeline**:
   - Scrapes data from Reddit and streams it to Kafka topics.
   - Processes data in parallel using Kafka consumers.

2. **Flask Server**:
   - Hosts the KoalaAI model, exposed via REST API for real-time classification.

3. **PySpark Analysis**:
   - Processes classified data to generate actionable insights and visualizations.

4. **Qdrant Vector Database**:
   - Stores embeddings of sensitive data for fast and efficient similarity searches.

5. **Streamlit UI**:
   - Allows users to input queries and view results, including semantic matches and label-based insights.

![image](https://github.com/user-attachments/assets/90f97766-fdd3-41d9-a4b5-177202656832)

---

## System Prerequisites

- **Python 3.8+**
- **Docker & Docker Compose** (for running Kafka and Qdrant)
- **Java 8/11** (for PySpark)
- **Kafka CLI Tools** (for managing topics)

## Pipeline Workflow

1. **Data Ingestion**:
   - Scraped data from Reddit is streamed into Kafka.
   - Kafka consumers pick up the data and process it sequentially:
     - **Classification**: Sent to Flask for real-time classification using KoalaAI.
     - **Analysis**: Processed with PySpark to generate label-based insights.
     - **Storage**: Sensitive embeddings are stored in Qdrant for future queries.

2. **Analysis**:
   - Use PySpark scripts to analyze label distributions and generate visualizations.

3. **Similarity Search**:
   - Query Qdrant for semantically similar entries using embeddings.
     
![image](https://github.com/user-attachments/assets/b948c2f2-edd1-4008-bdfc-64628bad0dbb)

---

## Streamlit UI

- Access the UI at `http://localhost:8501` (default Streamlit port).
- Input a query to retrieve the most semantically similar content from Qdrant.
- View results with similarity scores, labels, and original text.

  
## Technologies Used

- **Apache Kafka**: Real-time data streaming and ingestion.
- **Flask**: Hosting the KoalaAI model for classification.
- **PySpark**: Large-scale data analysis and label visualization.
- **Qdrant**: Storing and querying semantic embeddings.
- **Streamlit**: User-friendly interface for querying and similarity search.
- **KoalaAI**: Pre-trained NLP model for text classification.
