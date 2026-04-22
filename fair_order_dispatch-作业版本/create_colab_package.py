#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Colab upload bundle."""

import shutil
from pathlib import Path

# Project paths.
PROJECT_ROOT = Path(__file__).parent
COLAB_DIR = PROJECT_ROOT / "colab_upload"

print("📦 创建 Colab 上传包...")

# Reset the output folder.
if COLAB_DIR.exists():
    print(f"  删除旧的 {COLAB_DIR.name} 文件夹...")
    shutil.rmtree(COLAB_DIR)

# Create a fresh bundle.
print(f"  创建 {COLAB_DIR.name} 文件夹...")
COLAB_DIR.mkdir()

# Copy the project files.
print("  复制文件...")

# Copy src.
print("    - src/")
shutil.copytree(PROJECT_ROOT / "src", COLAB_DIR / "src")

# Copy scripts.
print("    - scripts/")
shutil.copytree(PROJECT_ROOT / "scripts", COLAB_DIR / "scripts")

# Copy the frozen shock level.
shock_file = PROJECT_ROOT / "results" / "shock_calibration.json"
if shock_file.exists():
    print("    - shock_calibration.json")
    shutil.copy(shock_file, COLAB_DIR / "shock_calibration.json")
else:
    print("    ⚠️ shock_calibration.json 不存在，跳过")

# Copy requirements.
req_file = PROJECT_ROOT / "requirements.txt"
if req_file.exists():
    print("    - requirements.txt")
    shutil.copy(req_file, COLAB_DIR / "requirements.txt")
else:
    print("    ⚠️ requirements.txt 不存在，跳过")

print("\n✅ 完成！")
print(f"\n📁 文件已准备在: {COLAB_DIR}")
print("\n下一步:")
print("  1. 右键点击 'colab_upload' 文件夹")
print("  2. 选择 '发送到' → '压缩(zipped)文件夹'")
print("  3. 会生成 'colab_upload.zip'")
print("  4. 上传到 Colab")
