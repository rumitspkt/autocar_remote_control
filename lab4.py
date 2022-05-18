from __future__ import print_function, division, absolute_import

import time

from robust_serial import write_order, Order, write_i8, write_i16, read_i8, read_order
from robust_serial.utils import open_serial_port

import pyrebase

config = {
    "apiKey": "AIzaSyC9I-94xLGtyWtQno72t1i5AZn4CZS-L5k",
    "authDomain": "lab4-6a6ab.firebaseapp.com",
    "databaseURL": "https://lab4-6a6ab-default-rtdb.firebaseio.com",
    "projectId": "lab4-6a6ab",
    "storageBucket": "lab4-6a6ab.appspot.com",
    "messagingSenderId": "503487597563",
    "appId": "1:503487597563:web:93ec464731f03ba80a595e"
}

firebase = pyrebase.initialize_app(config)

LED_ON = 1
LED_OFF = 2

if __name__ == '__main__':

    try:
        serial_file = open_serial_port(baudrate=115200, timeout=None)
    except Exception as e:
        raise e

    is_connected = False
    # Initialize communication with Arduino
    while not is_connected:
        print("Waiting for arduino...")
        write_order(serial_file, Order.HELLO)
        bytes_array = bytearray(serial_file.read(1))
        if not bytes_array:
            time.sleep(2)
            continue
        byte = bytes_array[0]
        if byte in [Order.HELLO.value, Order.ALREADY_CONNECTED.value]:
            is_connected = True

    print("Connected to Arduino")

    try:
        while True:
            database = firebase.database()
            ProjectBucket = database.child("project-503487597563")
            ledValue = ProjectBucket.child("LED").get().val()

            if str(ledValue) == "\"OFF\"":
                print("LED now is OFF.")
                write_order(serial_file, Order.HELLO)
                write_i8(serial_file, 2)
            else:
                print("LED now is ON.")
                write_order(serial_file, Order.HELLO)
                write_i8(serial_file, 1)

    except KeyboardInterrupt:
        print("Stopped")

