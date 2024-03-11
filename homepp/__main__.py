import os

import websockets

import asyncio
import custom_logger
import websocket_client
import sensors

logger = custom_logger.setup_logger()


async def main():
    # todo: move to separate config file
    WEBSOCKET_URL = os.getenv("WEBSOCKET_URL", "123")
    HARDWARE_KEY = os.getenv("HARDWARE_KEY", "1234")
    # DEBUG = os.getenv("DEBUG", False)

    while True:
        try:
            websocket = await websocket_client.connect_websocket(WEBSOCKET_URL, HARDWARE_KEY)
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
            await asyncio.sleep(3)


async def send_data(websocket):
    try:
        while True:
            sensor_data: dict = await sensors.read_sensor_data()
            await websocket_client.send_data(websocket, sensor_data)
    except websockets.exceptions.ConnectionClosed:
        logger.error("Connection to server closed")
    except Exception as e:
        logger.error("An error occurred while sending sensor data: %s", e)


async def receive_data(websocket):
    try:
        while True:
            received_data = await websocket_client.receive_data(websocket)
            logger.info("Received data from server: %s", received_data)
    except websockets.exceptions.ConnectionClosed:
        logger.error("Connection to server closed")


if __name__ == "__main__":
    logger.info("Starting websocket client")
    asyncio.run(main())



