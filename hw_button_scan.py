import os, sys, time
import RPi.GPIO as GPIO
import subprocess

key1_pin = 13
key2_pin = 23

start_main_script = False
stop_main_script = False
script_running = False

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(key1_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(key2_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    key1_pressed = False
    key2_pressed = False
    count = 0
    while True:
        if GPIO.input(key1_pin) == GPIO.LOW:
            time.sleep(0.05)
            if GPIO.input(key1_pin) == GPIO.LOW:
                start_main_script = True
                stop_main_script = False
                count += 1
            
            if GPIO.input(key1_pin) == GPIO.HIGH and count >100:
                print("shutting down...")
                os.system("sudo reboot -h now")
                
    
   
        elif GPIO.input(key2_pin) == GPIO.LOW:
            time.sleep(0.05)
            if GPIO.input(key2_pin) == GPIO.LOW:
                start_main_script = False
                stop_main_script = True 
   
        else:
            count=0
            if start_main_script and not script_running:
                print("Starting process")
                start_main_script = False
                script_running = True
                subprocess.Popen(["sudo","python3","/home/pi/TurboPi/CampTI_main.py"])
                print("Laucnhed process")
                
                #os.system("sudo python3 /home/pi/TurboPi/CampTI_main.py")
                
            elif stop_main_script and script_running:
                print("start of stopping")
                script_running = False
                try:
                    os.system("sudo pkill -f CampTI_main.py")
                finally:
                    subprocess.Popen(["sudo","python3","/home/pi/TurboPi/Functions/reset_motor.py"])
                print("end of stopping")
                
                
                #os.system("sudo python3 /home/pi/TurboPi/Functions/reset_motor.py")
                
