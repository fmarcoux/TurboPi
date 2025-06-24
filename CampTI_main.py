


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

chassis = mecanum.MecanumChassis()


start = True

def Stop(signum, frame):
    print("CLEAN STOP")
    global start

    start = False
    camera = Camera.Camera()
    camera.camera_close()
    



signal.signal(signal.SIGINT, Stop)


suiveur_de_ligne = SuiveurDeLigne.SuiveurDeLigne()


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
    
    
    # ÉCRIRE VOTRE CODE ICI
    bear = DetecteurCouleur.DetecteurDeCouleur()
    sonar = DetecteurDistance.DetecteurDeDistance()
    suiveur_de_ligne.test()
    print(sonar.detecteur_distance())
    time.sleep(3)
    suiveur_de_ligne.test()
    while(start):
        print(bear.trouver_la_couleur())
        time.sleep(1)


 #   
#
    #suiveur_de_ligne.suivre_la_ligne()
    
    
