from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor
import time

leftmotor = Motor("C")
rightmotor = Motor("B")

us_sensor = EV3UltrasonicSensor(1)

BAND_WIDTH = 10
BAND_CENTER = 30

def rotate(t) :
    initial = rightmotor.get_encoder()
    final = initial + t
    while(rightmotor.get_encoder() < final):
        rightmotor.set_dps(-t)
        leftmotor.set_dps(t)
        
        time.sleep(0.01)
if __name__ == "__main__":
    wait_ready_sensors()
    try:
        while(True):
            d = us_sensor.get_cm()
            print(f"distance: {d}")
            if (d > 200):
                rotate(-90)
                
            elif (d > BAND_CENTER - BAND_WIDTH):
                rightmotor.set_dps(-400)
                leftmotor.set_dps(-200)
            
            elif (d < BAND_CENTER + BAND_WIDTH):
                leftmotor.set_dps(-400)
                rightmotor.set_dps(-200)

            else:
                rightmotor.set_dps(-400)
                leftmotor.set_dps(-400)
            time.sleep(0.001)
            

    except BaseException:
        reset_brick()
        exit()
        
    reset_brick()
