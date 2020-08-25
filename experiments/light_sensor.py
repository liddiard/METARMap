import RPi.GPIO as GPIO
import time

import constants


__author__ = 'Gus (Adapted from Adafruit)'
__license__ = "GPL"
__maintainer__ = "pimylifeup.com"

# define the pin that goes to the circuit
pin_to_circuit = constants.PHOTORESISTOR_PIN


def rc_time(pin_to_circuit):
    """Determine how long it takes for the capacitor to drain, an indirect
    measure of ambient light. We take this approach because the Raspberry Pi's
    GPIO pins are digital so they're either off or on. A lower value
    corresponds to more ambient light. More info about this approach:
    https://pimylifeup.com/raspberry-pi-light-sensor/
    """
    count = 0

    # Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        if count > constants.MIN_AMBIENT_LIGHT:
            return count
        count += 1

    return count


# i Catch when script is interupted, clean up correctly
def get_ambient_light():
    return rc_time(pin_to_circuit)
