from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor
import time

leftmotor = Motor("C")
rightmotor = Motor("A")

us_sensor = EV3UltrasonicSensor(1)

BAND_WIDTH = 3
BAND_CENTER = 20

if __name__ == "__main__":
    wait_ready_sensors()
    try:
        while(True):
            d = us_sensor.get_cm()

            if (d < BAND_CENTER - BAND_WIDTH):
                rightmotor.set_dps(20)
                leftmotor.set_dps(10)
            
            elif (d > BAND_CENTER + BAND_WIDTH):
                leftmotor.set_dps(20)
                rightmotor.set_dps(10)
            else:
                rightmotor.set_dps(20)
                leftmotor.set_dps(20)
            time.sleep(0.01)
            

    except BaseException:
        reset_brick()
        exit()

    reset_brick()