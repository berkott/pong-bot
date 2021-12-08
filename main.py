import RPi.GPIO as GPIO
import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

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

# === Flywheel Init ===

# === Servo Init ===

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

def update_display(shooter_angle, flywheel_speed):
    # Draw a white background
    draw.rectangle((BORDER // 2, BORDER // 2, oled.width - BORDER // 2 - 1, oled.height - BORDER // 2 - 1), outline=0, fill=0)

    font = ImageFont.load_default()

    text = f"Shooter Angle: {int(shooter_angle)}"
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height - 2),
        text,
        font=font,
        fill=255,
    )

    text = f"Flywheel Speed: {int(flywheel_speed)}"
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


draw_menu()

while True:
    shoot_button_pressed = GPIO.input(SHOOT_BUTTON) == GPIO.HIGH
    shooter_angle = 7
    flywheel_speed = 8
    button_pressed = False

    # Menu State
    if not game_start:
        if shoot_button_pressed:
            game_start = True
    # Game State
    else:
        if shoot_button_pressed:
            # Change motor stuff


            update_display(shooter_angle, flywheel_speed)

    
    #print(shoot_button)
    #time.sleep(0.25)


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
