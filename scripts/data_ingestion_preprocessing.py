from telethon.sync import TelegramClient
import pandas as pd
import re
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Set up Telegram API credentials
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

# Debug: Print the loaded environment variables
print(f"API_ID: {API_ID}")
print(f"API_HASH: {API_HASH}")
print(f"PHONE_NUMBER: {PHONE_NUMBER}")

# List of Telegram channels to scrape
# @ZemenExpress
# @nevacomputer
# @meneshayeofficial
# @ethio_brand_collection
# @Leyueqa
# @sinayelj
CHANNELS = ['@ZemenExpress', '@nevacomputer', '@meneshayeofficial', '@ethio_brand_collection', '@Leyueqa']

# Initialize Telegram Client
client = TelegramClient('session_name', API_ID, API_HASH)

def clean_text(text):
    """Tokenize and normalize Amharic text"""
    text = re.sub(r'[^/u1200-/u137F/s]', '', text)  # Keep only Amharic Unicode range
    text = text.strip()
    return text

def fetch_messages():
    """Fetch messages from specified Telegram channels"""
    all_messages = []
    with client:
        client.connect()
        for channel in CHANNELS:
            try:
                entity = client.get_entity(channel)
                messages = client.get_messages(entity, limit=500)  # Fetch recent 500 messages
                for msg in messages:
                    if msg.text:
                        cleaned_text = clean_text(msg.text)
                        all_messages.append([
                            msg.sender_id, msg.date, cleaned_text
                        ])
            except Exception as e:
                print(f"Error fetching from {channel}: {e}")
    return all_messages

def store_data(messages):
    """Store messages in structured format"""
    df = pd.DataFrame(messages, columns=['Sender', 'Timestamp', 'Message'])
    df['Timestamp'] = df['Timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df.to_csv('C:/Users/ibsan/Desktop/TenX/week-5/data/raw_telegram_messages.csv', index=False)
    print("Data saved successfully!")

if __name__ == "__main__":
    messages = fetch_messages()
    if messages:
        store_data(messages)
    else:
        print("No messages fetched!")
