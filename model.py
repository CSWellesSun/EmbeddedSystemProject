from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import torch.nn as nn
import cv2

if __name__ == "__main__":
    net = InceptionResnetV1(pretrained='casia-webface').eval()
    example = torch.rand(1, 3, 160, 160)
    # img = cv2.imread('./user/u0/img0.png')
    # detect = MTCNN()
    # img = detect(img)
    # net(img.unsqueeze(0))
    net = torch.jit.trace(net, example)
    net.save("model.pt")
    # torch.onnx.export(net, example, './resnet.onnx', opset_version=12, input_names=['input'], output_names=['output'])