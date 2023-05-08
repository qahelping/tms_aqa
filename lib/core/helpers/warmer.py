from time import sleep

import asyncio
import aiohttp


class Warmer:

    def __init__(self, urls):
        Warmer.up(urls)

    TIMEOUT = 120

    @staticmethod
    async def get(url):
        async with aiohttp.ClientSession() as session:
            seconds_passed = 0
            while seconds_passed < Warmer.TIMEOUT:
                try:
                    timeout = (Warmer.TIMEOUT - seconds_passed)
                    async with session.get(url, timeout=timeout) as response:
                        return response
                except aiohttp.ClientConnectorError:
                    sleep(1)
                    seconds_passed = seconds_passed + 1

    @staticmethod
    def up(urls):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        tasks = [Warmer.get(url) for url in urls]
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()
