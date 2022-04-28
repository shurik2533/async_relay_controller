import datetime
import logging

import RPi.GPIO as GPIO
import asyncio
import time


PIN = 4
DAY_ON_DELAY = 1.5  # sec
DAY_OFF_DELAY = 120.0  # sec
NIGHT_ON_DELAY = 2  # sec
NIGHT_OFF_DELAY = 420.0  # sec
DAY_START_TIME = '04:00:00'
DAY_END_TIME = '23:00:00'

GPIO.setmode(GPIO.BCM)
CHANNELS = [PIN]
[GPIO.setup(channel, GPIO.OUT) for channel in CHANNELS]
[GPIO.output(channel, GPIO.HIGH) for channel in CHANNELS]

logging.basicConfig(filename='logs/async_relay_controller.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


def get_daytime():
    def time_in_range(start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def get_time(time_str):
        time_list = time_str.split(':')
        return datetime.time(int(time_list[0]), int(time_list[1]), int(time_list[2]))

    if time_in_range(get_time(DAY_START_TIME), get_time(DAY_END_TIME), datetime.datetime.now().time()):
        return 'DAY'
    return 'NIGHT'


def get_on_delay():
    return DAY_ON_DELAY if get_daytime() == 'DAY' else NIGHT_ON_DELAY


def get_off_delay():
    return DAY_OFF_DELAY if get_daytime() == 'DAY' else NIGHT_OFF_DELAY


async def on(pin):
    GPIO.output(pin, GPIO.LOW)
    await asyncio.sleep(get_on_delay())


async def off(pin):
    GPIO.output(pin, GPIO.HIGH)
    await asyncio.sleep(get_off_delay())


async def main():
    try:
        while True:
            start_time = time.time()
            await on(PIN)
            logging.info(f'ON for {round(time.time() - start_time, 2)} sec')
            start_time = time.time()
            await off(PIN)
            logging.info(f'OFF for {round(time.time() - start_time, 2)} sec')
    finally:
        GPIO.cleanup()
        pass


if __name__ == '__main__':
    asyncio.run(main())
