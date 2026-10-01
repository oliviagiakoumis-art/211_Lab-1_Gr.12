from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor

leftmotor = Motor("C")
rightmotor = Motor("A")

us_sensor = EV3UltrasonicSensor(1)

BAND_CENTER = 20
BASE_SPEED = -100

FACTOR = 3  # proportional gain 

if __name__ == "__main__":
    wait_ready_sensors()
    count = 0
    try:
        while True:
            d = us_sensor.get_cm()
            print(f"distance: {d}, correction: {d - BAND_CENTER}, count: {count}")
            error = d - BAND_CENTER     # positive means too far from wall, negative means too close
            correction = FACTOR * error  # scales with the size of the error
            if d >= 235:
                count += 1
            else:
                count = 0
                
            if 10 < count < 100:
                correction = 25
                
            leftmotor.set_dps((BASE_SPEED-100) + correction)
            rightmotor.set_dps(BASE_SPEED - correction)

            if d < 7:
                    # Move backwards / away from wall
                    rightmotor.set_dps(220)
                    leftmotor.set_dps(100)
                    time.sleep(1.5)
                    rightmotor.set_dps(-100)
                    leftmotor.set_dps(-150)
                    time.sleep(0.5)
                    leftmotor.set_dps(-100)
                    rightmotor.set_dps(-100)
                    time.sleep(0.2)

            time.sleep(0.01)
    except BaseException:
        reset_brick()
        exit()
    
    reset_brick()