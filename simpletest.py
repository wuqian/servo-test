#pressed Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
import select 
import sys
import pygame
from pygame.locals import *

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

x_current = 300
y_current = 400
step = 50

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def servo_move(channel, direction, current, offset, min_limit, max_limit):
    offset = direction * offset
    current += offset
    current = min_limit if current < min_limit else current
    current = max_limit if current > max_limit else current
    pwm.set_pwm(channel, 0, current)
    time.sleep(0.1)
    return current


# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

pygame.init()
screen = pygame.display.set_mode((640,480))

pwm.set_pwm(1, 0, y_current)
pwm.set_pwm(0, 0, x_current)

print('Moving servo on channel 0, press Ctrl-C to quit...')

while True:
    for event in  pygame.event.get():
        print event
        if (event.type == KEYDOWN):
            if (event.key == K_UP):
                y_current = servo_move(1, -1, y_current, step, servo_min, servo_max)
            if (event.key == K_DOWN):
                y_current = servo_move(1, 1, y_current, step, servo_min, servo_max)
            if (event.key == K_LEFT):
                x_current = servo_move(0, -1, x_current, step, servo_min, servo_max)
            if (event.key == K_RIGHT):
                x_current = servo_move(0, 1, x_current, step, servo_min, servo_max)
