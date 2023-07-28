import asyncio
import random
import os
from datetime import datetime, timedelta

from nio import AsyncClient, RoomMessageImage

MATRIX_HOMESERVER_URL = os.getenv('MATRIX_HOMESERVER_URL')
MATRIX_USERNAME = os.getenv('MATRIX_USERNAME')
MATRIX_PASSWORD = os.getenv('MATRIX_PASSWORD')
MATRIX_ACCESS_TOKEN = os.getenv('MATRIX_ACCESS_TOKEN')
TIME_TO_POST = os.getenv('TIME_TO_POST')
MINIMAL_AGE = os.getenv('MINIMAL_AGE')

class MatrixBot:
    def __init__(self):
        self.client = AsyncClient(MATRIX_HOMESERVER_URL, MATRIX_USERNAME)
        self.client.access_token = MATRIX_ACCESS_TOKEN

    async def fetch_room_media(self, room_id):
        media_list = []
        token = "END"  # a not None start token, actual value doesn't matter

        while True:
            # fetch room messages
            response = await self.client.room_messages(room_id, token)
            token = response.end

            # add media messages to the list
            media_list.extend([
                msg for msg in response.chunk
                if isinstance(msg, RoomMessageImage)
                and "url" in msg.source["content"]  # only media messages have 'url'
                and int(MINIMAL_AGE) <= int(msg.source["age"])
                ])

            if token is None:  # all messages have been fetched
                break

        return media_list

    async def send_media_message(self, random_media):
        await self.client.room_send(
                room_id=random_media.source["room_id"],
                message_type="m.room.message",
                content=random_media.source["content"]
                )

    async def daily_action(self):
        while True:
            # calculate how long until TIME_TO_POST
            now = datetime.now()
            target_time = datetime.strptime(TIME_TO_POST, "%H:%M").replace(year=now.year, month=now.month, day=now.day)

            if now > target_time:
                # if now surpassed today's target, calculate for next day
                target_time += timedelta(days=1)

            # wait until the target_time
            await asyncio.sleep((target_time - now).total_seconds())

            response = await self.client.joined_rooms()
            for room in response.rooms:
                # fetch room media then randomly select and send one
                media_list = await self.fetch_room_media(room)
                random_media = random.choice(media_list)
                await self.send_media_message(random_media)

    async def run(self):
        # login
        await self.client.login(MATRIX_PASSWORD)

        # run the daily action
        asyncio.create_task(self.daily_action())

        # keeps the bot running
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    bot = MatrixBot()
    asyncio.run(bot.run())
