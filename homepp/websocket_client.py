import websockets
import logging
import json
import asyncio
from websockets.client import WebSocketClientProtocol

logger = logging.getLogger(__name__)


async def connect_websocket(url: str, key: str) -> WebSocketClientProtocol:
        while True:
        try:
            websocket = await websockets.connect(url, extra_headers={"HardwareKey": key})
            logger.info("Connected to websocket")
            return websocket
        except ConnectionRefusedError as e:
            logger.error(e)
            logger.info("Reconnecting...")
            await asyncio.sleep(1)


async def receive_from_websocket(websocket: WebSocketClientProtocol) -> None:
    while True:
        text = await websocket.recv()
        data = json.loads(text)
        if data.get("type") == "error":
            logger.info("Received error: %s", data.get("detail"))




async def send_data(websocket: 'WebSocketClientProtocol', data: dict) -> None:
    await websocket.send(json.dumps(data))

async def receive_data(websocket: 'WebSocketClientProtocol') -> dict:
    data = await websocket.recv()
    return json.loads(data)

