import sys
sys.path.append('/home/pi/TurboPi/')
import HiwonderSDK.Sonar as Sonar
import HiwonderSDK.Board as Board
import numpy as np
import time

class DetecteurDeDistance:

    sonar = Sonar.Sonar()
    def __init__(self,buffer_size=100,time_to_scan=1):
        
        # vous pouvez modifer la valeur de self.buffer_size et expérimenter avec! :)
        self.buffer_size = buffer_size
        
        self.dodo = time_to_scan/buffer_size
        
        self.buffer = np.zeros(self.buffer_size)
        self.buffer_index = 0 
        self.max_value = 5000
        
    def distance(self):
        
        return int(self.sonar.getDistance())
    
    def distance_moyenne(self):
        
        dist = self.distance()
        
        
        if dist == 5000:
            
            return np.median(self.buffer)
        else:
            self.buffer[self.buffer_index] = self.distance()
    
            self.buffer_index += 1 
            if self.buffer_index == self.buffer_size-1:
                self.buffer_index = 0
            
            return np.median(self.buffer)
            
    def detecteur_distance(self):
        
        """
        Detecte si la distance mesurée est inférieure à distance_max_mm. 
        Si la distance est inférieure, les LEDs RGB s'allument en vert, sinon elles s'allument en rouge.
        :param distance_max_mm: distance max en mm
        :return: True si la distance est inférieure à distance_max_mm, False sinon
        """
        self.buffer = np.zeros(self.buffer_size)
        
        for i in range(self.buffer_size):
            self.distance_moyenne()
            time.sleep(self.dodo)
            
        return np.median(self.buffer)
                
    
    
