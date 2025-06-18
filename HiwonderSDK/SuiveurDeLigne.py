import sys
sys.path.append('/home/pi/TurboPi/')
import HiwonderSDK.Board as Board
import HiwonderSDK.mecanum as mecanum
import HiwonderSDK.FourInfrared as infrared
import HiwonderSDK.Sonar as Sonar
import cv2
import numpy as np
import math
import signal
import Camera
import yaml_handle


def getAreaMaxContour(contours):
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None

    for c in contours:  
        contour_area_temp = abs(cv2.contourArea(c))  # Calculate the contour area
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰
            
            if contour_area_temp > 300:  
                area_max_contour =c

    return area_max_contour, contour_area_max  # 返回最大的轮廓



class SuiveurDeLigne:

    car = mecanum.MecanumChassis()
    line = infrared.FourInfrared()
    sonar = Sonar.Sonar()

    def suivre_la_ligne_jusqua_lobstacle(self,distance_de_lobstacle=20):
        nombre_consecutif_de_detection_dobstacle = 0
        nombre_max_de_detection_dobstacle = 5  # Nombre de détections consécutives pour considérer qu'il y a un obstacle
        while True:   
            sensor_data = self.line.readData()
            # 2，3 (0,1,1,0)
            if not sensor_data[0] and sensor_data[1] and sensor_data[2] and not sensor_data[3]:
                self.car.set_velocity(35,90,0)
                
                
            # 3 (0,0,1,0)
            elif not sensor_data[0] and not sensor_data[1] and sensor_data[2] and not sensor_data[3]:
                self.car.set_velocity(35,90,0.03)
                
            # 2 (0,1,0,0)
            elif not sensor_data[0] and  sensor_data[1] and not sensor_data[2] and not sensor_data[3]:
                self.car.set_velocity(35,90,-0.03)
                
            # 4  (0,0,0,1)
            elif not sensor_data[0] and not sensor_data[1] and not sensor_data[2] and sensor_data[3]:
                self.car.set_velocity(35,90,0.3)
                
            # 1 (1,0,0,0)
            elif sensor_data[0] and not sensor_data[1] and not sensor_data[2] and not sensor_data[3]:
                self.car.set_velocity(35,90,-0.3)
                
            # Après avoir effectué les actions pour la ligne, on vérifie si on détecte un obstacle
            if self.sonar.Distance < distance_de_lobstacle:
                nombre_consecutif_de_detection_dobstacle += 1
                self.car.set_velocity(0,0,0)
            else:
                # Si on ne détecte pas d'obstacle, on réinitialise le compteur
                nombre_consecutif_de_detection_dobstacle = 0
    
            if nombre_consecutif_de_detection_dobstacle >= nombre_max_de_detection_dobstacle:
                # Si on a détecté l'obstacle suffisamment de fois, on arrête la voiture
                break
            
    
    def suivre_la_ligne_jusquau_stop(self):
        
        while True:   
            sensor_data = self.line.readData()
            # 2，3 (0,1,1,0)
            if not sensor_data[0] and sensor_data[1] and sensor_data[2] and not sensor_data[3]:
                self.car.set_velocity(35,90,0)
                
            # 3 (0,0,1,0)
            elif not sensor_data[0] and not sensor_data[1] and sensor_data[2] and not sensor_data[3]:
                self.car.set_velocity(35,90,0.03)
                
            # 2 (0,1,0,0)
            elif not sensor_data[0] and  sensor_data[1] and not sensor_data[2] and not sensor_data[3]:
                self.car.set_velocity(35,90,-0.03)
                
            # 4  (0,0,0,1)
            elif not sensor_data[0] and not sensor_data[1] and not sensor_data[2] and sensor_data[3]:
                self.car.set_velocity(35,90,0.3)
                
            # 1 (1,0,0,0)
            elif sensor_data[0] and not sensor_data[1] and not sensor_data[2] and not sensor_data[3]:
                self.car.set_velocity(35,90,-0.3)
                
            
            # Détection de toute les lignes, on sort de la boucle
            elif sensor_data[0] and sensor_data[1] and sensor_data[2] and sensor_data[3]:
                self.car.set_velocity(0,0,0)
                break
            

range_rgb = {
    'red': (0, 0, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}
target_color = ('red', 'green', 'blue')


class DetecteurDeCouleur:

    isRunning = False
    detect_color = 'None'
    size = (640, 480)
    lab_data =  yaml_handle.get_yaml_data(yaml_handle.lab_file_path) 
    
    def trouver_la_couleur(self,img):
   
    
        img_copy = img.copy()
   
        frame_resize = cv2.resize(img_copy, self.size, interpolation=cv2.INTER_NEAREST)
        frame_gb = cv2.GaussianBlur(frame_resize, (3, 3), 3)
        
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间

        color_area_max = None
        max_area = 0
     
        for i in target_color:
            if i in self.lab_data:
                frame_mask = cv2.inRange(frame_lab,
                                            (self.lab_data[i]['min'][0],
                                            self.lab_data[i]['min'][1],
                                            self.lab_data[i]['min'][2]),
                                            (self.lab_data[i]['max'][0],
                                            self.lab_data[i]['max'][1],
                                            self.lab_data[i]['max'][2]))  # Effectue une opération de masque sur l'image originale
                

                opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  
                closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  
                contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # Trouver les contours
                areaMaxContour, area_max = getAreaMaxContour(contours)  # Trouver le plus grand contour
                if areaMaxContour is not None:
                    if area_max > max_area: # Trouver la plus grande surface 
                        print(f"Color: {i}, Area: {area_max}")
                        max_area = area_max
                        color_area_max = i

            # Filtrer les petits contours pour éviter les interférences, seul le contour de la plus grande surface supérieure à 300 est valide
            if max_area > 2500:  # 有找到最大面积
                
                if color_area_max == 'red':  # 红色最大
                    return "rouge"
                elif color_area_max == 'green':  # 绿色最大
                    return "vert"
                elif color_area_max == 'blue':  # 蓝色最大
                    return "bleu"
                else:
                    return "inconnu"
            return "inconnu"

