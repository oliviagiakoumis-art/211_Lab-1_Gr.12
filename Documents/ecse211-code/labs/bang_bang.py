from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor
import time

leftmotor = Motor("C")
rightmotor = Motor("A")

us_sensor = EV3UltrasonicSensor(1)

BAND_WIDTH = 7
BAND_CENTER = 20

if __name__ == "__main__":
    wait_ready_sensors()
    try:
        d = us_sensor.get_cm()

        while(d < BAND_CENTER - BAND_WIDTH):
            rightmotor.set_dps(20)
            leftmotor.set_dps(10)
            time.sleep(0.01)
            d = us_sensor.get_cm()

        while(d > BAND_CENTER + BAND_WIDTH):
            leftmotor.set_dps(20)
            rightmotor.set_dps(10)
            time.sleep(0.01)
            d = us_sensor.get_cm()

    except BaseException:
        reset_brick()
        exit()

    reset_brick()