"""Simple delay demo coroutine"""
import asyncio


async def delay(delay_seconds: int) -> int:
    print(f"`delay`: sleeping for {delay_seconds} second(s)")
    await asyncio.sleep(delay_seconds)
    print(f"`delay`: finished sleeping for {delay_seconds} second(s)")
    return delay_seconds
