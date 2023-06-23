import subprocess
import cv2
import numpy as np
import os


class CameraManager:
    def __init__(self, height=240, weight=320, camera=5):
        self.height = height
        self.weight = weight
        self.camera = camera
        self.paramset_inst = (
            "v4l2-ctl --device=/dev/video%d --set-fmt-video=width=%d,height=%d,pixelformat=1"
            % (camera, weight, height)
        )
        self.getframe_inst = (
            "v4l2-ctl  --device=/dev/video%d --stream-mmap=3 --stream-count=1 --stream-to=myframe.raw"
            % (camera)
        )
        subprocess.call(self.paramset_inst, shell=True)

    def getframe(self):
        while True:
            subprocess.call(self.getframe_inst, shell=True)
            with open("myframe.raw", "rb") as f:
                buffer = f.read()
                img = np.frombuffer(buffer, dtype=np.uint8)
            img = img.reshape([2, 480, 640])[0]
            yield img

    # def getframe(self):
    #     file = os.listdir(self.foldname)
    #     for filename in file:
    #         filename = self.foldname + "\\" + filename
    #         yield cv2.imread(filename)

    # def setfoldername(self, path):
    #     self.foldname = path


if __name__ == "__main__":
    camera = CameraManager()
    img = camera.getframe()
    cv2.imwrite("frame.png", img)
