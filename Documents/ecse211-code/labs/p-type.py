from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor

leftmotor = Motor("C")
rightmotor = Motor("A")

us_sensor = EV3UltrasonicSensor(1)

BAND_CENTER = 20
BASE_SPEED = 100
FACTOR = 2  # proportional gain 

if __name__ == "__main__":
    wait_ready_sensors()
    try:
        while True:
            d = us_sensor.get_cm()

            error = d - BAND_CENTER      # positive means too far from wall, negative means too close
            correction = FACTOR * error  # scales with the size of the error

            leftmotor.set_dps(BASE_SPEED + correction)
            rightmotor.set_dps(BASE_SPEED - correction)

            time.sleep(0.01)
    except BaseException:
        reset_brick()
        exit()
    
    reset_brick()