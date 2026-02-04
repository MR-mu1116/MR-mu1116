#!/usr/bin/env python3
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import whisper


def parse_keywords(raw: str) -> list[str]:
    return [item.strip() for item in raw.split("、") if item.strip()]


class TranscribeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("录音转文字")
        self.geometry("720x520")
        self.resizable(True, True)

        self.audio_path = tk.StringVar(value="")
        self.model_name = tk.StringVar(value="base")
        self.language = tk.StringVar(value="zh")
        self.keywords = tk.StringVar(value="")

        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self, padding=12)
        container.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(4, weight=1)

        ttk.Label(container, text="音频文件:").grid(row=0, column=0, sticky="w")
        audio_entry = ttk.Entry(container, textvariable=self.audio_path)
        audio_entry.grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(container, text="选择文件", command=self._select_file).grid(
            row=0, column=2, sticky="e"
        )

        ttk.Label(container, text="模型:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        model_box = ttk.Combobox(
            container,
            textvariable=self.model_name,
            values=["tiny", "base", "small", "medium", "large"],
            state="readonly",
        )
        model_box.grid(row=1, column=1, sticky="w", padx=8, pady=(8, 0))

        ttk.Label(container, text="语言:").grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(container, textvariable=self.language).grid(
            row=2, column=1, sticky="w", padx=8, pady=(8, 0)
        )

        ttk.Label(container, text="关键词(用“、”隔开):").grid(
            row=3, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Entry(container, textvariable=self.keywords).grid(
            row=3, column=1, sticky="ew", padx=8, pady=(8, 0)
        )

        ttk.Button(container, text="开始转写", command=self._transcribe).grid(
            row=3, column=2, sticky="e", pady=(8, 0)
        )

        ttk.Label(container, text="转写结果:").grid(
            row=4, column=0, sticky="nw", pady=(8, 0)
        )
        self.output = tk.Text(container, wrap="word")
        self.output.grid(row=4, column=1, columnspan=2, sticky="nsew", padx=8, pady=(8, 0))

    def _select_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=[("Audio Files", "*.wav *.mp3 *.m4a *.flac *.aac *.ogg"), ("All Files", "*.*")],
        )
        if file_path:
            self.audio_path.set(file_path)

    def _transcribe(self) -> None:
        audio_path = Path(self.audio_path.get())
        if not audio_path.exists():
            messagebox.showerror("错误", "请先选择有效的音频文件。")
            return

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "转写中，请稍候...\n")
        self.update_idletasks()

        model = whisper.load_model(self.model_name.get())
        result = model.transcribe(
            str(audio_path),
            language=self.language.get().strip() or "zh",
        )
        text = (result.get("text") or "").strip()

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

        keywords = parse_keywords(self.keywords.get())
        hit = [word for word in keywords if word in text]
        if hit:
            messagebox.showinfo("关键词提示", f"检测到关键词: {', '.join(hit)}")


if __name__ == "__main__":
    app = TranscribeApp()
    app.mainloop()
