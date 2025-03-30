import threading
from Sophia import *
from pyrogram import Client, filters
import os
from pyrogram import idle
from subprocess import getoutput as r
from Restart import restart_program
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

PWD = f"{os.getcwd()}/"
my_id = None

PHOTO_URL = os.getenv("STARTUP_PHOTO_URL", "http://ibb.co/zNPxZZy")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "@Paradopia")


if __name__ == "__main__":
    Sophia.start()
    SophiaBot.start()
    try:
        SophiaBot.send_photo(
            Sophia.me.id,
            photo=PHOTO_URL,
            caption=(
                f"**✅ System Started ⚡**\n\n"
                f"**👾 Version:** {MY_VERSION}\n"
                f"**🥀 Python:** {r('python --version').lower().split('python ')[1]}\n"
                f"**🐬 Owner:** {Sophia.me.first_name if not Sophia.me.last_name else f'{Sophia.me.first_name} {Sophia.me.first_name}'}\n"
                f"**🦋 Join:** {CHANNEL_LINK} & @ParadopiaSupport"
            )
        )
    except Exception as e:
        logger.error(f"Error sending startup message: {e}")

    idle()
