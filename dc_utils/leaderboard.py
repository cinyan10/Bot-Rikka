import asyncio
import datetime

from dc_utils.localstats import get_playtime_rank


async def update_gokzcn_rank_7am(channel):
    while True:
        current_time = datetime.datetime.now()

        if current_time.hour == 7 and current_time.minute == 0:
            await get_playtime_rank(channel)
            await asyncio.sleep(24 * 60 * 60)
        else:
            await asyncio.sleep(60)


async def update_playtime_rank_7am(channel):
    while True:
        current_time = datetime.datetime.now()

        if current_time.hour == 1:  # and current_time.minute == 0:
            await get_playtime_rank(channel)
            await asyncio.sleep(24 * 60 * 60)
        else:
            await asyncio.sleep(60)

