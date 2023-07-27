import asyncio
import random
import os
from datetime import datetime, timedelta

from nio import AsyncClient, RoomMessagesResponse

MATRIX_HOMESERVER_URL = os.getenv('MATRIX_HOMESERVER_URL')
MATRIX_USERNAME = os.getenv('MATRIX_USERNAME')
MATRIX_PASSWORD = os.getenv('MATRIX_PASSWORD')
MATRIX_ACCESS_TOKEN = os.getenv('MATRIX_ACCESS_TOKEN')
TIME_TO_POST = os.getenv('TIME_TO_POST')

class MatrixBot:
    def __init__(self):
        self.client = AsyncClient(MATRIX_HOMESERVER_URL, MATRIX_USERNAME)
        self.client.access_token = MATRIX_ACCESS_TOKEN
        self.room_id = None

    async def autojoin_rooms(self):
        response = await self.client.joined_rooms()

        for room in response.rooms:
            self.room_id = room

    async def fetch_room_media(self):
        media_only = []
        token = "END"  # a not None start token, actual value doesn't matter

        while True:
            # get several last messages
            response = await self.client.room_messages(self.room_id, token)
            token = response.end

            # add media messages to the list
            media_only.extend([
                msg for msg in response.chunk
                if isinstance(msg, RoomMessagesResponse)
                and "url" in msg.content  # only media messages have 'url'
            ])

            if token is None:  # all messages have been fetched
                break

        return media_only

    async def pick_random_media(self, media_list):
        if len(media_list) == 0:
            # handle the empty list somehow. For example, raise an exception:
            raise ValueError("No media found in the provided list")

        random_media = random.choice(media_list)
        media_url = random_media.content["url"]

        return media_url

    async def send_media_message(self, media_url):
        await self.client.room_send(
            room_id=self.room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.image",
                "url": media_url,
            }
        )

    async def daily_action(self):
        while True:
            # calc how long until TIME_TO_POST
            now = datetime.now()
            target_time = datetime.strptime(TIME_TO_POST, "%H:%M").replace(year=now.year, month=now.month, day=now.day)

            if now > target_time:
                # if now surpassed today's target, calculate for next day
                target_time += timedelta(days=1)

            # wait until the target_time
            await asyncio.sleep((target_time - now).total_seconds())

            # fetch old media then select and send one
            old_media = await self.fetch_room_media()
            media_to_send_url = await self.pick_random_media(old_media)
            await self.send_media_message(media_to_send_url)

    async def run(self):
        # login
        await self.client.login(MATRIX_PASSWORD)

        # auto-join rooms
        await self.autojoin_rooms()

        # run the daily action
        asyncio.create_task(self.daily_action())

        # keeps the bot running
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    bot = MatrixBot()
    asyncio.run(bot.run())
