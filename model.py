from rknnlite.api import RKNNLite

class FaceModel:
    def __init__(self, rknn_file):
        self.rknn_lite = RKNNLite()
        ret = self.rknn_lite.load_rknn(rknn_file)
        if ret != 0:
            print('Load RKNN model failed')
            exit(ret)
        ret = self.rknn_lite.init_runtime()
        if ret != 0:
            print('Init runtime environment failed')
            exit(ret)
    
    def __call__(self, face):
        return self.rknn_lite.inference(inputs=[face])
    
    def __del__(self):
        self.rknn_lite.release()