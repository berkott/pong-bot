import RPi.GPIO as GPIO
import time

# Maybe look at putting sensor reading code in another file

# Fix pin numbers!
LEFT_RIGHT_POT_A = 18
LEFT_RIGHT_POT_B = 18
UP_DOWN_POT_A = 18
UP_DOWN_POT_B = 18

SHOOT_BUTTON = 10

GPIO.setwarnings(False)
# Determine optimal mode:
# GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# Shooting Button
GPIO.setup(shoot_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

# Joystick
def discharge(pin_a, pin_b):
    GPIO.setup(pin_a, GPIO.IN)
    GPIO.setup(pin_b, GPIO.OUT)
    GPIO.output(pin_b, False)
    time.sleep(0.004)

def charge_time(pin_a, pin_b):
    GPIO.setup(pin_b, GPIO.IN)
    GPIO.setup(pin_a, GPIO.OUT)
    count = 0
    GPIO.output(pin-a, True)
    while not GPIO.input(pin_b):
        count = count + 1
    return count

def analog_read(pin_a, pin_b):
    discharge(pin_a, pin_b)
    return charge_time(pin_a, pin_b)

# Main loop
while True:
    left_right_pot_value = analog_read(LEFT_RIGHT_POT_A, LEFT_RIGHT_POT_B)
    up_down_pot_value = analog_read(UP_DOWN_POT_A, UP_DOWN_POT_B)

    shoot_button = GPIO.input(SHOOT_BUTTON) == GPIO.HIGH

    time.sleep(1)