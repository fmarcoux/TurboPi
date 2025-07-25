#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/TurboPi/')
import time
import signal
import HiwonderSDK.mecanum as mecanum

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

chassis = mecanum.MecanumChassis()

start = True

def Stop(signum, frame):
    global start

    start = False

    chassis.set_velocity(0,0,0)  # 关闭所有电机
    

signal.signal(signal.SIGINT, Stop)

if __name__ == '__main__':
    while start:
        chassis.set_velocity(0,90,0.3)
        time.sleep(3)
        chassis.set_velocity(0,90,-0.3)
        time.sleep(3)
    chassis.set_velocity(0,0,0)


        
