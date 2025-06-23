import sys
sys.path.append('/home/pi/TurboPi/')
import HiwonderSDK.Sonar as Sonar
import HiwonderSDK.Board as Board

class DetecteurDeDistance:

    sonar = Sonar.Sonar()

    def distance(self):
        return self.sonar.getDistance()
    
    def detecteur_distance(self,distance_max_mm=200):
        """
        Detecte si la distance mesurée est inférieure à distance_max_mm. 
        Si la distance est inférieure, les LEDs RGB s'allument en vert, sinon elles s'allument en rouge.
        :param distance_max_mm: distance max en mm
        :return: True si la distance est inférieure à distance_max_mm, False sinon
        """
        if self.distance() < distance_max_mm:
            Board.set_LED_color(0,0, 255, 0)  # Vert
            Board.set_LED_color(1,0, 255, 0)  # Vert
            return True
        else:
            Board.set_LED_color(0, 255,0, 0)  # Vert
            Board.set_LED_color(1, 255,0, 0)  # Vert
            
            return False
    
    