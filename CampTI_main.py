import sys
sys.path.append('/home/pi/TurboPi/')
import CampTI.DetecteurCouleur as DetecteurCouleur
import CampTI.DetecteurDistance as DetecteurDistance
import CampTI.SuiveurDeLigne as SuiveurDeLigne
import HiwonderSDK.Board as Board
import time

suiveur_de_ligne = SuiveurDeLigne.SuiveurDeLigne()

if __name__ == "__main__":
    # ÉCRIRE VOTRE CODE ICI
    
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
    

    suiveur_de_ligne.suivre_la_ligne()