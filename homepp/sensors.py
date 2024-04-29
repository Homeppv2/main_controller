import asyncio
import datetime
import logging
import os
import random

import aioserial

logger = logging.getLogger(__name__)

GENERATE_FAKE_VALUES = bool(int(os.getenv("GENERATE_FAKE_VALUES", False)))


async def read_sensor_data() -> dict:
    serial_port = aioserial.AioSerial("/dev/ttyAMA0", 115200)
    received_data = (await serial_port.readline_async()).decode('utf-8')
    parsed_data = parse_received_data(received_data)


    ids_to_strings_dict = {
        16: "one",
        17: "two",
        18: "three"
    }

    formatted_data = {ids_to_strings_dict[parsed_data["sensor_info"]["id"]]: parsed_data["sensor_info"]}
    # todo: one, two, three things
    if parsed_data["sensor_info"]["id"] == 16:
        ...
    elif parsed_data["sensor_info"]["id"] == 17:

        formatted_data["controlermodule"] = parsed_data["sensor_data"]

    return formatted_data




def parse_received_data(received_frame):
    print(received_frame)
    received_frame = [x if x != "0" else "00" for x in received_frame]
    received_data = received_frame[4:]
    parsed_data = {}
    parsed_data["sensor_info"] = {"id": int((received_frame[0] + received_frame[1])[::-1], 16),
                                  "number": int((received_frame[2] + received_frame[3])[::-1], 16),
                                  "status": int((received_data[0] + received_data[1])[::-1], 16),
                                  "charge": int(received_data[2][::-1], 16)}

    # Разбор данных в зависимости от типа
    if parsed_data["sensor_info"]["id"] == 16:  # Датчик протечки
        parsed_data["sensor_data"]["name"] = "Датчик протечки"
        parsed_data["sensor_data"] = {
            "leak": int(received_data[3], 8)
        }
    elif parsed_data["sensor_info"]["id"] == 17:  # Модульный датчик
        print(
            "".join(received_data[3:7][::-1]),
            "".join(received_data[7:11][::-1]),
            "".join(received_data[11:15][::-1]),
            "".join(received_data[15:19][::-1]),
        )
        parsed_data["sensor_info"]["name"] = "Модульный датчик"
        parsed_data["sensor_data"] = {
            "temperature": int("".join(received_data[3:7][::-1]), 16),
            "humidity": int("".join(received_data[7:11][::-1]), 16),
            "pressure": int("".join(received_data[11:15][::-1]), 16),
            "gas": int("".join(received_data[15:19][::-1]), 16)
        }


    elif parsed_data["sensor_info"]["id"] == 18:  # Датчик окружающей среды
        parsed_data["sensor_info"]["name"] = "Датчик окружающей среды"

        parsed_data["sensor_data"] = {
            "temperature": int("".join(received_data[3:7][::-1]), 16),
            "humidity": int("".join(received_data[7:11][::-1]), 16),
            "pressure": int("".join(received_data[11:15][::-1]), 16),
            "VOC": int("".join(received_data[15:19][::-1]), 16),
            "gas1": int("".join(received_data[19:23][::-1]), 16),
            "gas2": int("".join(received_data[23:27][::-1]), 16),
            "gas3": int("".join(received_data[27:31][::-1]), 16),
            "pm1": int("".join(received_data[31:33][::-1]), 16),
            "pm25": int("".join(received_data[33:35][::-1]), 16),
            "pm10": int("".join(received_data[35:37][::-1]), 16),
            "fire": int("".join(received_data[37:39][::-1]), 16),
            "smoke": int(received_data[39], 16)
        }


    return parsed_data


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
            ['11', '0', '1', '0', '0', '0', 'FF', '0', '1F', '85', 'CF', '41', '0', '57', '4', '42', '71', 'C2', '79',
             '44',
             '0', '0', 'C0'],
            ['11', '0', '1', '0', '0', '0', 'FF', '0', '5C', '8F', 'D0', '41', '0', '83', '6', '42', '38', 'C1', '79',
             '44',
             '0', '0', 'C0'],
            ['11', '0', '1', '0', '0', '0', 'FF', '0', 'A', 'D7', 'D1', '41', '0', '73', '8', '42', 'EC', 'C0', '79',
             '44', '0',
             '0', 'C0']
    ):
        print(received_data)
        parsed_data = parse_received_data(received_data)
        print(parsed_data)
