# 录音转文字

这是一个将音频文件转成文字的小工具，基于 OpenAI Whisper 本地模型推理。

## 环境准备

- Python 3.9+
- 需要本地安装 `ffmpeg`

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get update && sudo apt-get install -y ffmpeg
```

## 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 使用示例

```bash
python transcribe.py ./sample.m4a
```

指定模型、语言、输出文件：

```bash
python transcribe.py ./sample.m4a --model small --language zh --output output.txt
```

启用 fp16（GPU 环境）：

```bash
python transcribe.py ./sample.m4a --fp16
```
