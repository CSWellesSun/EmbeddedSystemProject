from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import torch.nn as nn

class FaceModel(nn.Module):
    def __init__(self):
        super(FaceModel, self).__init__()
        self.mtcnn = MTCNN()
        self.resnet = InceptionResnetV1(pretrained="casia-webface").eval()

    def forward(self, img):
        img_cropped = self.mtcnn(img)
        if img_cropped is None:
            return None
        else:
            return self.resnet(img_cropped.unsqueeze(0))[0].detach().numpy()

if __name__ == "__main__":
    net = FaceModel()
    torch.save(net, "model.pt")