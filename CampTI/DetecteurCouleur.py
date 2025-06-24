import sys
sys.path.append('/home/pi/TurboPi/')
import HiwonderSDK.Board as Board
import cv2
import numpy as np
import Camera
import yaml_handle


range_rgb = {
    'red': (0, 0, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}
target_color = ('red', 'green', 'blue')



    
class DetecteurDeCouleur:

    size = (640, 480)
    lab_data =  yaml_handle.get_yaml_data(yaml_handle.lab_file_path) 
    
    def __del__(self):
        if self.camera is not None:
            self.camera.camera_close()
            cv2.destroyAllWindows()
    
    def __init__(self):
       
        self.camera = Camera.Camera()
        self.camera.camera_close()
        cv2.destroyAllWindows()
        self.camera.camera_open(correction=True)
        print("init done")
        
    def obtenir_image(self):
        if self.camera.opened:
            frame = self.camera.frame
            if frame is not None:
                return frame
            else:
                print("Erreur lors de la capture de l'image.")
                return None
        else:
            print("La caméra n'est pas ouverte.")
            return None
    
    def change_couleur_LED(self,color):
        if color == "red":
            Board.set_LED_color(0, 255, 0, 0)
            Board.set_LED_color(1, 255, 0, 0)
        elif color == "green":
            Board.set_LED_color(0, 0, 255, 0)
            Board.set_LED_color(1, 0, 255, 0)
        elif color == "blue":
            Board.set_LED_color(0, 0, 0, 255)
            Board.set_LED_color(1, 0, 0, 255)
        else:
            Board.set_LED_color(0, 0, 0, 0)
            Board.set_LED_color(1, 0, 0, 0)

    def trouver_la_couleur(self):
        img = self.obtenir_image()#.copy()
        if img is None:
            print("image none!!!")
            return None
        else:
            img = img.copy()
   
        frame_resize = cv2.resize(img, self.size, interpolation=cv2.INTER_NEAREST)
        frame_gb = cv2.GaussianBlur(frame_resize, (3, 3), 3)
        
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  

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
        if max_area > 2500:  
            if color_area_max == 'red': 
                self.change_couleur_LED("red")
                return "rouge"
            elif color_area_max == 'green':
                self.change_couleur_LED("green")
                return "vert"
            elif color_area_max == 'blue':
                self.change_couleur_LED("blue")
                return "bleu"
            else:
                self.change_couleur_LED("black")
                return "inconnu"
        return "inconnu"

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

