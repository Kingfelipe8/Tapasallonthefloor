
#!/usr/bin/env python3
from ST7789 import ST7789, BG_SPI_CS_FRONT
from PIL import Image, ImageDraw, ImageFont
from displayhatmini import DisplayHATMini
import random
import pygame
import time
import sys
import math

#get py game going
pygame.init()


#Define how text works
def text(draw, text, position, size, color):
    fnt = ImageFont.load_default()
    draw.text(position, text, font=fnt, fill=color)

# Plumbing to convert Display HAT Mini button presses into pygame events
def button_callback(pin):
    key = {
        display_hat.BUTTON_A: 'a',
        display_hat.BUTTON_B: 'b',
        display_hat.BUTTON_X: 'x',
        display_hat.BUTTON_Y: 'y'
    }[pin]
    event = pygame.KEYDOWN if display_hat.read_button(pin) else pygame.KEYUP
    pygame.event.post(pygame.event.Event(event, unicode=key, key=pygame.key.key_code(key)))

# Always have an escape plan

def handle_quit():
	pygame.quit()
	quit()

#pick a colour any color
colours = ["Green", "Blue", "Red", "Yellow"]

# Buttons
BUTTON_A = 5
BUTTON_B = 6
BUTTON_X = 16
BUTTON_Y = 24

# Onboard RGB LED
LED_R = 17
LED_G = 27
LED_B = 22

# General
SPI_PORT = 0
SPI_CS = 1
SPI_DC = 9
BACKLIGHT = 13

# Screen dimensions
WIDTH = 320
HEIGHT = 240

#initial player score
player_score = 0

#target score
target_score = 25

#player lives
lives = 2

#Display
display = ST7789(
    port=SPI_PORT,
    cs=SPI_CS,
    dc=SPI_DC,
    backlight=BACKLIGHT,
    width=WIDTH,
    height=HEIGHT,
    rotation=180,
    spi_speed_hz=60 * 1000 * 1000
)

#How long people have to react
reaction = 1
pacer = 1  #set this less than 1 to make it get progressively quicker



buffer = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(buffer)

#black background
draw.rectangle((0,0,240,320),(0,0,0))

#the colours by buttons
draw.rectangle((0, 0, 50, 50), (255, 0, 0))
draw.rectangle((320-50, 0, 320, 50), (0, 255, 0))
draw.rectangle((0, 240-50, 50, 240), (0, 0, 255))
draw.rectangle((320-50, 240-50, 320, 240), (255, 255, 0))

#circle in the middle
draw.ellipse((160-80, 120-80, 160+80, 120+80), (120,120,120))
display.display(buffer)
time.sleep(0.5)

#Define circle colours
'''draw.ellipse((160-80, 120-80, 160+80, 120+80), (0,0,120))
display.display(buffer)
time.sleep(0.5)
draw.ellipse((160-80, 120-80, 160+80, 120+80), (120,0,0))
display.display(buffer)
time.sleep(0.5)
draw.ellipse((160-80, 120-80, 160+80, 120+80), (0,120,0))
display.display(buffer)
time.sleep(0.5)
draw.ellipse((160-80, 120-80, 160+80, 120+80), (120,120,120))'''

#something about my dispaly, dunno why this is important but it is???
display_hat = DisplayHATMini(None)

screen = pygame.Surface((display_hat.WIDTH, display_hat.HEIGHT))
display_hat.on_button_pressed(button_callback)
'''
if DisplayHATMini.read_button(DisplayHATMini.BUTTON_X):
	player_score += 1
'''
print(player_score)

live_game = True

while live_game:
	
	circle = random.choice(colours)
	if circle == "Blue":
			draw.ellipse((160-80, 120-80, 160+80, 120+80), (0,0,255))
			display.display(buffer)
			print(circle)
			time.sleep(reaction)
			reaction = pacer*reaction
	if circle == "Red":
			draw.ellipse((160-80, 120-80, 160+80, 120+80), (255,0,0))
			display.display(buffer)
			print(circle)
			time.sleep(reaction)
			reaction = pacer*reaction
	if circle == "Yellow":
			draw.ellipse((160-80, 120-80, 160+80, 120+80), (255,255,0))
			display.display(buffer)
			print(circle)
			time.sleep(reaction)
			reaction = pacer*reaction
	if circle == "Green":
			draw.ellipse((160-80, 120-80, 160+80, 120+80), (0,255,0))
			display.display(buffer)
			print(circle)
			time.sleep(reaction)
			reaction = pacer*reaction

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_b:
				if circle == "Blue":
					player_score += 1
				else:
					lives -= 1 
				print(player_score)
				print("lives remaining:" + str(lives))
			if event.key == pygame.K_a:
				if circle == "Red":
					player_score += 1
				else:
					lives -= 1 
				print(player_score)
				print("lives remaining:" + str(lives))
			if event.key == pygame.K_x:
				if circle == "Green":
					player_score += 1
				else:
					lives -= 1 
				print(player_score)
				print("lives remaining:" + str(lives))
			if event.key == pygame.K_y:
				if circle == "Yellow":
					player_score += 1
				else:
					lives -= 1 
				print(player_score)
				print("lives remaining:" + str(lives))

				#endgame with celebration lights
			if (player_score > target_score):
				draw.ellipse((160-80, 120-80, 160+80, 120+80), (0,0,0))
				text(draw,"You win! Your score was: " + str(player_score), (100, 10),50,(255,255,255))
				display_hat.set_led(0.05, 0.00, 0.00)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.05, 0.00)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.00, 0.05)
				time.sleep(0.3)
				display_hat.set_led(0.05, 0.00, 0.00)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.05, 0.00)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.00, 0.05)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.00, 0.00)
				live_game = False
			if (lives < 1):
				draw.ellipse((160-80, 120-80, 160+80, 120+80), (0,0,0))
				text(draw,"You lose, call an ambulance", (40, 80),100,(255,255,255))
				text(draw,"Your score was: " + str(player_score), (40, 100),50,(255,255,255))
				display.display(buffer)
				display_hat.set_led(0.05, 0.00, 0.00)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.00, 0.05)
				time.sleep(0.3)
				display_hat.set_led(0.05, 0.00, 0.00)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.00, 0.05)
				time.sleep(0.3)
				display_hat.set_led(0.05, 0.00, 0.00)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.00, 0.05)
				time.sleep(0.3)
				display_hat.set_led(0.05, 0.00, 0.00)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.00, 0.05)
				time.sleep(0.3)
				display_hat.set_led(0.00, 0.00, 0.00)
				live_game = False
				
			
pygame.quit()






while True:
    display.display(buffer)
    time.sleep(1.0 / 60)



				#draw = ImageDraw.Draw(buffer)
