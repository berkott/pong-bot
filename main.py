import RPi.GPIO as GPIO
import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from gpiozero import AngularServo

# === Display Init ===
BORDER = 5
oled_reset = digitalio.DigitalInOut(board.D1)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3d, reset = oled_reset) # Change addr if needed

# Clear display.
oled.fill(1)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# === Shoot Button Init ===
SHOOT_BUTTON = 15

GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD) # Physical pin numbering

GPIO.setup(SHOOT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# === Joystick Init ===
RIGHT_SWITCH = 27
LEFT_SWITCH = 17
UP_SWITCH = 22
DOWN_SWITCH = 10

GPIO.setup(RIGHT_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LEFT_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(UP_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DOWN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# === Flywheel Init ===
MAX_RPM = 400

I1_PIN = 16
I2_PIN = 20
EN_PIN = 21

GPIO.setup(I1_PIN, GPIO.OUT)
GPIO.setup(I2_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)
GPIO.output(I1_PIN, GPIO.LOW)
GPIO.output(I2_PIN, GPIO.LOW)

pwm = GPIO.PWM(EN_PIN, 100)
pwm.start(25)

# === Servo Init ===
SERVO_SIGNAL_PIN = 12
MAX_ANGLE = 20

GPIO.setup(SERVO_SIGNAL_PIN, GPIO.OUT, initial=False)
pwm_servo = GPIO.PWM(SERVO_SIGNAL_PIN, 50)
pwm_servo.start(0)
# servo = AngularServo(SERVO_SIGNAL_PIN, min_angle=-MAX_ANGLE, max_angle=MAX_ANGLE) # Change min and max angle here
# servo.angle = 0

# === Game Init ===
game_start = False

# === Main Flow ===
def draw_menu():
    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    # Draw a smaller inner rectangle
    draw.rectangle(
        (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
        outline=0,
        fill=0,
    )

    font = ImageFont.load_default()

    text = "Welcome to Pong!"
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height - 2),
        text,
        font=font,
        fill=255,
    )

    text = "Press Button"
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 + 2),
        text,
        font=font,
        fill=255,
    )

    # Display image
    oled.image(image)
    oled.show()

def update_display(shooter_angle, flywheel_speed, extra_text):
    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    draw.rectangle((BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1), outline = 0, fill = 0)

    font = ImageFont.load_default()

    text = f"Shooter Angle: {int(shooter_angle)}"
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - (font_height // 2) * 3),
        text,
        font=font,
        fill=255,
    )

    text = f"Flywheel RPM: {int(flywheel_speed)}"
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )

    text = extra_text
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 + (font_height // 2) * 3),
        text,
        font=font,
        fill=255,
    )

    # Display image
    oled.image(image)
    oled.show()


draw_menu()
shooter_angle = 0
flywheel_speed = 0

while True:
    shoot_button_pressed = GPIO.input(SHOOT_BUTTON) == GPIO.HIGH

    right_switch = GPIO.input(RIGHT_SWITCH) == GPIO.HIGH
    left_switch = GPIO.input(LEFT_SWITCH) == GPIO.HIGH
    up_switch = GPIO.input(UP_SWITCH) == GPIO.HIGH
    down_switch = GPIO.input(DOWN_SWITCH) == GPIO.HIGH

    # Menu State
    if not game_start:
        if shoot_button_pressed:
            game_start = True
            update_display(shooter_angle, flywheel_speed, "Press to Shoot")
            time.sleep(2)

    # Game State
    else:
        if right_switch or left_switch or up_switch or down_switch:
            flywheel_speed += 10 if up_switch and flywheel_speed < MAX_RPM else 0
            flywheel_speed -= 10 if down_switch and flywheel_speed > 0 else 0
            shooter_angle += 1 if right_switch and shooter_angle < MAX_ANGLE else 0
            shooter_angle -= 1 if left_switch and shooter_angle > -MAX_ANGLE else 0

            pwm_servo.ChangeDutyCycle(7.5 + (shooter_angle/10))

            # servo.angle = shooter_angle * 100
            # if right_switch:
                # pwm_servo.ChangeDutyCycle(8.5)
            # elif left_switch:
                # pwm_servo.ChangeDutyCycle(6.5)
            # else:
                # pwm_servo.ChangeDutyCycle(0)

            update_display(shooter_angle, flywheel_speed, "Press to Shoot")

        if shoot_button_pressed:
            # Set Flywheel Speed
            # Maybe change the ones below to I2_PIN depending on desired turn direction
            GPIO.output(I1_PIN, GPIO.HIGH)
            pwm.ChangeDutyCycle((flywheel_speed / MAX_RPM) * 100) # within the range [0, 100]

            # for i in range(100):
                # pwm.ChangeDutyCycle(i) # within the range [0, 100]
                # time.sleep(0.2)

            for i in range(3):
                update_display(shooter_angle, flywheel_speed, f"Drop in {3 - i}")
                time.sleep(1)

            for i in range(2):
                update_display(shooter_angle, flywheel_speed, f"DROP NOW! {2 - i}")
                time.sleep(1)

            # Zero Flywheel Speed
            GPIO.output(I1_PIN, GPIO.LOW)

            for i in range(2):
                update_display(shooter_angle, flywheel_speed, f"Resetting {2 - i}")
                time.sleep(1)

            update_display(shooter_angle, flywheel_speed, "Press to Shoot")


# import RPi.GPIO as GPIO
# import time

# # Maybe look at putting sensor reading code in another file

# # Fix pin numbers!
# LEFT_RIGHT_POT_A = 12
# LEFT_RIGHT_POT_B = 16
# UP_DOWN_POT_A = 18
# UP_DOWN_POT_B = 22

# SHOOT_BUTTON = 10

# GPIO.setwarnings(False)
# # Determine optimal mode:
# # GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# # Shooting Button
# GPIO.setup(SHOOT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

# # Joystick
# def discharge(pin_a, pin_b):
#     GPIO.setup(pin_a, GPIO.IN)
#     GPIO.setup(pin_b, GPIO.OUT)
#     GPIO.output(pin_b, False)
#     time.sleep(0.2)

# def charge_time(pin_a, pin_b):
#     GPIO.setup(pin_b, GPIO.IN)
#     GPIO.setup(pin_a, GPIO.OUT)
#     count = 0
#     GPIO.output(pin_a, True)
#     while not GPIO.input(pin_b):
#         count += 1
#     return count

# def analog_read(pin_a, pin_b):
#     discharge(pin_a, pin_b)
#     return charge_time(pin_a, pin_b)

# # Main loop
# while True:
#     #left_right_pot_value = analog_read(LEFT_RIGHT_POT_A, LEFT_RIGHT_POT_B)
#     #print(left_right_pot_value)
#     up_down_pot_value = analog_read(UP_DOWN_POT_A, UP_DOWN_POT_B)
#     print(up_down_pot_value)
#     #shoot_button = GPIO.input(SHOOT_BUTTON) == GPIO.HIGH
#     #print(shoot_button)
#     #time.sleep(0.25)
