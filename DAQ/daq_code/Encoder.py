#!/home/hydro/Documents/Senior-Design/DAQ/bin/python3
from gpiozero import Button
from signal import pause

# Define the GPIO pin you want to monitor
gpio_pin = 17

# Create a Button object for the GPIO pin
button = Button(gpio_pin, pull_up=False)  # If pull_up=True, use pull-up resistor

# Initialize a counter variable
press_count = 0

# Define a callback function to be called when a rising edge is detected
def on_rising_edge():
    global press_count
    press_count += 1
    print("Rising edge detected! Press count:", press_count)

# Assign the callback function to the Button's when_pressed event
button.when_pressed = on_rising_edge

# Keep the program running to allow event detection
pause()
