from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor

# Initialize sensors and motors (Update ports if necessary)
us_sensor = EV3UltrasonicSensor(1)
left_motor = Motor("C")
right_motor = Motor("B")

# Lab 1 Bang-Bang Parameters
BAND_CENTER = 20    # Target distance in cm
BAND_WIDTH = 3      # Acceptable tolerance in cm[cite: 1]
BASE_SPEED = -100    # Nominal driving speed (Degrees Per Second)

LOWER_THRESHOLD = BAND_CENTER - BAND_WIDTH  # 17 cm
UPPER_THRESHOLD = BAND_CENTER + BAND_WIDTH  # 23 cm


if __name__ == "__main__":
    wait_ready_sensors()
    
    try:
        print("Running Bang-Bang Controller (Wall on Left)...")
        while True:
            distance = us_sensor.get_cm()
            
            if distance is not None:
                print(f"Distance: {distance} cm")
                
                if distance < LOWER_THRESHOLD:
                    # Too close to left wall: steer right away from wall (fast left, slow right)
                    left_motor.set_dps(-100)
                    right_motor.set_dps(-150)
                elif distance > UPPER_THRESHOLD:
                    # Too far from left wall: steer left towards wall (slow left, fast right)
                    left_motor.set_dps(-150)
                    right_motor.set_dps(-100)
                
                if distance >= 20.0 and distance <= 255.0:
                    td = us_sensor.get_cm()
                    while(td <= 230):
                        left_motor.set_dps(-90)
                        right_motor.set_dps(90)
                        time.sleep(0.01)
                        td = us_sensor.get_cm()
                else:
                    # Within the band width: drive straight
                    left_motor.set_dps(BASE_SPEED)
                    right_motor.set_dps(BASE_SPEED)
            
                
            time.sleep(0.1)
            
    except BaseException:
        reset_brick()
        exit()
        
    reset_brick()
    