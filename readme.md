**Project README**
Amharic NER for Ethiopian Telegram E-commerce
This project involves developing a Named Entity Recognition (NER) system for Amharic text from Ethiopian-based Telegram e-commerce channels. The objective is to identify entities like products, prices, and locations within messages shared in these channels.

**Objectives**
Data Collection and Preprocessing: Set up a data ingestion system to fetch real-time messages (text, images, documents) from at least 5 Ethiopian Telegram e-commerce channels. Preprocess and clean the data for entity extraction.
Data Labeling: Label a subset of the dataset in CoNLL format, identifying entities such as products, prices, and locations.
Model Training and Comparison: Fine-tune and compare multiple NER models on the preprocessed and labeled dataset.

**Data Collection (Task-1)**
Use a custom scraper to identify and connect to at least 5 relevant Telegram channels for Ethiopian e-commerce.
Collect messages containing both text and images.
Preprocess text data, handle Amharic-specific linguistic features (e.g., normalization, tokenization), and clean it for entity extraction.
Store the cleaned data in a structured format for further analysis.

**Data Labeling (Task-2)**
Label the Amharic text data for entities such as products, prices, and locations.
Label a subset of the dataset in CoNLL format, which includes the following: