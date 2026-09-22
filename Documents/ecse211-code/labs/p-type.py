from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor
import time

leftmotor = Motor("C")
rightmotor = Motor("A")

us_sensor = EV3UltrasonicSensor(1)

BAND_CENTER = 20
BASE_SPEED = 20
FACTOR = 2

if __name__ == "__main__":
    wait_ready_sensors()
    try:
        while True:
            d = us_sensor.get_cm()

            if d > BAND_CENTER:
                leftmotor.set_dps(BASE_SPEED + abs(BAND_CENTER - d))
                rightmotor.set_dps(BASE_SPEED - abs(BAND_CENTER - d))

            elif d < BAND_CENTER:
                rightmotor.set_dps(BASE_SPEED + abs(BAND_CENTER - d))
                leftmotor.set_dps(BASE_SPEED - abs(BAND_CENTER - d))
            else:
                leftmotor.set_dps(BASE_SPEED)
                rightmotor.set_dps(BASE_SPEED)

            time.sleep(0.01)
    except BaseException:
        reset_brick()
        exit()

    reset_brick()


