from model import FaceModel
from camera import CameraManager
import os
import cv2
import numpy as np
import time


class FaceRecoginition:
    def __init__(self):
        self.camera = CameraManager()
        self.facemodel = FaceModel()
        self.embeds = []
        self.labels = []
        folders = os.listdir("user")
        for i, foldname in enumerate(folders):
            filename = "user" + "\\" + foldname + "\\" + "embed.npy"
            self.embeds.append(np.load(filename))
            self.labels.extend(["u%d" % i for j in range(self.embeds[-1].shape[0])])
        self.embeds = np.concatenate(self.embeds)

    def register(self):
        print("输入用户信息")
        name = input("姓名:").strip()
        age = input("年龄:").strip()

        print("按任意键拍摄一张人脸,输入ctrl+C停止拍摄")
        list = self.camera.getframe()
        imgs = []
        embeds = []
        try:
            while True:
                img = next(list)
                cv2.imshow("", img)
                cv2.waitKey(0)
                use = input("是否使用该图?(Y/n)")
                if use == "n":
                    continue

                embed = self.facemodel(img)
                if embed is None:
                    print("特征提取失败,请重新拍摄照片")
                else:
                    imgs.append(img)
                    embeds.append(embed)
                    print("特征提取成功")
        except KeyboardInterrupt:
            print("拍摄结束")
            folderlist = os.listdir("user")
            newfoldername = "u%d" % (len(folderlist))
            newfoldername = "user\\" + newfoldername
            os.makedirs(newfoldername)

            for i, img in enumerate(imgs):
                cv2.imwrite(newfoldername + "\\img%d.png" % (i), img)

            with open(newfoldername + "\\info.txt", "wt") as info:
                info.writelines([name + "\n", age])

            embeds = np.array(embeds)
            np.save(newfoldername + "\\embed.npy", embeds)

            self.embeds = np.concatenate([self.embeds, embeds])
            self.labels.extend(
                ["u%d" % len(folderlist) for i in range(embeds.shape[0])]
            )
        except Exception:
            raise Exception
            print("发生其他异常,请联系管理人员维修")

    def recognite(self):
        videolist = self.camera.getframe()
        while True:
            time.sleep(1)
            img = next(videolist)
            embed = self.facemodel(img)
            if embed is None:
                continue
            else:
                norm = np.linalg.norm(self.embeds - embed, axis=1)
                index = norm.argmin()
                diff = norm.min()
                if diff < 0.6:
                    return self.labels[index]
                else:
                    continue


if __name__ == "__main__":
    f = FaceRecoginition()
    # f.camera.setfoldername("from/u0/face")
    # f.register()
    # f.camera.setfoldername("from/u1/face")
    # f.register()
    # f.camera.setfoldername("from/u2/face")
    f.register()
