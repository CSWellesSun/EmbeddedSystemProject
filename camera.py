import subprocess
import cv2
import numpy as np
import os


class CameraManager:
    def __init__(self, camera=9):
        self.camera = camera
        self.cap = cv2.VideoCapture(camera)
        

    def getframe(self):
        while True:
            ret, frame = self.cap.read()
            yield frame
    
    def get_one_frame(self):
        ret, frame = self.cap.read()
        if ret == False:
            return None
        return frame

    def __del__(self):
        self.cap.release()
    
if __name__ == "__main__":
    ID = 0
    while(1):
        cap = cv2.VideoCapture(ID)
        # get a frame
        ret, frame = cap.read()
        if ret == False:
            ID += 1
        else:
            print(ID)
            break
