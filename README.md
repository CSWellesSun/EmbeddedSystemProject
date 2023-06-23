# Embedded System Project

## 环境

使用 `python-3.8`。执行 `pip install -r requirements.txt` 安装必要的库。

我们使用的嵌入式设备是 [Firefly RK3568](https://wiki.t-firefly.com/zh_CN/ROC-RK3568-PC/)。

## 使用 (TODO)

### 配置

首先需要将 `config.example.ini` 中的 `ChatGPT` 接口进行修改，目前仅支持 `Azure OpenAI` 接口（学生可免费申请），注意使用 `Azure OpenAI` 接口不需要代理。

### RKNN转换（TODO）

首先使用 `python model.py` 将模型保存成 `model.pt`。

### 注册

当使用 `FaceRecoginition` 的 `register` 功能时，会在 `user` 目录下创建一个新的用户 `u<id>`（例如 `u0 / u1 / u2` ），其中会保存图像处理之后的图片 `img<id>.png` 、经过 `facenet` 抽取的特征 `embed.npy` 以及用户的姓名年龄信息 `info.txt`。

当没有嵌入式设备的摄像头的时候，可以使用 `camera.py` 中被注释掉的 `getframe` 和 `setfoldername` 函数，只需要提前将拍摄好的人脸照片放在某一文件夹下，然后使用 `setfoldername` 然后即可通过 `getframe` 从中获取图像。
