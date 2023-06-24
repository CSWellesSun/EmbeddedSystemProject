# Embedded System Project

## 环境

基本必须使用如下环境才能运行。

### RKNN-Toolkit2 (PC) 

我们已经提供了 `resnet.rknn` 模型，这一步可以跳过，如果要自己生成，具体方法如下：

使用 `Ubuntu18.04`，`python-3.6`。`RKNN-Toolkit2`的版本是 1.4.0，首先执行 `RKNN-Toolkit2` 所需要的所有环境，特别是 `torch==1.10.1` 和 `torchvision==0.11.2`。

然后安装 `facenet-pytorch`的环境，由于RKNN不支持 `ReduceL1 / ReduceL2`等算子，而 `InceptionResnetV1` 里存在 `F.normalize(x, p=2)` 无法被转换成 RKNN，所以需要进入 `facenet-pytorch` 源码修改 `InceptionResnetV1`，将 `forward` 最后一层的 `normalize` 删除。

最后执行 `python save_model.py` 就能导出 `model.pt`，然后再执行 `python model.py` 就能得到 `resnet.rknn` 模型。

### RKNN-Toolkit-Lite2 (板子)

我们使用的嵌入式设备是 [Firefly RK3568](https://wiki.t-firefly.com/zh_CN/ROC-RK3568-PC/)。`RKNN` 在 `RK3568` 上使用 NPU 必须要用 `Debain` 系统！系统使用官网提供的 [Debain10](https://www.t-firefly.com/doc/download/107.html)（该系统限制极大！），`RKNN-Toolkit2`的版本是 1.4.0，我们只需要安装 `RKNN-Toolkit-Lite2` 即可（安装其中的 `packages`）。

然后极力推荐使用 [MiniConda](https://docs.conda.io/en/latest/miniconda.html) 以及 [whl官方下载网站](https://download.pytorch.org/whl/torch_stable.html)。默认的 `python3` 和 `pip3` 极难下载到正确的环境！

我们使用的是 `python3.9`，具体的环境参考 `requirements.txt`，其中依旧是 `torch` 和 `torchvision` 的版本最为重要！其他基本不冲突即可。

## 外设

### 摄像头

使用 USB 摄像头，只需要该摄像头能支持 `OpenCV` 即可。注意将 `camera.py` 中的 `camera` 变量改成具体的 `ID`。如果不知道 `ID` 值，可以执行 `python camera.py` 来得到获取 `ID` 值。

## 使用

### 执行

`python system.py` 即可。一开始有可能出现 `torchvision` 中导入 `io.image` 失败的 `warning`，但是对系统执行不影响。

### 配置

首先需要将 `config.example.ini` 中的 `ChatGPT` 接口进行修改，目前仅支持 `Azure OpenAI` 接口（学生可免费申请），注意使用 `Azure OpenAI` 接口不需要代理。

### RKNN-Toolkit-Lite2 源码修改

在执行过程中可能会出现 `ToolKit-Lite2` 的报错，大意是 `inputs[0]` 类型不是 `numpy`，该类型为 `tensor`,只需要加上一行 `inputs = [inputs[i].numpy() for i in range(len(inputs))]` 即可。 

### 注册

当使用 `FaceRecoginition` 的 `register` 功能时，会在 `user` 目录下创建一个新的用户 `u<id>`（例如 `u0 / u1 / u2` ），其中会保存图像处理之后的图片 `img<id>.png` 、经过 `facenet` 抽取的特征 `embed.npy` 以及用户的姓名年龄信息 `info.txt`。

使用 `MobaXterm` ssh 连接到板子之后就可以打开摄像头窗口，按下 `s` 键即可保存图片并抽取特征。
