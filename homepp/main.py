import os

import websockets

import asyncio
import custom_logger
import websocket_client
import sensors

logger = custom_logger.setup_logger()


async def main():
    websocket_url = os.getenv("WEBSOCKET_URL", "ws://0.0.0.0:8010")
    hardware_key = os.getenv("HARDWARE_KEY", "123")

    while True:
        try:
            websocket = await websocket_client.connect_websocket(websocket_url, hardware_key)
            if websocket:
                await asyncio.gather(
                    send_data(websocket),
                    receive_data(websocket)
                )
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.error("An error occurred: %s", e)
        finally:
            logger.info("Reconnecting...")
            await asyncio.sleep(1)


async def send_data(websocket):
    try:
        while True:
            sensor_data = await sensors.read_sensor_data()
            await websocket_client.send_data(websocket, sensor_data)
    except websockets.exceptions.ConnectionClosed:
        logger.error("Connection to server closed")


async def receive_data(websocket):
    try:
        while True:
            received_data = await websocket_client.receive_data(websocket)
            logger.info("Received data from server: %s", received_data)
    except websockets.exceptions.ConnectionClosed:
        logger.error("Connection to server closed")


if __name__ == "__main__":
    asyncio.run(main())



