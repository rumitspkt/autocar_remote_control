from __future__ import print_function, division, absolute_import

import time

from robust_serial import write_order, Order, write_i8, write_i16, read_i8, read_order
from robust_serial.utils import open_serial_port

import pyrebase

config = {
    "apiKey": "AIzaSyB3kmpKBsxo7crCAEBwWLd8VKPveqssRqs",
    "authDomain": "lab-5-3ba59.firebaseapp.com",
    "databaseURL": "https://lab-5-3ba59-default-rtdb.firebaseio.com",
    "projectId": "lab-5-3ba59",
    "storageBucket": "lab-5-3ba59.appspot.com",
    "messagingSenderId": "284326813891",
    "appId": "1:284326813891:web:2de26d00cc7609acb44276"
}

firebase = pyrebase.initialize_app(config)

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
            devices = database.child("devices")
            Keys = devices.child("Keys")
            state = Keys.child("state").get().val()
            level = Keys.child("level").get().val()

            if state:
                print("LED22 now is ON.")
                # GPIO.output(LED22, GPIO.HIGH)
            else:
                print("LED22 now is OFF.")
                # GPIO.output(LED22, GPIO.LOW)


    except KeyboardInterrupt:
        print("CLEAN UP GPIO")
        # clean GPIO
        # GPIO.cleanup()
