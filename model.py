from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import torch.nn as nn
import cv2

if __name__ == "__main__":
    net = InceptionResnetV1(pretrained='casia-webface').eval()
    example = torch.rand(1, 3, 160, 160)
    net = torch.jit.trace(net, example)
    net.save("model.pt")