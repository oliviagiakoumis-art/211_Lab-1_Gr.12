from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor
import time

leftmotor = Motor("C")
rightmotor = Motor("A")

us_sensor = EV3UltrasonicSensor(1)

BAND_WIDTH = 10
BAND_CENTER = 40

def rotate(t):
    initial = rightmotor.get_encoder()
        
    while True:
        current = rightmotor.get_encoder()
        delta = ((current - initial + 2**31) % 2**32) - 2**31
        if (t > 0 and delta >= t) or (t < 0 and delta <= t):
            break
        
        rightmotor.set_dps(t)
        leftmotor.set_dps(-t)       
        time.sleep(0.2)
        rightmotor.set_dps(-140)
        leftmotor.set_dps(-140)
        time.sleep(0.3)
        
    rightmotor.set_dps(-0)
    leftmotor.set_dps(-0)
    
if __name__ == "__main__":
    wait_ready_sensors()
    try:
        while(True):
            d = us_sensor.get_cm()
            time.sleep(0.01)
            d2 = us_sensor.get_cm()
            time.sleep(0.01)
            d3 = us_sensor.get_cm()
            
            print(f"distance: {d} {d2} {d3}")
            
            if (d3 < 13): # move backwards
                rightmotor.set_dps(200)
                leftmotor.set_dps(200)
                time.sleep(1.2)
            if (d3 > 40):
                rightmotor.set_dps(-220)
                leftmotor.set_dps(-70)
                time.sleep(1)
            elif (d3 < 25):
                leftmotor.set_dps(-220)
                rightmotor.set_dps(-70) 
                time.sleep(1)
            else:
                leftmotor.set_dps(-350)
                rightmotor.set_dps(-350)
                time.sleep(0.1)
                
            if (d > 200 and d2 > 200 and d3 > 200):
                rotate(-100)
            
            time.sleep(0.05)

    except BaseException:
        reset_brick()
        exit()
        
    reset_brick()