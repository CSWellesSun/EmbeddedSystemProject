# Embedded System Project

## 环境

使用 `python-3.8`。执行 `pip install -r requirements.txt` 安装必要的库。

我们使用的嵌入式设备是 [Firefly RK3568](https://wiki.t-firefly.com/zh_CN/ROC-RK3568-PC/)。

## 使用 (TODO)

首先需要将 `config.example.ini` 中的 `ChatGPT` 接口进行修改，目前仅支持 `Azure OpenAI` 接口（学生可免费申请），注意使用 `Azure OpenAI` 接口不需要代理。

其次我们需要脸部图片，具体需要放在 `from` 、`test_faces`、`user` 三个文件夹中。