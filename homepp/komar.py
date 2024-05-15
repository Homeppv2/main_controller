import ctypes

# # Создание числа типа float
# original_float = 12.33
# original_hex = "".join(["ae", "47", "45", "41"][::-1]).lower()
#
# # Перевод числа в массив байтов
# byte_array = bytearray.fromhex(original_hex)
#
# # Печать массива байтов
# print("Массив байтов:", byte_array)
#
# # Преобразование массива байтов обратно в число типа float
# converted_float = ctypes.c_float.from_buffer(bytearray.fromhex(original_hex))
#
# # Печать восстановленного числа
# print("Восстановленное число float:", converted_float.value)
#
#
# # rework this code to work with data in hex format, for example "AABBCCDD" string
#
# # Создание строки в шестнадцатеричном формате
# original_hex = "41a8f5c3"

# Перевод строки в массив байтов
# byte_array = bytearray.fromhex(original_hex)



# rewrite this code to work with data in hex format, for example "ae474541" string, ideally using list of strings

# Создание строки в шестнадцатеричном формате
original_hex = ["52", "b8", "d6", "41"]

# Перевод строки в массив байтов
byte_array = bytearray.fromhex("".join(original_hex))

# print in normal format
for byte in byte_array:
    print(format(byte, "02x"), end=" ")

# Преобразование массива байтов обратно в число типа float
converted_float = ctypes.c_float.from_buffer(bytearray.fromhex("".join(original_hex)))

# Печать восстановленного числа
print("Восстановленное число float:", converted_float.value)
# Path: homepp/komar.py
# Compare this snippet from homepp/__main__.py:
# import os
