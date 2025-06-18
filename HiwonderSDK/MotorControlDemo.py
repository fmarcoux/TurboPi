#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/TurboPi/')
import time
import signal
import threading
import HiwonderSDK.Board as Board

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)
    
def MotorStop():
    Board.setMotor(1, 0) 
    Board.setMotor(2, 0)
    Board.setMotor(3, 0)
    Board.setMotor(4, 0)

start = True

def Stop(signum, frame):
    global start

    start = False
    MotorStop()
    

signal.signal(signal.SIGINT, Stop)

if __name__ == '__main__':
    
    while True:
        Board.setMotor(1, 35)
        time.sleep(1)
        Board.setMotor(1, 60)
        time.sleep(2)
        Board.setMotor(1, 90)
        time.sleep(3)    
        
        if not start:
            MotorStop()
            break
    
    
        