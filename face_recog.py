from camera import CameraManager
import os
import cv2
import numpy as np
import time
import torch
from facenet_pytorch import MTCNN
from model import FaceModel


class FaceRecoginition:
    def __init__(self, rknn_file):
        self.camera = CameraManager()
        self.facedetector = MTCNN()
        self.facemodel = FaceModel(rknn_file)
        self.embeds = []
        self.labels = []
        folders = os.listdir("user")
        for i, foldname in enumerate(folders):
            filename = "user" + "/" + foldname + "/" + "embed.npy"
            self.embeds.append(np.load(filename))
            self.labels.extend(["u%d" % i for j in range(self.embeds[-1].shape[0])])
        self.embeds = np.concatenate(self.embeds)

    def register(self):
        print("输入用户信息")
        name = input("姓名:").strip()
        age = input("年龄:").strip()

        print("按任意键拍摄一张人脸,输入ctrl+C停止拍摄")
        imgs = []
        embeds = []
        try:
            while True:
                img = None
                while True:
                    img = self.camera.get_one_frame()
                    if img is None:
                        continue
                    cv2.imshow("Video", img) # 显示图像
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        break
                use = input("是否使用该图?(Y/n)")
                if use == "n":
                    continue

                face = self.facedetector(img)
                if face is None:
                    print("未检测到人脸,请重新拍摄照片")
                    continue
                embed = self.facemodel(face)
                if embed is None:
                    print("特征提取失败,请重新拍摄照片")
                else:
                    embed = embed[0]
                    embed = torch.nn.functional.normalize(torch.tensor(embed), p=2, dim=1)
                    embed = embed.numpy()
                    imgs.append(img)
                    embeds.append(embed)
                    print("特征提取成功")
        except KeyboardInterrupt:
            print("拍摄结束")
            if len(embeds) == 0:
                return
            folderlist = os.listdir("user")
            newfoldername = "u%d" % (len(folderlist))
            newfoldername = "user/" + newfoldername
            os.makedirs(newfoldername)

            for i, img in enumerate(imgs):
                cv2.imwrite(newfoldername + "/img%d.png" % (i), img)

            with open(newfoldername + "/info.txt", "wt") as info:
                info.writelines([name + "\n", age])

            embeds = np.array(embeds)
            embeds = embeds[:][0][:]
            np.save(newfoldername + "/embed.npy", embeds)

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
            face = self.facedetector(img)
            if face is None:
                continue
            face = face.unsqueeze(0)
            embed = self.facemodel(face)
            embed = embed[0]
            embed = torch.nn.functional.normalize(torch.tensor(embed), p=2, dim=1)
            embed = embed.numpy()
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
    f.register()
