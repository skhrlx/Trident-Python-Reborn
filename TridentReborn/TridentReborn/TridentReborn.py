from time import sleep
from os import system
from hashlib import sha256
import random
import serial
from win32 import win32api
import cv2
import numpy as np
import threading
import dxcam
import serial
import configparser
import math
import subprocess
import pyautogui
from PIL import Image

class TriggerBot:
    def __init__(self):
    
        self.monitor_width = S_HEIGHT
        self.monitor_height = S_WIDTH

        self.left = int((self.monitor_width / 2) - (FOV / 2))
        self.top = int((self.monitor_height / 2) - (FOV / 2))
        self.width = FOV
        self.height = FOV

        self.center = FOV / 2
        
        print("Triggerbot Ready!")

    def find_dimensions(self, box_size): 
        self.box_size = box_size
        self.box_middle = int(self.box_size / 2)
        self.y = int(((GetSystemMetrics(1)   / 2) - (self.box_size / 2))) 
        self.x = int(((GetSystemMetrics(0) / 2) - (self.box_size / 2))) 

    def process_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        processed = cv2.inRange(hsv, lower, upper)

        processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, np.ones((10, 10), np.uint8))
        dilatation_size = 15
        dilation_shape = cv2.MORPH_RECT
        dilation_shape = cv2.MORPH_ELLIPSE
        dilation_shape = cv2.MORPH_CROSS
        element = cv2.getStructuringElement(dilation_shape, (2 * dilatation_size + 1, 2 * dilatation_size + 1),
                                    (dilatation_size, dilatation_size))
        processed = cv2.dilate(processed, element)
        processed = cv2.blur(processed, (8, 8))        
        return processed

    def detect_contours(self, frame, minimum_size):
        contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large_contours = []
        if len(contours) != 0:
            for i in contours:
                if (cv2.contourArea(i), minimum_size):
                   if cv2.contourArea(i) > minimum_size:
                       large_contours.append(i)
        return large_contours

    def scale_contour(self,cnt, scale:float):
        M = cv2.moments(cnt)
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])

        center = cnt - [x, y]
        cnt_scaled = center * scale
        cnt_scaled = cnt_scaled + [x, y]
        cnt_scaled = cnt_scaled.astype(np.int32)

        return cnt_scaled
    
    def on_target(self, contour, HITBOX):
        for c in contour:
            cont = self.scale_contour(c, HITBOX)
            test = cv2.pointPolygonTest(cont,( self.center, self.center),False)
            if test >= 0:
                return True
        return False
    
    def can_shoot(self):
        contours = trigger.detect_contours(trigger.process_frame(np.array(camera.Frame())), 100)
        if contours and trigger.on_target(contours, HITBOX):
            return pax(5)

    def on_target_silent(self, contour):
        for c in contour:
            cont = self.scale_contour(c, 1)
            test = cv2.pointPolygonTest(cont,( self.center, self.center),False)
            if test >= 0:
                return True
        return False
        
    def can_shoot_silent(self):
        contours = trigger.detect_contours(trigger.process_frame(np.array(camera.Frame())), 50)
        if contours and trigger.on_target_silent(contours):
            return pax(5)


config = configparser.ConfigParser()
config.read('settings.cfg')

key_pressed = False

S_HEIGHT = config.getint('Screen Resolution', 'S_HEIGHT', fallback=1280)
S_WIDTH = config.getint('Screen Resolution', 'S_WIDTH', fallback=1024)
BHOP = config.getboolean('Features', 'BHOP', fallback=False)
RCS = config.getboolean('Features', 'RCS', fallback=False)
RCS_AIM = config.getboolean('Features', 'RCS_AIM', fallback=True)
TRIGGERBOT = config.getboolean('Features', 'TRIGGERBOT', fallback=True)
MINECRAFT = config.getboolean('Features', 'MINECRAFT', fallback=False)
AIMBOT = config.getboolean('Features', 'AIMBOT', fallback=True)
FORTNITE = config.getboolean('Features', 'FORTNITE', fallback=False)
FLICK_AIM = config.getboolean('Features', 'FLICK_AIM', fallback=False)
FOV = config.getint('Settings', 'FOV', fallback=35)
COLOR = config.get('Settings', 'COLOR', fallback='purple')
HITBOX = config.getfloat('Settings', 'HITBOX', fallback=0.2)

if COLOR == "purple":
    lower = np.array([139, 95, 154], np.uint8)
    upper = np.array([153, 255, 255], np.uint8)
elif COLOR == "yellow":
    lower = np.array([30, 125, 150], np.uint8)
    upper = np.array([30, 255, 255], np.uint8)
elif COLOR == "apex":
    lower = np.array([139, 95, 154], np.uint8)
    upper = np.array([153, 255, 255], np.uint8)
else:
    lower = np.array([139, 95, 154], np.uint8)
    upper = np.array([153, 255, 255], np.uint8)

if not config.has_section('Settings'):
    config.add_section('Settings')
    config.set('Settings', 'FOV', str(FOV))
    config.set('Settings', 'COLOR', str(COLOR))
    config.set('Settings', 'HITBOX', str(HITBOX))
    
    with open('settings.cfg', 'w') as config_file:
        config.write(config_file)
        
if not config.has_section('Features'):
    config.add_section('Features')
    config.set('Features', 'BHOP', str(False))
    config.set('Features', 'RCS', str(False))
    config.set('Features', 'RCS_AIM', str(True))
    config.set('Features', 'TRIGGERBOT', str(True))
    config.set('Features', 'MINECRAFT', str(False))
    config.set('Features', 'AIMBOT', str(True))
    config.set('Features', 'FORTNITE', str(False))
    config.set('Features', 'FLICK_AIM', str(False))

    with open('settings.cfg', 'w') as config_file:
        config.write(config_file)

if not config.has_section('Screen Resolution'):
    config.add_section('Screen Resolution')
    config.set('Screen Resolution', 'S_HEIGHT', str(768))
    config.set('Screen Resolution', 'S_WIDTH', str(1024))
    
    with open('settings.cfg', 'w') as config_file:
        config.write(config_file)

class FortniteBot:

    def __init__(self):
        self.key_pressed = False
        print("FortniteBot Ready !")

    def editmcr(self):
        if not self.key_pressed:
            self.key_pressed = True
            return sleep(0.009), pax(4)
        else:
            if self.key_pressed:
                self.key_pressed = False
                return pax(5)

class Camera():

    def __init__(self):

        self.monitor_width = S_HEIGHT
        self.monitor_height = S_WIDTH

        self.left = int((self.monitor_width / 2) - (FOV / 2))
        self.top = int((self.monitor_height / 2) - (FOV / 2))
        self.width = FOV
        self.height = FOV

        self.center = FOV / 2
        region = (self.left, self.top, self.left + self.width, self.top + self.height)
        center = FOV / 2
        self.camera = dxcam.create(region=region, output_color="BGR")
        self.camera.start(target_fps=240, video_mode=False)

        print("Camera Ready !")

    def Frame(self):
        image = self.camera.get_latest_frame()
        return image

    def sFrame(self):
        image = self.camera.grab()
        return image

arduino = serial.Serial('COM6', 128000)

def Send_Command(command): 
    return arduino.write(command)

def mousemove(x, y, z):

    if x < 0:
        x = x + 256
    if y < 0:
        y = y + 256

    pax = [int(2), int(x), int(y), int(z)]  # z value is the scroll value
    arduino.write(pax)  # send it to Arduino to move the mouse

def pax(pax):
    value = [int(pax)]
    return arduino.write(value)

class AimBot:
    def __init__(self):

        self.monitor_width = S_HEIGHT
        self.monitor_height = S_WIDTH
        
        self.left = int((self.monitor_width / 2) - (FOV / 2))
        self.top = int((self.monitor_height / 2) - (FOV / 2))
        self.width = FOV
        self.height = FOV
        trigger = TriggerBot()
        self.center = FOV / 2

        print("AimBot Ready !")

    def run(self, image, x_speed, y_speed):
        self.xspd = x_speed
        self.yspd = y_speed
        img = np.array(image)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            M = cv2.moments(thresh)
            point_to_aim = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            closestX = point_to_aim[0] + 5.2
            closestY = point_to_aim[1] - 6.2

            diff_x = int(closestX - self.center)
            diff_y = int(closestY - self.center)

            target_x = diff_x * self.xspd
            target_y = diff_y * self.yspd 

            mousemove(target_x, target_y, 0)
            
    def run_silent(self, image, x_speed, y_speed):
        self.xspd = x_speed
        self.yspd = y_speed
        img = np.array(image)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            M = cv2.moments(thresh)
            point_to_aim = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            closestX = point_to_aim[0] + 1.0 #+ 1.0
            closestY = point_to_aim[1] - 8.1 #- 8.1

            diff_x = int(closestX - self.center)
            diff_y = int(closestY - self.center)

            target_x = diff_x * self.xspd
            target_y = diff_y * self.yspd 

            mousemove(target_x, target_y, 0)
            #trigger.can_shoot_silent()
            pax(5)
            mousemove(-target_x, -target_y, 0), sleep(0.10)
            

class MinecraftBot:

    def __init__(self):
        print("MinecraftBot Ready!")
        self.shake_left = [-2, -1, 0, 1, 2]
        self.shake_right = [-2, -1, 0, 1, 2]
        self.shake_right = [0]
        self.left_sleep = random.uniform(0.05, 0.09)
        #self.right_sleep = random.uniform(0.06, 0.08) #legit one
        self.right_sleep = random.uniform(0.008, 0.01) #rage one

    def left_ac(self):
        pax(5),mousemove(random.choice(self.shake_left), random.choice(self.shake_left), 0) , sleep(self.left_sleep)

    def right_ac(self):
        pax(6),mousemove(random.choice(self.shake_right), random.choice(self.shake_right), 0) , sleep(self.right_sleep)

if __name__ == "__main__":
    _hash = sha256(f'{random.random()}'.encode('utf-8')).hexdigest()
    print(_hash), system(f'title {_hash}'), sleep(0.5), system('@echo off'), system('cls')

    if AIMBOT:
        aim = AimBot()
    if AIMBOT or TRIGGERBOT:
        camera = Camera()
    if TRIGGERBOT:
        trigger = TriggerBot()
    if FORTNITE:
        fortnite = FortniteBot()
    if MINECRAFT:
        minecraft = MinecraftBot()

    print("Everything started correctly Ready !"), sleep(1), system("cls")

    while True:
        aim.run(camera.Frame(), 0.3, 0.1)
        if (win32api.GetAsyncKeyState(0x01) and RCS_AIM):
            aim.run(camera.Frame(), 0.1, 0.1), mousemove(0, +2, 0), sleep(0.0030)

        if (win32api.GetAsyncKeyState(0x01) and RCS):
            mousemove2(0, +1, 0), sleep(0.0030)

        if (win32api.GetAsyncKeyState(0x4C) and FLICK_AIM):
            aim.run_silent(camera.Frame(), 4.3, 4.3) #4.3

        #if (win32api.GetAsyncKeyState(0x4C) and AIMBOT):
            #aim.run(camera.Frame(), 1, 0.6)

        if (win32api.GetAsyncKeyState(0x50) and TRIGGERBOT):
            trigger.can_shoot()

        if (win32api.GetAsyncKeyState(0x20) and BHOP):
            pax(1), sleep(0.03)

        if (win32api.GetAsyncKeyState(0x4C) and MINECRAFT):
            minecraft.left_ac()

        if (win32api.GetAsyncKeyState(0x50) and MINECRAFT):
            minecraft.right_ac()

        if win32api.GetAsyncKeyState(0x45) and FORTNITE:
            if not key_pressed:
                sleep(0.005)#sleep(0.005)
                pax(3)
                key_pressed = True
        else:
            if key_pressed:
                pax(4)
                key_pressed = False

        sleep(0.0000001)
