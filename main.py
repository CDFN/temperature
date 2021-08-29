import threading
import time
import serial
import mysql.connector


class RepeatThread(threading.Thread):

    def __init__(self, interval, f):
        super().__init__()
        self.interval = interval
        self.f = f

    def start(self):
        while True:
            self.f()
            time.sleep(self.interval)


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


def read():
    a = ser.read(2048).decode('UTF-8')
    if a == "":
        return
    split = a.split(':')
    if len(split) < 2:
        return
    query = f"insert into temperature(temperature, pressure) values ({split[0]}, {split[1]})"
    with mysql.connector.connect(host="localhost", user="root",
                                 password="passwd",
                                 database="temperature") as db:
        with db.cursor() as cursor:
            cursor.execute(query)
            db.commit()
            t = time.strftime("%H:%M:%S", time.localtime())
            print(f"Inserted {cursor.rowcount} at {t}")


t = RepeatThread(1.0, read)
t.start()
while True:
    pass
