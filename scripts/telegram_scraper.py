from telethon import TelegramClient
import csv
import os
import asyncio
from functools import wraps
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Load environment variables
# load_dotenv('.env')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

print(f"API_ID: {API_ID}")
print(f"API_HASH: {API_HASH}")
print(f"PHONE_NUMBER: {PHONE_NUMBER}")

# Metaprogramming: Channel registration through decorators
channels_to_scrape = []

def channel(name):
    """Decorator to register channels for scraping"""
    def decorator(func):
        channels_to_scrape.append(name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Register channels using decorators
@channel('@ZemenExpress')
@channel('@nevacomputer')
@channel('@Shewabrand')
@channel('@meneshayeofficial')
@channel('@ethio_brand_collection')
@channel('@helloomarketethiopia')
@channel('@modernshoppingcenter')
@channel('@qnashcom')
@channel('@Fashiontera')
@channel('@kuruwear')
def register_channels():
    """Dummy function for channel registration"""

# Functional Programming: Error handler decorator
def handle_errors(func):
    """Decorator to handle exceptions in async functions"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {str(e)}")
    return wrapper

# Context Manager for CSV writing
class CSVWriter:
    """Context manager for handling CSV file operations"""
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.writer = None

    def __enter__(self):
        self.file = open(self.filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date'])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

# Coroutine for writing to CSV
async def write_csv(queue):
    """Coroutine to write data from queue to CSV"""
    with CSVWriter('C:/Users/ibsan/Desktop/TenX/week-5/data/telegram_data.csv') as csv_writer:
        while True:
            item = await queue.get()
            if item is None:  # Termination signal
                break
            csv_writer.writer.writerow(item)
            queue.task_done()

# Generator function for message batches
async def message_batcher(messages, batch_size=100):
    """Generator to yield message batches"""
    batch = []
    async for message in messages:
        batch.append(message)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

# Enhanced scraping function with error handling
@handle_errors
async def scrape_channel(client, channel_username, queue):
    """Scrape messages from a channel and put them in the queue"""
    entity = await client.get_entity(channel_username)
    channel_title = entity.title
    
    # Using generator for batch processing
    async for batch in message_batcher(client.iter_messages(entity, limit=10_000)):
        for message in batch:
            await queue.put([
                channel_title,
                channel_username,
                message.id,
                message.message,
                message.date
            ])
            print(f"Scraped message ID {message.id} from {channel_title}")

# Client initialization with performance optimizations
client = TelegramClient('scraping_session', API_ID, API_HASH).start()

async def main():
    # Create processing queue
    queue = asyncio.Queue()
    
    # Start writer task
    writer_task = asyncio.create_task(write_csv(queue))
    
    # Create scraping tasks using list comprehension
    scrape_tasks = [
        asyncio.create_task(scrape_channel(client, channel, queue))
        for channel in channels_to_scrape
    ]
    
    # Run all tasks concurrently
    await asyncio.gather(*scrape_tasks)
    
    # Signal writer to finish
    await queue.put(None)
    await writer_task

# Run the program
if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())

