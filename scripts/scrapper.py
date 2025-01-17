from telethon import TelegramClient, events
import os
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('phone')

# Directory for media files
media_dir = 'photos_'
os.makedirs(media_dir, exist_ok=True)

# Initialize Telegram client
client = TelegramClient('scraping_session', api_id, api_hash)

# Function to save messages to CSV
def save_message_to_csv(writer, channel_title, channel_username, message, media_path=None):
    writer.writerow([
        channel_title,
        channel_username,
        message.id,
        message.message,
        message.date,
        media_path
    ])

# Function to scrape past data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    async for message in client.iter_messages(entity, limit=10000):
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            # Create a unique filename for the photo
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            # Download the media to the specified directory if it's a photo
            await client.download_media(message.media, media_path)
        
        # Save message to CSV
        save_message_to_csv(writer, channel_title, channel_username, message, media_path)

# Function to handle real-time message ingestion
@client.on(events.NewMessage(chats=['@meneshayeofficial']))
async def handle_new_message(event):
    channel = await event.get_chat()
    channel_title = channel.title
    channel_username = f"@{channel.username}" if channel.username else "Unknown"
    
    # Prepare the media path
    media_path = None
    if event.message.media and hasattr(event.message.media, 'photo'):
        filename = f"{channel_username}_{event.message.id}.jpg"
        media_path = os.path.join(media_dir, filename)
        await client.download_media(event.message.media, media_path)

    # Open the CSV in append mode to save real-time data
    with open('telegram_data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        save_message_to_csv(writer, channel_title, channel_username, event.message, media_path)
        print(f"New message saved from {channel_username}: {event.message.text}")

# Main function
async def main():
    await client.start()
    
    # Open the CSV file and prepare the writer for initial data scraping
    with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
        
        # List of channels to scrape
        channels = [
            '@meneshayeofficial'
        ]
        
        # Scrape past data from each channel
        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            print(f"Scraped past data from {channel}")

    print("Real-time ingestion has started. Listening for new messages...")
    # Real-time ingestion will run indefinitely

with client:
    client.loop.run_until_complete(main())
