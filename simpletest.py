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
import RPi.GPIO as GPIO



# Import the PCA9685 module.
import Adafruit_PCA9685


GPIO.setmode(GPIO.BCM)
TRIG = 18
ECHO = 16
 
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.00001)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    start = time.time()

    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()
    distance = (stop - start) * 34000 / 2 #cm
    return distance


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

#init pygame
pygame.init()
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 100)
text = font.render("Hello, World", True, (0, 128, 0))

pwm.set_pwm(1, 0, y_current)
pwm.set_pwm(0, 0, x_current)

print('Moving servo on channel 0, press Ctrl-C to quit...')

last = time.time()
dis = get_distance()

try:
    while True:
        #handle keyboard event
        for event in  pygame.event.get():
            #print event
            if (event.type == KEYDOWN):
                if (event.key == K_UP):
                    y_current = servo_move(1, -1, y_current, step, servo_min, servo_max)
                if (event.key == K_DOWN):
                    y_current = servo_move(1, 1, y_current, step, servo_min, servo_max)
                if (event.key == K_LEFT):
                    x_current = servo_move(0, -1, x_current, step, servo_min, servo_max)
                if (event.key == K_RIGHT):
                    x_current = servo_move(0, 1, x_current, step, servo_min, servo_max)

        #update distance value
        if (time.time() - last > 0.2):
            dis = get_distance()
            last = time.time()
        text = font.render("{:.2f}cm".format(dis), True, (0, 128, 0))
        screen.fill((255, 255, 255))
        screen.blit(text,(320 - text.get_width() // 2, 240 - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

except KeyboardInterrupt:
    GPIO.cleanup()
