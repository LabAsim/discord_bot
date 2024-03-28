# This example requires the 'message_content' intent.
import logging

import colorama

from core import bot
from helper import color_logging
from saved_tokens import BOT_TOKEN

logger = logging.getLogger(__name__)


# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f'Logged on as {self.user}!')
#
#     async def on_message(self, message):
#         print(f'Message from {message.author}: {message.content}')

# client = MyClient(intents=intents)
# client.run(token)

def main():
    level = logging.DEBUG
    console = color_logging(level=level)
    logging.basicConfig(
        level=level,
        force=True,
        handlers=[console],
    )  # Force is needed here to re config logging
    # Init should be here so as the colors be rendered properly in fly.io
    colorama.init(convert=True)

    bot.run(token=BOT_TOKEN)


if __name__ == "__main__":
    main()
