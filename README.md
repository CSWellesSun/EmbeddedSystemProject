# Embedded System Project

## 环境

使用 `python-3.8`。执行 `pip install -r requirements.txt` 安装必要的库。

我们使用的嵌入式设备是 [Firefly RK3568](https://wiki.t-firefly.com/zh_CN/ROC-RK3568-PC/)。

## 使用 (TODO)

首先需要将 `config.example.ini` 中的 `ChatGPT` 接口进行修改，目前要求一个支持 `POST` 且内容为 `{"msg":"xxx"}` 的后端接口，之后会修改成 `OPENAI` API。修改完成后将该文件重命名为 `config.ini`。

其次我们需要脸部图片，具体需要放在 `from` 、`test_faces`、`user` 三个文件夹中。