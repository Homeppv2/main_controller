import json
import asyncio
import random
import websockets
import logging
import logging.config
from websockets.client import connect as ws_connect
from websockets.client import WebSocketClientProtocol

logger = logging.getLogger()


async def connect(url: str, key: str) -> WebSocketClientProtocol:
    while True:
        try:
            return await ws_connect(url, extra_headers={"HardwareKey": key})
        except ConnectionRefusedError as e:
            logger.error(e)
            logger.info("Reconnecting...")


async def send_data_from_sensors(ws: WebSocketClientProtocol) -> None:
    while True:
        events = await read_sensors()
        await ws.send(events)


async def listen_aggregator(ws: WebSocketClientProtocol) -> None:
    while True:
        text = await ws.recv()
        data = json.loads(text)
        match data:
            case {"type": "error"}:
                logger.info("Received error: %s" % data["detail"])


# TODO: add asyncio support for read data from sensors
async def read_sensors() -> str:
    await asyncio.sleep(2)
    return json.dumps(
        {"type": "some_sensor", "message": random.randint(0, 150)}
    )


async def main(ws_url: str, key: str, wait_seconds: int) -> None:
    websocket = None
    while wait_seconds:
        try:
            websocket = await connect(ws_url, key)
            logger.info("Connected to websocket")
            wait_seconds = 0
        except OSError:
            logger.info("Trying to connect: %s" % ws_url)
            await asyncio.sleep(1)
            wait_seconds -= 1

    if not websocket:
        logger.info("Connection failed")
    else:
        try:
            await asyncio.gather(
                send_data_from_sensors(websocket), listen_aggregator(websocket)
            )
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed by server")
        finally:
            # for aggregator disconnect exception handling
            await websocket.close(1002)


if __name__ == "__main__":
    # TODO: move to environment
    server = "ws://0.0.0.0:8010"
    key = "123"
    wait_seconds = 5
    logging_config_path = "homepp/config/logging_config.ini"

    logging.config.fileConfig(logging_config_path)
    try:
        logger.info("Started controller")
        asyncio.run(main(server, key, wait_seconds))
    except KeyboardInterrupt:
        logger.info("Shutdown controller")
