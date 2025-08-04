import pyautogui as pg
from pynput import mouse
import math
import time

allowed = True
def unitsign(number,multiplyby = 1):
    if number != 0:
        num = number/(number**2)**(1/2) * multiplyby
    else:
        num = 0
    return num
def allow():
    allow.allowed = True
def on_move(x, y):
    # print("Touchpad touched")
    allow.allowed = False


def on_scroll(x, y, dx, dy):
    # print("Touchpad scrolled")
    allow.allowed = False
allow()
pg.FAILSAFE = False
listener = mouse.Listener(on_move=on_move, on_scroll=on_scroll)
listener.start()
prev = pg.position()
velx,vely = (0,0)
count = 0
maxi = 10
# listener.join()
while True:
    count += 1
    new = pg.position()
    if new[0] <= 0 or new[0] >= 1365:
        velx = -velx
    if new[1] <= 0 or new[1] >= 767:
        vely = -vely
    if allow.allowed == True:
        pg.moveTo(x = new[0] + velx,y = new[1] + vely)
        # print('Not being pressed')
    else:
        # print('pressed')
        velx = new[0] - prev[0]
        vely = new[1] - prev[1]
        prev = new
        allow.allowed = True
    time.sleep(0.08)