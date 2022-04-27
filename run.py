import logging

import RPi.GPIO as GPIO
import asyncio
import time


PIN = 4
ON_DELAY = 1.0  # sec
OFF_DELAY = 12.0  # sec

logging.basicConfig(filename='logs/async_relay_controller.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


async def on(pin):
    GPIO.output(pin, GPIO.LOW)
    await asyncio.sleep(ON_DELAY)


async def off(pin):
    GPIO.output(pin, GPIO.HIGH)
    await asyncio.sleep(OFF_DELAY)


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
