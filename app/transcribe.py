#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

import whisper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="将音频文件转换为文字输出",
    )
    parser.add_argument(
        "audio_path",
        type=Path,
        help="音频文件路径（如 .wav/.mp3/.m4a）",
    )
    parser.add_argument(
        "--model",
        default="base",
        help="Whisper 模型大小（tiny/base/small/medium/large），默认 base",
    )
    parser.add_argument(
        "--language",
        default="zh",
        help="音频语言代码，默认 zh",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="输出文本文件路径（可选，不填则打印到控制台）",
    )
    parser.add_argument(
        "--fp16",
        action="store_true",
        help="启用 fp16 推理（GPU 环境可更快）",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.audio_path.exists():
        print(f"找不到音频文件: {args.audio_path}", file=sys.stderr)
        return 1

    model = whisper.load_model(args.model)
    result = model.transcribe(
        str(args.audio_path),
        language=args.language,
        fp16=args.fp16,
    )
    text = (result.get("text") or "").strip()

    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
