from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor

leftmotor = Motor("C")
rightmotor = Motor("A")

us_sensor = EV3UltrasonicSensor(1)

BAND_WIDTH = 3
BAND_CENTER = 20

#Fix Rotate: Add direction depending on angle
def rotate(angle, speed=90): 

    initial = rightmotor.get_encoder()
    final = initial + angle
    direction = speed if angle > 0 else -speed

    if angle > 0:
        while rightmotor.get_encoder() < final:
            rightmotor.set_dps(direction)
            leftmotor.set_dps(-direction)
            time.sleep(0.01)
    else:
        while rightmotor.get_encoder() > final:
            rightmotor.set_dps(direction)
            leftmotor.set_dps(-direction)
            time.sleep(0.01)
    
    #stop after completing the rotation
    rightmotor.set_dps(0)
    leftmotor.set_dps(0)


if __name__ == "__main__":
    wait_ready_sensors()
    try:
        while True:
            d = us_sensor.get_cm()

            if d <= 10:
                rotate(-90) #rotate right, robot too close to the wall

            elif d >= 60 and d <= 255:
                rotate(90) #rotate left, robot too far from the wall

            elif d < BAND_CENTER - BAND_WIDTH: #move away from the wall
                rightmotor.set_dps(100)
                leftmotor.set_dps(50)

            elif d > BAND_CENTER + BAND_WIDTH: #move closer to the wall
                leftmotor.set_dps(100)
                rightmotor.set_dps(50)

            else: #robot in bounds, just move forward
                rightmotor.set_dps(100)
                leftmotor.set_dps(100)
                
            time.sleep(0.01)

    except BaseException:
        reset_brick()
        exit()
    
    reset_brick()