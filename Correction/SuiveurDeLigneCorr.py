import sys
sys.path.append('/home/pi/TurboPi/')

import HiwonderSDK.mecanum as mecanum
import HiwonderSDK.FourInfrared as infrared
import HiwonderSDK.Sonar as Sonar
import CampTI.DetecteurDistance as DetecteurDistance
import HiwonderSDK.Board as Board
import time

class SuiveurDeLigne:

    car = mecanum.MecanumChassis()
    line = infrared.FourInfrared()
    sonar = Sonar.Sonar()

    # FONCTION D'EXEMPLE QUI SUIT LA LIGNE
    def suivre_la_ligne(self):
        while True:   
            sensor_data = self.line.readData()
            # 2，3 (0,1,1,0)
            if self.detection_milieu(sensor_data):
                self.car.set_velocity(35,90,0)
                
            # 3 (0,0,1,0)
            elif self.detection_centre_droite(sensor_data):
                self.car.set_velocity(35,90,0.03)
                
            # 2 (0,1,0,0)
            elif self.detection_centre_gauche(sensor_data):
                self.car.set_velocity(35,90,-0.03)
                
            # 4  (0,0,0,1)
            elif self.detection_droite_seulement(sensor_data):
                self.car.set_velocity(35,90,0.3)
                
            # 1 (1,0,0,0)
            elif self.detection_gauche_seulement(sensor_data):
                self.car.set_velocity(35,90,-0.3)
            
 
            time.sleep(0.01)
    

    # TODO 2 : À COMPLÉTER 
    # LE BUT DE CETTE FONCTION EST DE SUIVRE LA LIGNE JUSQU'À` CE QU'ON SOIT SUR UNE LIGNE PERPENDICULAIRE (UN STOP)
    def suivre_la_ligne_jusquau_stop(self):
        #Écrire le code ici
        while True:   
            sensor_data = self.line.readData()
            # 2，3 (0,1,1,0)
            if self.detection_milieu(sensor_data):
                self.car.set_velocity(35,90,0)
                
            # 3 (0,0,1,0)
            elif self.detection_centre_droite(sensor_data):
                self.car.set_velocity(35,90,0.03)
                
            # 2 (0,1,0,0)
            elif self.detection_centre_gauche(sensor_data):
                self.car.set_velocity(35,90,-0.03)
                
            # 4  (0,0,0,1)
            elif self.detection_droite_seulement(sensor_data):
                self.car.set_velocity(35,90,0.3)
                
            # 1 (1,0,0,0)
            elif self.detection_gauche_seulement(sensor_data):
                self.car.set_velocity(35,90,-0.3)
                
            elif self.all_black(sensor_data):
                self.car.set_velocity(0,0,0)
                return 

            time.sleep(0.01)


        
    # TODO 3 : À COMPLÉTER SI VOUS AVEZ LE TEMPS
    # LE BUT DE CETTE FONCTION EST DE SUIVRE LA LIGNE JUSQU'À CE QUE LE CAPTEUR DE DISTANCE VOIT UN OBSTACLE
    # INDICE : UTILISER LA CLASSE DetecteurDistance
    # OPTIONNEL : POUR EVITER DES QUE LE CAPTEUR DE DISTANCE VOIT UN OBSTACLE MÊME S'IL Y EN A PAS,
    # IL SERAIT JUDISCIEUX DE FAIRE PLUSIEURS VÉRIFICATIONS AVANT D'ARRETER LE VEHICULE
    def suivre_la_ligne_jusqua_obstacle(self,distance_detection):
        
        #Écrire le code ici
        
        #Pour faire arrêter le véhicule, utiliser la ligne suivante
        self.car.set_velocity(0, 0, 0)
        return
    
    
    #TODO 1 : À COMPLETER
    def detection_tous_les_capteurs(self,sensor_data:list[bool]) -> bool:
        """
        Détecte si tous les capteurs sont activés.
        
        :return: True si tous les capteurs sont activés, sinon False.
        """
        # (1,1,1,1)
        #LE BUT EST DE VÉRIFIER SI TOUS LES CAPTEURS SONT ACTIVÉS ET RETOURNER TRUE SI C'EST LE CAS
        # SINON RETOURNER FALSE
        return sensor_data[0] and sensor_data[1] and sensor_data[2] and sensor_data[3]
        

    def detection_centre_droite(self,sensor_data:list[bool]) -> bool:
        """
        Détecte si le capteur du milieu droit est activé.
        
        :return: True si le capteur du milieu droit est activé, sinon False.
        """
        # (0,0,1,0)
        return not sensor_data[0] and not sensor_data[1] and sensor_data[2] and not sensor_data[3]
    
    def detection_centre_gauche(self,sensor_data:list[bool]) -> bool:
        """
        Détecte si le capteur du milieu gauche est activé.
        
        :return: True si le capteur du milieu gauche est activé, sinon False.
        """
        # (0,1,0,0)
        return not sensor_data[0] and sensor_data[1] and not sensor_data[2] and not sensor_data[3]
       
    def detection_milieu(self,sensor_data:list[bool]) -> bool:
        """
        Détecte si les deux capteurs du milieu sont activés.
        
        :return: True si les deux capteurs du milieu sont activés, sinon False.
        """
        # (0,1,1,0)
        return not sensor_data[0] and sensor_data[1] and sensor_data[2] and not sensor_data[3]
         
    def detection_droite_seulement(self,sensor_data:list[bool]) -> bool:
        """
        Détecte si SEULEMENT le capteur droit est activé.
        
        :return: True si le capteur droit est activé, sinon False.
        """
        # (0,0,0,1)
        return not sensor_data[0] and not sensor_data[1] and not sensor_data[2] and sensor_data[3]
            
    def detection_gauche_seulement(self,sensor_data:list[bool]) -> bool:
        """
        Détecte si SEULEMENT le capteur gauche est activé.
        
        :return: True si le capteur gauche est activé, sinon False.
        """
        # (1,0,0,0)
        return sensor_data[0] and not sensor_data[1] and not sensor_data[2] and not sensor_data[3]
    
