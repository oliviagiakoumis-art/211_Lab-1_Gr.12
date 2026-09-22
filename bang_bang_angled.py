from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3ultrasonicsensor

# Initialize sensors and motors (Update ports if necessary)
us_sensor = EV3ultrasonicsensor()
left_motor = Motor("A")
right_motor = Motor("D")

# Lab 1 Bang-Bang Parameters
BAND_CENTER = 20    # Target distance in cm
BAND_WIDTH = 3      # Acceptable tolerance in cm[cite: 1]
BASE_SPEED = 200    # Nominal driving speed (Degrees Per Second)

LOWER_THRESHOLD = BAND_CENTER - BAND_WIDTH  # 17 cm
UPPER_THRESHOLD = BAND_CENTER + BAND_WIDTH  # 23 cm
GAP_THRESHOLD = 45.0                        # Distance threshold to detect a wall gap

if __name__ == "__main__":
    wait_ready_sensors()
    
    try:
        print("Running Bang-Bang Controller with Corner Handling (Wall on Left)...")
        while True:
            distance = us_sensor.get_cm()
            
            if distance is not None:
                print(f"Distance: {distance} cm")
                
                # --- CONCAVE CORNER / BAD SENSOR RANGE (50 to 255 cm) ---
                if distance >= 50.0 and distance <= 255.0:
                    print("Concave corner detected: Executing timed pivot turn...")
                    t1 = time.time()
                    d = 0
                    while d <= 2.65999999999999873:
                        d += 0.01
                        left_motor.set_dps(90)
                        right_motor.set_dps(-90)
                        time.sleep(0.01)
                        print(f"{time.time()}")
                    t2 = time.time()
                
                # --- GAP CHECK ---
                elif distance > GAP_THRESHOLD:
                    # Drive straight through the gap instead of reacting to a false "too far" state
                    left_motor.set_dps(BASE_SPEED)
                    right_motor.set_dps(BASE_SPEED)
                elif distance < LOWER_THRESHOLD:
                    # Too close to left wall: steer right away from wall (fast left, slow right)
                    left_motor.set_dps(120)
                    right_motor.set_dps(100)
                elif distance > UPPER_THRESHOLD:
                    # Too far from left wall: steer left towards wall (slow left, fast right)
                    left_motor.set_dps(120)
                    right_motor.set_dps(250)
                else:
                    # Within the band width: drive straight[cite: 1]
                    left_motor.set_dps(BASE_SPEED)
                    right_motor.set_dps(BASE_SPEED)
                
                left_motor.start()
                right_motor.start()
                
            time.sleep(0.05)
            
    except BaseException:
        reset_brick()
        exit()