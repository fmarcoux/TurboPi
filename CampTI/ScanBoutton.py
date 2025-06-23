# import os, sys, time
# import RPi.GPIO as GPIO
# import threading 



# # Class 
# class ScanneurBoutton():
#     key1_pin = 13
#     key2_pin = 23
    
#     running : bool = False
#     stopped : bool = False
#     thread : threading.Thread = None
 
#     def __init__(self):
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.key1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#         GPIO.setup(self.key2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#         self.running = False
#         self.stopped = False
        
#         self.thread = threading.Thread(target=self.scan_button)
#         self.thread.start()

#     def cycle(self):
#         if self.is_idle():
#             self.running = True
#             print('ScanBoutton started')
#         elif self.is_running():
#             self.stopped = True
#             self.running = False
#             print('ScanBoutton stopped')
#         elif self.is_stopped():
#             self.running = True
#             self.stopped = False
#             print('ScanBoutton restarted')

#     def is_idle(self):
#         return not self.running and not self.stopped
#     def is_running(self):
#         return self.running and not self.stopped
#     def is_stopped(self):
#         return self.stopped and not self.running

#     def scan_button(self):
#         while True:
#             if GPIO.input(self.key1_pin) == GPIO.LOW:
#                 time.sleep(0.05)
#                 if GPIO.input(self.key1_pin) == GPIO.LOW:
#                     self.cycle()
            
#             elif GPIO.input(self.key2_pin) == GPIO.LOW:
#                 time.sleep(0.05)
#                 if GPIO.input(self.key2_pin) == GPIO.LOW:
#                     if self.stopped:
#                         self.running = True
#                         print('sudo halt')
#                         os.system('sudo halt')
#             else:
#                 time.sleep(0.05)




# servo_test = False
# if __name__ == "__main__":
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(key1_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#     GPIO.setup(key2_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#     key1_pressed = False
#     key2_pressed = False
#     count = 0
#     while True:
#         if GPIO.input(key1_pin) == GPIO.LOW:
#             time.sleep(0.05)
#             if GPIO.input(key1_pin) == GPIO.LOW:
#                 if key1_pressed == True:
#                     count += 1
#                     servo_test = True
#                     if count == 60:
#                         count = 0
#                         servo_test = False
#                         key1_pressed = False
#                         print('reset_wifi')
#                         reset_wifi()
#             else:
#                 count = 0
#                 continue
            
#         elif GPIO.input(key2_pin) == GPIO.LOW:
#             time.sleep(0.05)
#             if GPIO.input(key2_pin) == GPIO.LOW:
#                 if key2_pressed == True:
#                     count += 1
#                     if count == 60:
#                         count = 0
#                         key2_pressed = False
#                         print('sudo halt')
#                         os.system('sudo halt')
#             else:
#                 count = 0
#                 continue
#         else:
#             if servo_test:
#                 servo_test = False
#                 os.system("sudo python3 /home/pi/TurboPi/HiwonderSDK/BuzzerControlDemo.py")
                        
#             count = 0
#             if not key1_pressed:
#                 key1_pressed = True
#             if not key2_pressed:
#                 key2_pressed = True
#             time.sleep(0.05)

        