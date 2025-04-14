from pyrogram.client import Client
from config import *

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="techifybots",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"{me.first_name} is started...")
    async def stop(self, *args):
        await super().stop()
        me = await self.get_me()
        print(f"{me.first_name} is stopped...")


Bot().run()
