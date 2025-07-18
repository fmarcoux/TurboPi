#!/usr/bin/python3
#coding=utf8
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
import pandas as pd
import HiwonderSDK.Sonar as Sonar
import HiwonderSDK.Board as Board
import HiwonderSDK.mecanum as mecanum

# Évitement d'obstacles par ultrasons

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

car = mecanum.MecanumChassis()

speed = 40
old_speed = 0
distance = 500
Threshold = 30.0
distance_data = []

TextSize = 12
TextColor = (0, 255, 255)

turn = True
forward = True
HWSONAR = None
stopMotor = True
__isRunning = False


# Position initiale du robot
def initMove():
    car.set_velocity(0,90,0)
    servo_data = yaml_handle.get_yaml_data(yaml_handle.servo_file_path)
    servo1 = servo_data['servo1']
    servo2 = servo_data['servo2']
    Board.setPWMServoPulse(1, servo1, 1000)
    Board.setPWMServoPulse(2, servo2, 1000)

# Réinitialisation des variables
def reset():
    global turn
    global speed
    global forward
    global distance
    global old_speed
    global Threshold
    global stopMotor
    global __isRunning
    
    speed = 40
    old_speed = 0
    distance = 500
    Threshold = 30.0
    turn = True
    forward = True
    stopMotor = True
    __isRunning = False

    # App initialization call
def init():
    print("Avoidance Init")
    initMove()
    reset()
    
__isRunning = False
# App start call
def start():
    global __isRunning
    global stopMotor
    global forward
    global turn
    
    turn = True
    forward = True
    stopMotor = True
    __isRunning = True
    print("Avoidance Start")

# App stop call
def stop():
    global __isRunning
    __isRunning = False
    car.set_velocity(0,90,0)
    time.sleep(0.3)
    car.set_velocity(0,90,0)
    print("Avoidance Stop")

# App exit call
def exit():
    global __isRunning
    __isRunning = False
    car.set_velocity(0,90,0)
    time.sleep(0.3)
    car.set_velocity(0,90,0) # Control the robot movement function, linear speed 0 (0~100), direction angle 90 (0~360), yaw angular speed 0 (-2~2)
    HWSONAR.setPixelColor(0, Board.PixelColor(0, 0, 0))
    HWSONAR.setPixelColor(1, Board.PixelColor(0, 0, 0))
    print("Avoidance Exit")

# Définir la vitesse d'évitement d'obstacles
def setSpeed(args):
    global speed
    speed = int(args[0])
    return (True, ())
 
# Définir le seuil d'évitement d'obstacles
def setThreshold(args):
    global Threshold
    Threshold = args[0]
    return (True, (Threshold,))

# Get current avoidance threshold
def getThreshold(args):
    global Threshold
    return (True, (Threshold,))

# 机器人移动逻辑处理
def move():
    global turn
    global speed
    global forward
    global distance
    global Threshold
    global old_speed
    global stopMotor
    global __isRunning

    while True:
        if __isRunning:   
            if speed != old_speed:   # 同样的速度值只设置一次 
                old_speed = speed
                car.set_velocity(speed,90,0) # 控制机器人移动函数,线速度speed(0~100)，方向角90(0~360)，偏航角速度0(-2~2)
                
            if distance <= Threshold:   # 检测是否达到距离阈值
                if turn: # 做一个判断防止重复发指令
                    turn = False
                    forward = True
                    stopMotor = True
                    car.set_velocity(0,90,-0.5) # 距离小于阈值，设置机器人向左转
                    time.sleep(0.5)
                
            else:
                if forward: # 做一个判断防止重复发指令
                    turn = True
                    forward = False
                    stopMotor = True
                    car.set_velocity(speed,90,0) # 距离大于阈值，设置机器人向前移动
        else:
            if stopMotor: # 做一个判断防止重复发指令
                stopMotor = False
                car.set_velocity(0,90,0)  # 关闭所有电机
            turn = True
            forward = True
            time.sleep(0.03)
 
# 运行子线程
th = threading.Thread(target=move)
th.setDaemon(True)
th.start()

# 机器人图像和传感器检测处理
def run(img):
    global HWSONAR
    global distance
    global distance_data
    
    dist = HWSONAR.getDistance() / 10.0 # 获取超声波传感器距离数据

    distance_data.append(dist) # 距离数据缓存到列表
    data = pd.DataFrame(distance_data)
    data_ = data.copy()
    u = data_.mean()  # 计算均值
    std = data_.std()  # 计算标准差

    data_c = data[np.abs(data - u) <= std]
    distance = data_c.mean()[0]

    if len(distance_data) == 5: # 多次检测取平均值
        distance_data.remove(distance_data[0])

    return cv2.putText(img, "Dist:%.1fcm"%distance, (30, 480-30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, TextColor, 2)  # 把超声波测距值打印在画面上


#关闭前处理
def manual_stop(signum, frame):
    global __isRunning
    
    print('关闭中...')
    __isRunning = False
    car.set_velocity(0,90,0)  # 关闭所有电机

if __name__ == '__main__':
    init()
    start()
    HWSONAR = Sonar.Sonar()
    camera = Camera.Camera()
    camera.camera_open(correction=True) # 开启畸变矫正,默认不开启
    signal.signal(signal.SIGINT, manual_stop)
    while __isRunning:
        img = camera.frame
        if img is not None:
            frame = img.copy() # 复制图像
            Frame = run(frame)  
            frame_resize = cv2.resize(Frame, (320, 240)) # 画面缩放到320*240
            cv2.imshow('frame', frame_resize)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            time.sleep(0.01)
    camera.camera_close()
    cv2.destroyAllWindows()
    