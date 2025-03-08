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
# @Shewabrand
# @helloomarketethiopia
# @modernshoppingcenter
# @qnashcom
# @Fashiontera
# @kuruwear
CHANNELS = ['@ZemenExpress', '@nevacomputer', '@Shewabrand',
            '@meneshayeofficial', '@ethio_brand_collection', 
            '@helloomarketethiopia', '@modernshoppingcenter',
            '@qnashcom', '@Fashiontera', '@kuruwear']
# print(len(CHANNELS))

# Initialize Telegram Client
client = TelegramClient('session_name', API_ID, API_HASH)

def clean_text(text):
    """Tokenize and normalize Amharic text"""
    text = re.sub(r'[^\u1200-\u137F\s]', '', text)  # Keep only Amharic Unicode range
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
                messages = client.get_messages(entity, limit=3000)  # Fetch recent 500 messages
                for msg in messages:
                    if msg.text:
                        cleaned_text = clean_text(msg.text)
                        all_messages.append([
                            msg.id, msg.sender_id, msg.date, cleaned_text, 'text', entity.title, entity.username
                        ])
                    elif msg.media:
                        if msg.photo:
                            all_messages.append([
                                msg.id, msg.sender_id, msg.date, msg.photo, 'photo', entity.title, entity.username
                            ])
                        elif msg.document:
                            all_messages.append([
                                msg.id, msg.sender_id, msg.date, msg.document, 'document', entity.title, entity.username
                            ])
            except Exception as e:
                print(f"Error fetching from {channel}: {e}")
    return all_messages

def store_data(messages):
    """Store messages in structured format"""
    df = pd.DataFrame(messages, columns=['ID', 'Sender', 'Timestamp', 'Message', 'Type', 'Channel Title', 'Channel Username'])
    df['Timestamp'] = df['Timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_telegram_messages.csv'), index=False)
    print("Data saved successfully!")

if __name__ == "__main__":
    messages = fetch_messages()
    if messages:
        store_data(messages)
    else:
        print("No messages fetched!")
