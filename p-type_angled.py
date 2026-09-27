from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3ultrasonicsensor

# Initialize sensors and motors
us_sensor = EV3ultrasonicsensor()
left_motor = Motor("A")
right_motor = Motor("D")

# Lab 1 P-Type Parameters
BAND_CENTER = 20     # Target distance in cm
BASE_SPEED = 200     # Nominal driving speed (DPS)
KP = 4.0             # Proportional gain constant (tune in lab)
MAX_CORRECTION = 150 # Saturation cap to prevent motor strain
GAP_THRESHOLD = 38   # Distance threshold to detect gaps (> max wall distance)

# Safety tracking variable for angled sensor glitches
last_valid_distance = BAND_CENTER  

if __name__ == "__main__":
    wait_ready_sensors()
    
    try:
        print("Running P-Type Controller (Wall on Left) with Angled Sensor Filtering...")
        while True:
            raw_distance = us_sensor.get_cm()
            
            # --- ANGLING & ERROR FILTERING LAYER ---
            # If the sensor returns None or an impossible minimum range, 
            # fall back to the last known good distance to prevent crashes/jerking.
            if raw_distance is None or raw_distance < 3.0:
                distance = last_valid_distance
                print(f"Sensor glitch detected (Raw: {raw_distance}). Using fallback: {distance} cm")
            else:
                distance = raw_distance
                last_valid_distance = distance  # Update our safe fallback memory
            # --------------------------------------
            
            # 1. Gap Handling Check
            if distance > GAP_THRESHOLD:
                # Treat as a gap: hold steady course straight across the opening
                left_motor.set_dps(BASE_SPEED)
                right_motor.set_dps(BASE_SPEED)
                print(f"Gap detected! Distance: {distance} cm - Driving straight.")
            else:
                # Normal P-type control logic
                error = distance - BAND_CENTER
                correction = int(KP * abs(error))
                
                if correction > MAX_CORRECTION:
                    correction = MAX_CORRECTION

                if error > 0:
                    # Too far from left wall: steer left smoothly towards wall
                    left_motor.set_dps(max(50, BASE_SPEED - correction))
                    right_motor.set_dps(BASE_SPEED + correction)
                else:
                    # Too close to left wall: steer right smoothly away from wall
                    left_motor.set_dps(BASE_SPEED + correction)
                    right_motor.set_dps(max(50, BASE_SPEED - correction))
            
            # Start motion
            left_motor.start()
            right_motor.start()
                
            time.sleep(0.05)
            
    except BaseException:
        reset_brick()
        exit()