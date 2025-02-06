import os
import threading
import logging
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from Mukund import Mukund
from flask import Flask
import random

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Create Flask app for health check
web_app = Flask(__name__)

@web_app.route('/health')
def health_check():
    return "OK", 200

def run_flask():
    web_app.run(host="0.0.0.0", port=8000)

# Initialize Mukund database
storage = Mukund("Vegeta")
db = storage.database("cric")

# Initialize Pyrogram bot with optimizations
bot = Client(
    "pro",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("SESSION"),
    workers=10,  # Increased for better concurrency
    max_concurrent_transmissions=5  # Handles multiple updates simultaneously
)



@bot.on_message(filters.photo & filters.user([7742832624]))
async def hacke(c: Client, m: Message):
    try:
        await asyncio.sleep(random.uniform(0.5, 1.0))  # Small delay

        if m.caption and "/ᴄᴏʟʟᴇᴄᴛ" in m.caption:
            logging.info(f"Detected message with caption: {m.caption}")
            file_data = db.get(m.photo.file_unique_id)

            if file_data:
                logging.info(f"Image ID {m.photo.file_unique_id} found in DB: {file_data['name']}")

                # Send /collect command
                await m.reply(f"/collect {file_data['name']}")

                # Wait a bit before sending reaction message
                await asyncio.sleep(random.uniform(2.0, 4.0))  

                # Fun messages after collecting
                fun_responses = [
                    "Camping ke fayde ",
                    "Successfully chori kr liya",
                    "OP",
                    "OP bhai OP ",
                    "Hell yeah! ",
                    "Fuck yeah! "
                ]
                fun_response = random.choice(fun_responses)
                await m.reply(fun_response)

            else:
                logging.warning(f"Image ID {m.photo.file_unique_id} not found in DB!")

    except FloodWait as e:
        logging.warning(f"Rate limit hit! Waiting for {e.value} seconds...")
        await asyncio.sleep(e.value)

    except Exception as e:
        logging.error(f"Error processing message: {e}")
# Start both Flask and Pyrogram using threading
if __name__ == "__main__":
    logging.info("Starting Flask server and Pyrogram bot...")
    threading.Thread(target=run_flask, daemon=True).start()

    bot.start()  # Start the bot
    idle()  # Keeps the bot running efficiently
    bot.stop()  # Stops the bot when exiting
