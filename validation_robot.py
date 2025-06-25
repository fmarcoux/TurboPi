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
import threading
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

def func_distance(event):
	while not event.is_set():
		distance = sonar.detecteur_distance()
		if distance <  200:
			Board.setBuzzer(1)
			time.sleep(0.5)
			Board.setBuzzer(0)
		
def func_couleur(event):
	while not event.is_set():
		couleur = detecteur_couleur.trouver_la_couleur()
		detecteur_couleur.change_couleur_LED(couleur)


def func_darth_vader(event):
	while not event.is_set():
		buzz.imperial_walk()


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


	chassis.tourner_90_a_droite()
	chassis.tourner_90_a_gauche()

	thread_distance = threading.Thread(target=func_distance, args=(stop_event,))
	thread_distance.start()

	thread_couleur = threading.Thread(target=func_couleur, args=(stop_event,))
	thread_couleur.start()
	
	thread_couleur.join()
	thread_distance.join()

	
	
	
	
	
