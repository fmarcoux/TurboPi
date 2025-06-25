import sys
sys.path.append('/home/pi/TurboPi/')
import CampTI.DetecteurCouleur as DetecteurCouleur
import CampTI.DetecteurDistance as DetecteurDistance
import CampTI.SuiveurDeLigne as SuiveurDeLigne
import HiwonderSDK.Board as Board
import Camera
import time
import signal
import HiwonderSDK.mecanum as mecanum
from multiprocessing import Event
import numpy as np

import HiwonderSDK.BuzzerControlDemo as buzz
#Stop event utilise pour arrêter proprement le programme
stop_event = Event()

chassis = mecanum.MecanumChassis()
suiveur_de_ligne = SuiveurDeLigne.SuiveurDeLigne(stop_event)
detecteur_couleur = DetecteurCouleur.DetecteurDeCouleur()
sonar = DetecteurDistance.DetecteurDeDistance()


def Stop(signum, frame):
    print("CLEAN STOP")
    global stop_event

    if not stop_event.is_set():
        stop_event.set()
        
    camera = Camera.Camera()
    camera.camera_close()
    

signal.signal(signal.SIGINT, Stop)





if __name__ == "__main__":
    
    # Indice visuel que le code est démarré, on change la LED de couleur
        
    Board.set_LED_color(0, 255, 0, 0)  # Rouge
    Board.set_LED_color(1, 255, 0, 0)  
    time.sleep(0.5) 
    Board.set_LED_color(0, 0, 255, 0)  # Vert
    Board.set_LED_color(1, 0, 255, 0) 
    time.sleep(0.5)
    Board.set_LED_color(0, 0, 0, 255)  # Bleu
    Board.set_LED_color(1, 0, 0, 255)  
    time.sleep(0.5)
    
    
    # ECRIRE VOTRE CODE ICI.
   
    
    #TODO 3: Avancer pendant 1 secondes lorsque le capteur de distance
    # détecte un object à moins de 20 cm (200 mm)


    

    
    
