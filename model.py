from facenet_pytorch import MTCNN, InceptionResnetV1


class FaceModel:
    def __init__(self):
        self.mtcnn = MTCNN()
        self.resnet = InceptionResnetV1(pretrained="casia-webface").eval()

    def __call__(self, img):
        img_cropped = self.mtcnn(img)
        if img_cropped is None:
            return None
        else:
            return self.resnet(img_cropped.unsqueeze(0))[0].detach().numpy()
