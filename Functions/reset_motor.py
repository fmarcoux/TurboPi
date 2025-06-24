#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/TurboPi/')
import cv2
import time
import math
import signal
import Camera
import threading
import numpy as np
import yaml_handle
import HiwonderSDK.Board as Board
import HiwonderSDK.mecanum as mecanum
import HiwonderSDK.FourInfrared as infrared



if __name__ == "__main__":
	chassis = mecanum.MecanumChassis()
	chassis.set_velocity(0,0,0)
	Board.set_LED_color(0, 0, 0, 0)
	Board.set_LED_color(1, 0, 0, 0)
