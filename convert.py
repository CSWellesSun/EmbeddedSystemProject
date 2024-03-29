import numpy as np
import cv2
from rknn.api import RKNN
import torchvision.models as models
import torch
import os
# from model import FaceModel

def show_outputs(output):
    output_sorted = sorted(output, reverse=True)
    top5_str = '\n-----TOP 5-----\n'
    for i in range(5):
        value = output_sorted[i]
        index = np.where(output == value)
        for j in range(len(index)):
            if (i + j) >= 5:
                break
            if value > 0:
                topi = '{}: {}\n'.format(index[j], value)
            else:
                topi = '-1: 0.0\n'
            top5_str += topi
    print(top5_str)


def show_perfs(perfs):
    perfs = 'perfs: {}\n'.format(perfs)
    print(perfs)


def softmax(x):
    return np.exp(x)/sum(np.exp(x))

def torch_version():
    import torch
    torch_ver = torch.__version__.split('.')
    torch_ver[2] = torch_ver[2].split('+')[0]
    return [int(v) for v in torch_ver]

if __name__ == '__main__':
    print(torch.__version__)
    if torch_version() < [1, 9, 0]:
        import torch
        print("Your torch version is '{}', in order to better support the Quantization Aware Training (QAT) model,\n"
              "Please update the torch version to '1.9.0' or higher!".format(torch.__version__))
        exit(0)

    # model = './model1.pt'
    model = './model.pt'

    input_size_list = [[1, 3, 160, 160]]

    # Create RKNN object
    rknn = RKNN(verbose=True)

    # Pre-process config
    # print('--> Config model')
    # rknn.config(mean_values=[123.675, 116.28, 103.53], std_values=[58.395, 58.395, 58.395])
    rknn.config(target_platform='rk3568')
    # print('done')

    # Load model
    print('--> Loading model')
    ret = rknn.load_pytorch(model=model, input_size_list=input_size_list)
    # ret = rknn.load_onnx(model=model, input_size_list=input_size_list)
    if ret != 0:
        print('Load model failed!')
        exit(ret)
    print('done')

    # Build model
    print('--> Building model')
    ret = rknn.build(do_quantization=False)
    if ret != 0:
        print('Build model failed!')
        exit(ret)
    print('done')

    # Export rknn model
    print('--> Export rknn model')
    ret = rknn.export_rknn('./model.rknn')
    if ret != 0:
        print('Export rknn model failed!')
        exit(ret)
    print('done')

    rknn.release()
