#adding to github- steps:
'''
go into terminal:

"cd "C:\Users\ogana\Downloads\211\lab 1"
git init

git add .py

git add file2.py
git commit -m "Initial commit"

git branch -M main
git remote add origin https://github.com/your-username/your-repo-name.git

git push -u origin main --> for the first time only,,after that : git push


--> for me: git remote add origin https://github.com/oliviagiakoumis-art/211-Lab-1.git

'''




from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3ultrasonicsensor

# Initialize sensors and motors
us_sensor = EV3ultrasonicsensor()
left_motor = Motor("A")
right_motor = Motor("D")

# Lab 1 P-Type Parameters
BAND_CENTER = 20    # Target distance in cm
BASE_SPEED = 200    # Nominal driving speed (DPS)
KP = 4.0            # Proportional gain constant (tune in lab)--> Kp too high-->tuirns too fast
MAX_CORRECTION = 150 # Saturation cap to prevent motor strain

if __name__ == "__main__":
    wait_ready_sensors()
    
    try:
        print("Running P-Type Controller (Wall on Left)...")
        while True:
            distance = us_sensor.get_cm()
            
            if distance is not None:
                print(f"Distance: {distance} cm")
                
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
                
                left_motor.start()
                right_motor.start()
                
            time.sleep(0.05)
            
    except BaseException:
        reset_brick()
        exit()