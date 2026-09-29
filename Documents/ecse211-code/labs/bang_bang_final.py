from utils.brick import reset_brick, wait_ready_sensors, Motor, time, EV3UltrasonicSensor
import time

leftmotor = Motor("C")
rightmotor = Motor("A")

us_sensor = EV3UltrasonicSensor(1)

BAND_WIDTH = 7.5             # TODO: Eventually use these constants in our code
BAND_CENTER = 27.5

# Number of consecutive 255 ( currently actually using > 80 ) readings required before
# we consider the wall to actually be missing
NO_WALL_LIMIT = 5


def rotate(t):
    initial = rightmotor.get_encoder()

    while True:
        current = rightmotor.get_encoder()
        delta = ((current - initial + 2**31) % 2**32) - 2**31

        if (t > 0 and delta >= t) or (t < 0 and delta <= t):
            break

        rightmotor.set_dps(t)
        leftmotor.set_dps(t/4)          # NOTE for testing: if need a sharper turn (more like a pivot), can increase the number we're dividing t by

        time.sleep(0.1)

        #rightmotor.set_dps(-140)       # NOTE: maybe put lines 32-35 back after more testing if needed, just keep in mind this will cause jerky action if the values don't connect nicely with lines 27-28
        #leftmotor.set_dps(-140)

        #time.sleep(0.1)

    #rightmotor.set_dps(0)              # NOTE: pretty sure lines 37-38 should stay removed, we found that this made the convex turns much smoother
    #leftmotor.set_dps(0)


if __name__ == "__main__":
    wait_ready_sensors()

    no_wall_count = 0

    try:
        while True:

            # Take one ultrasonic reading
            d = us_sensor.get_cm()

            print(f"distance: {d}")

            # -----------------------------------------
            # FILTER 255 ( actually > 80 ) / NO-WALL READINGS
            # -----------------------------------------
            if d > 80:                  # NOTE: after some testing, we decided that instead of only counting "255" readings as NO-WALL, we are requiring that readings > "80" should also trigger NO-WALL behaviour (did this to try to avoid taking left (convex) turns where there is a wall in front after completing the 90 degree turn too widely)
                no_wall_count += 1
            else:
                no_wall_count = 0

            # If 255 ( actually > 80 ) persists for long enough,
            # assume the wall has actually disappeared
            if no_wall_count >= NO_WALL_LIMIT:
                print("Wall missing - rotating")
                rotate(-150)            # NOTE for testing: adjust this value to control how much the robot rotates per rotate() call during left (convex) turns
                no_wall_count = 0

            # -----------------------------------------
            # NORMAL WALL-FOLLOWING CONTROL
            # -----------------------------------------
            elif d != 255:

                if d < 15:
                    # Move backwards / away from wall, then move forward a little bit
                    rightmotor.set_dps(220)
                    leftmotor.set_dps(100)
                    time.sleep(1.2)
                    rightmotor.set_dps(-100)    # NOTE for testing: could try really reducing this speed so that the robot makes a sharp pivot away from wall
                    leftmotor.set_dps(-150)
                    time.sleep(0.5)
                    leftmotor.set_dps(-100)
                    rightmotor.set_dps(-100)
                    time.sleep(0.2)

                elif d > 35:
                    # Too far from wall -> turn toward wall
                    rightmotor.set_dps(-220)
                    leftmotor.set_dps(-100)
                    time.sleep(0.3)

                elif d < 20:
                    # Too close to wall -> turn away from wall
                    leftmotor.set_dps(-220)
                    rightmotor.set_dps(-100)
                    time.sleep(1)

                else:
                    # Within desired band -> drive straight
                    leftmotor.set_dps(-250)
                    rightmotor.set_dps(-250)
                    time.sleep(0.1)

            # Small delay before the next sensor reading
            time.sleep(0.05)

    except BaseException:
        reset_brick()
        exit()

    reset_brick()