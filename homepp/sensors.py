import asyncio
import json
import random


# TODO: add asyncio support for read data from sensors
async def read_sensor_data() -> str:
    await asyncio.sleep(2)
    return json.dumps(
        {"type": "some_sensor", "message": random.randint(0, 150)}
    )