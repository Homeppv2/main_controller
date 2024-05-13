import asyncio
import ctypes
import datetime
import logging
import os
import random
from dotenv import load_dotenv

load_dotenv()

import aioserial

logger = logging.getLogger(__name__)

GENERATE_FAKE_VALUES = bool(int(os.getenv("GENERATE_FAKE_VALUES", False)))


def convert_hex_to_float(hex_string: str) -> float:
    hex_string = "0" * (8 - len(hex_string)) + hex_string

    converted_float = ctypes.c_float.from_buffer(bytearray.fromhex(hex_string))
    return converted_float.value


async def read_sensor_data() -> dict:
    serial_port = aioserial.AioSerial("/dev/ttyAMA0", 115200)
    received_data = (await serial_port.readline_async()).decode('utf-8')
    parsed_data = parse_received_data(received_data.split())

    ids_to_strings_dict = {
        16: "one",
        17: "two",
        18: "three"
    }
    ids_to_names_dict = {
        16: "controlerleack",
        17: "controlermodule",
        18: "controlerenviroment",

    }

    controller_data_name = ids_to_names_dict[parsed_data["sensor_info"]["type"]]
    sensor_data = parsed_data.get('sensor_data')

    parsed_data["sensor_info"][controller_data_name] = sensor_data

    formatted_data = {
        ids_to_strings_dict[parsed_data["sensor_info"]["type"]]: parsed_data["sensor_info"]

    }
    return formatted_data


def parse_received_data(received_frame):
    logger.debug(f"Got new data to parse: {received_frame}")
    received_frame = [("0" + x) if len(x) == 1 else x for x in received_frame]
    parsed_frame: dict[str: int | float] = {"sensor_info": {
        "type": int("".join(received_frame[0:2][::-1]), 16),
        "number": int("".join(received_frame[2:4][::-1]), 16),
        "status": int("".join(received_frame[4:6][::-1]), 16),
        "charge": int(received_frame[6], 16),
        "temperature_MK": int(received_frame[7], 8)
    }}

    # Разбор данных в зависимости от типа
    if parsed_frame["sensor_info"]["type"] == 16:
        parsed_frame["sensor_data"] = {
            "leack": int(received_frame[8], 16)
        }
    elif parsed_frame["sensor_info"]["type"] == 17:

        parsed_frame["sensor_data"] = {
            "temperature": "%.2f" % convert_hex_to_float("".join(received_frame[8:12])),
            "humidity": "%.2f" % convert_hex_to_float("".join(received_frame[12:16])),
            "pressure": "%.2f" % convert_hex_to_float("".join(received_frame[16:20])),
            "gas": int("".join(received_frame[20:22][::-1]), 16),
        }

    elif parsed_frame["sensor_info"]["type"] == 18:
        parsed_frame["sensor_data"] = {
            "temperature": "%.2f" % convert_hex_to_float("".join(received_frame[8:12])),
            "humidity": "%.2f" % convert_hex_to_float("".join(received_frame[12:16])),
            "pressure": "%.2f" % convert_hex_to_float("".join(received_frame[16:20])),
            "VOC": "%.2f" % convert_hex_to_float("".join(received_frame[20:24])),
            "gas1": int("".join(received_frame[24:28][::-1]), 16),
            "gas2": int("".join(received_frame[28:32][::-1]), 16),
            "gas3": int("".join(received_frame[32:26][::-1]), 16),
            "pm1": int("".join(received_frame[36:38][::-1]), 16),
            "pm25": int("".join(received_frame[38:40][::-1]), 16),
            "pm10": int("".join(received_frame[40:42][::-1]), 16),
            "fire": int("".join(received_frame[42:44][::-1]), 16),
            "smoke": int("".join(received_frame[44:46][::-1]), 16),
        }
    # elif parsed_frame["sensor_info"]["type"] == 19:
    #     # parsed_frame["sensor_info"]["name"] = "Датчик дыма и пожара"
    #     parsed_frame["sensor_data"] = {
    #         "smoke": int("".join(received_frame[8:10][::-1]), 16),
    #         "fire1": int("".join(received_frame[10:12][::-1]), 16),
    #         "fire2": int("".join(received_frame[12:14][::-1]), 16),
    #         "fire3": int("".join(received_frame[14:16][::-1]), 16),
    #         "fire4": int("".join(received_frame[16:18][::-1]), 16),
    #         "brightness": int("".join(received_frame[18:20][::-1]), 16),
    #     }
    # elif parsed_frame["sensor_info"]["type"] == 20:
    #     # parsed_frame["sensor_info"]["name"] = "Датчик CO2"
    #     parsed_frame["sensor_data"] = {
    #         "temperature": "%.2f" % convert_hex_to_float("".join(received_frame[8:12])),
    #         "humidity": "%.2f" % convert_hex_to_float("".join(received_frame[12:16])),
    #         "pressure": "%.2f" % convert_hex_to_float("".join(received_frame[16:20])),
    #         "TVOC": int("".join(received_frame[20:22][::-1]), 16),
    #         "ECO2": int("".join(received_frame[22:24][::-1]), 16),
    #         "AQI": int(received_frame[24], 16),
    #     }

    return parsed_frame


# if GENERATE_FAKE_VALUES:
#     # generate list of 10 fake ids
#     fake_ids = random.sample(range(1, 100), 10)
#     sensor_types_values = {
#         "gk": ["charge", ],
#         "module": ["temperature_MK", ],
#         "leak": ["leak", ],
#         "module_env": ["temperature", "humidity", "pressure", "gas", ],
#         "env": ["temperature", "humidity", "pressure", "VOC", "gas1", "gas2", "gas3", "pm1", "pm25", "pm10", "fire",
#                 "smoke", ]
#     }
#
#
#     async def read_sensor_data() -> dict:
#         await asyncio.sleep(random.randint(1, 10))
#         sensor_type = random.choice(list(sensor_types_values.keys()))
#         sensor_type_values = sensor_types_values[sensor_type]
#         current_time = datetime.datetime.now()
#
#         parsed_data = {}
#         for value in sensor_type_values:
#             parsed_data[value] = random.randint(0, 100)
#
#         fake_data = {
#             "id": random.choice(fake_ids),
#             "type": 0,
#             "number": 1,
#             "status": 1,
#             "charge": parsed_data.get("charge", None),
#             "temperature_MK": parsed_data.get("temperature_MK", None),
#             "data": {
#                 "second": current_time.second,
#                 "minute": current_time.minute,
#                 "hour": current_time.hour,
#                 "day": current_time.day,
#                 "month": current_time.month,
#                 "year": current_time.year
#             },
#         }
#
#         if sensor_type == "gk":
#             fake_data += {
#                 "controlergk": {
#                     "charge": parsed_data.get("charge", None)
#                 }
#             }
#
#         if sensor_type == "module":
#             fake_data += {
#                 "temperature_MK": parsed_data.get("temperature_MK", None)
#             },
#
#         if sensor_type == "leak":
#             fake_data += {
#                 "controlerleak": {
#                     "leak": parsed_data.get("leak", None)
#                 },
#             }
#         if sensor_type == "module_env":
#             fake_data += {
#                 "controlermodule": {
#                     "temperature": parsed_data.get("temperature", None),
#                     "humidity": parsed_data.get("humidity", None),
#                     "pressure": parsed_data.get("pressure", None),
#                     "gas": parsed_data.get("gas", None)
#                 },
#             }
#         if sensor_type == "env":
#             fake_data += {
#                 "controlerenviroment": {
#                     "temperature": parsed_data.get("temperature", None),
#                     "humidity": parsed_data.get("humidity", None),
#                     "pressure": parsed_data.get("pressure", None),
#                     "VOC": parsed_data.get("VOC", None),
#                     "gas1": parsed_data.get("gas1", None),
#                     "gas2": parsed_data.get("gas2", None),
#                     "gas3": parsed_data.get("gas3", None),
#                     "pm1": parsed_data.get("pm1", None),
#                     "pm25": parsed_data.get("pm25", None),
#                     "pm10": parsed_data.get("pm10", None),
#                     "fire": parsed_data.get("fire", None),
#                     "smoke": parsed_data.get("smoke", None)
#                 }
#             }
#
#         return fake_data


if __name__ == "__main__":
    for received_data in (
            # ['11', '0', '1', '0', '0', '0', 'FF', '0', '1F', '85', 'CF', '41', '0', '57', '4', '42', '71', 'C2', '79',
            #  '44',
            #  '0', '0', 'C0'],
            # ['11', '0', '1', '0', '0', '0', 'FF', '0', '5C', '8F', 'D0', '41', '0', '83', '6', '42', '38', 'C1', '79',
            #  '44',
            #  '0', '0', 'C0'],
            # ['11', '0', '1', '0', '0', '0', 'FF', '0', 'A', 'D7', 'D1', '41', '0', '73', '8', '42', 'EC', 'C0', '79',
            #  '44', '0',
            #  '0', 'C0'],
            # "11 0 1 0 1 0 ff 0 0 0 0 0 5c 8f ae 41 0 7 31 42 80 89 78 44 30 0 0 0".split(),
            "11 0 1 0 1 0 ff 0 52 b8 d6 41 0 a e 42 a9 f3 76 44 2b 0".split(),

    ):
        print(received_data)
        parsed_data = parse_received_data(received_data)
        print(parsed_data)

        ids_to_strings_dict = {
            16: "one",
            17: "two",
            18: "three"
        }
        ids_to_names_dict = {
            16: "controlerleack",
            17: "controlermodule",
            18: "controlerenviroment",

        }

        controller_data_name = ids_to_names_dict[parsed_data["sensor_info"]["type"]]
        sensor_data = parsed_data.get('sensor_data')

        parsed_data["sensor_info"][controller_data_name] = sensor_data

        formatted_data = {
            ids_to_strings_dict[parsed_data["sensor_info"]["type"]]: parsed_data["sensor_info"]

        }

        print(formatted_data)
