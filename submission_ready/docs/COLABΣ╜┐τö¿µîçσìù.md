# 在 Google Colab 上运行实验指南

## 🎯 为什么用 Colab？

- ✅ **免费 GPU 加速**：比本地 AMD CPU 快 5-10 倍
- ✅ **无需本地配置**：不需要安装 PyTorch 等依赖
- ✅ **随时随地运行**：只需要浏览器
- ✅ **预计时间**：5-10 分钟（GPU）vs 30-60 分钟（CPU）

---

## 📋 第一步：准备 ZIP 文件

### 手动打包（推荐，无需终端）

1. **打开项目文件夹**
   - 在文件资源管理器中打开：`d:\111_temu_商品\ST455\2026-project-gaogou\fair_order_dispatch`

2. **创建 colab_upload 文件夹**
   - 右键 → 新建 → 文件夹，命名为 `colab_upload`

3. **复制以下内容到 colab_upload 文件夹**
   - `src/` 文件夹（整个文件夹）
   - `scripts/` 文件夹（整个文件夹）
   - `shock_calibration.json` 文件（从 `results/` 文件夹里复制）
   - `requirements.txt` 文件

4. **压缩成 ZIP**
   - 右键点击 `colab_upload` 文件夹
   - 选择 "发送到" → "压缩(zipped)文件夹"
   - 会生成 `colab_upload.zip`

**最终 colab_upload 文件夹结构：**
```
colab_upload/
├── src/              (文件夹)
├── scripts/          (文件夹)
├── shock_calibration.json  (文件)
└── requirements.txt  (文件)
```

---

## 🚀 第二步：打开 Colab 并启用 GPU

1. 访问 [Google Colab](https://colab.research.google.com/)
2. 登录你的 Google 账号
3. 点击 **"新建笔记本"**
4. 点击菜单：**运行时 → 更改运行时类型**
5. 硬件加速器：选择 **GPU**（T4 或 V100）
6. 点击 **"保存"**

⚠️ **重要**：必须启用 GPU，否则实验会很慢（30-60 分钟 vs 5-10 分钟）

---

## 📤 第三步：上传并解压 ZIP

在 Colab 的第一个代码框中运行：

```python
# 上传 ZIP 文件
from google.colab import files
import zipfile
import os

print("📤 请选择 colab_upload.zip 文件...")
uploaded = files.upload()

# 解压 ZIP
for filename in uploaded.keys():
    if filename.endswith('.zip'):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall('.')
        print(f'✅ 已解压: {filename}')

# 检查解压后的文件
print("\n📁 解压后的文件:")
!ls -la

# 检查 colab_upload 文件夹内容
if os.path.exists('colab_upload'):
    print("\n📁 colab_upload 文件夹内容:")
    !ls -la colab_upload/
```

**操作提示**：点击 "选择文件" 按钮，选择你刚才创建的 `colab_upload.zip`

---

## ✅ 第四步：验证文件结构

在新的代码框中运行：

```python
import os
import sys

# 切换到 colab_upload 目录
if os.path.exists('colab_upload'):
    os.chdir('colab_upload')
    print("✅ 已切换到 colab_upload 目录")

print(f"\n📁 当前目录: {os.getcwd()}")
print("\n📋 文件列表:")
!ls -la

print("\n✅ 检查关键文件:")
print("  src 文件夹:", "✅ 存在" if os.path.exists('src') else "❌ 缺失")
print("  scripts 文件夹:", "✅ 存在" if os.path.exists('scripts') else "❌ 缺失")
print("  requirements.txt:", "✅ 存在" if os.path.exists('requirements.txt') else "❌ 缺失")
print("  shock_calibration.json:", "✅ 存在" if os.path.exists('shock_calibration.json') else "❌ 缺失")
```

**确保所有文件都显示 ✅ 存在**，然后继续下一步。

---

## ⚙️ 第五步：安装依赖并设置环境

在新的代码框中运行：

```python
# 安装依赖
print("📥 安装依赖...")
!pip install -q gymnasium stable-baselines3 pandas matplotlib scipy

# 检查 GPU
import torch
print(f"\n🖥️ PyTorch 版本: {torch.__version__}")
print(f"🖥️ GPU 可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"🖥️ GPU 型号: {torch.cuda.get_device_name(0)}")
else:
    print("⚠️ 警告：GPU 未启用！实验会很慢（30-60分钟）")
    print("   请检查：运行时 → 更改运行时类型 → 选择 GPU")

# 设置 Python 路径
import sys
sys.path.insert(0, os.path.abspath('src'))

# 创建结果目录
os.makedirs('results', exist_ok=True)
os.makedirs('figures', exist_ok=True)

# 复制 shock_calibration.json 到 results 目录
import shutil
if os.path.exists('shock_calibration.json'):
    shutil.copy('shock_calibration.json', 'results/shock_calibration.json')
    print("\n✅ 已复制 shock_calibration.json 到 results 目录")

print("\n✅ 环境设置完成！")
```

---

## 🧪 第六步：运行实验

在新的代码框中运行：

```python
print("🧪 开始运行实验...")
print("预计时间: 5-10 分钟（GPU）或 30-60 分钟（CPU）\n")

!python scripts/run_multi_seed_experiments.py

print("\n✅ 实验完成！")
```

**等待实验完成**：你会看到实时进度输出，显示 `[1/60]` 到 `[60/60]`

---

## 📊 第七步：运行统计分析

实验完成后，在新的代码框中运行：

```python
print("📊 运行统计分析...")
!python scripts/statistical_analysis.py

print("\n📁 生成的结果文件:")
!ls -la results/

print("\n📊 生成的图表:")
!ls -la figures/
```

---

## 💾 第八步：下载结果

在新的代码框中运行：

```python
from google.colab import files
import zipfile

print("📦 打包结果...")
with zipfile.ZipFile('results.zip', 'w') as zipf:
    for root, dirs, filenames in os.walk('results'):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            zipf.write(filepath)
    
    for root, dirs, filenames in os.walk('figures'):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            zipf.write(filepath)

print("💾 开始下载...")
files.download('results.zip')
print("✅ 完成！")
```

**下载位置**：文件会自动下载到你的浏览器下载文件夹（通常是 `C:\Users\你的用户名\Downloads\`）

---

## 📝 一键运行版本（可选）

如果你想一次性运行所有步骤，可以把以下代码放在一个代码框中：

```python
# ========================================
# Fair Order Dispatch - Colab 一键运行
# ========================================

# 1. 上传并解压
print("📤 步骤 1: 上传 ZIP 文件")
from google.colab import files
import zipfile
import os
import sys

uploaded = files.upload()
for filename in uploaded.keys():
    if filename.endswith('.zip'):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall('.')
        print(f'✅ 已解压: {filename}')

# 2. 切换目录并验证
if os.path.exists('colab_upload'):
    os.chdir('colab_upload')
print(f"✅ 当前目录: {os.getcwd()}")

# 3. 安装依赖
print("\n📥 步骤 2: 安装依赖")
!pip install -q gymnasium stable-baselines3 pandas matplotlib scipy

# 4. 验证 GPU
print("\n🖥️ 步骤 3: 验证 GPU")
import torch
print(f"PyTorch: {torch.__version__}")
print(f"GPU 可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
else:
    print("⚠️ GPU 未启用，实验会很慢！")

# 5. 设置环境
sys.path.insert(0, os.path.abspath('src'))
os.makedirs('results', exist_ok=True)
os.makedirs('figures', exist_ok=True)
import shutil
if os.path.exists('shock_calibration.json'):
    shutil.copy('shock_calibration.json', 'results/shock_calibration.json')

# 6. 运行实验
print("\n🧪 步骤 4: 运行实验（5-10 分钟）")
!python scripts/run_multi_seed_experiments.py

# 7. 统计分析
print("\n📊 步骤 5: 统计分析")
!python scripts/statistical_analysis.py

# 8. 下载结果
print("\n💾 步骤 6: 下载结果")
with zipfile.ZipFile('results.zip', 'w') as zipf:
    for root, dirs, filenames in os.walk('results'):
        for filename in filenames:
            zipf.write(os.path.join(root, filename))
    for root, dirs, filenames in os.walk('figures'):
        for filename in filenames:
            zipf.write(os.path.join(root, filename))

files.download('results.zip')
print("✅ 完成！")
```

---

## 🔧 如何启用 GPU 加速（重要！）

### 问题：为什么显示"设备: CPU (强制)"？

实验脚本默认强制使用 CPU，因为本地环境是 AMD 显卡。但在 Colab 上，我们需要使用 GPU 来加速。

### 解决方案：修改实验脚本

**方法 1：在 Colab 中临时修改（推荐）**

在运行实验之前，先运行这段代码来修改脚本：

```python
# 修改脚本以启用 GPU
script_path = 'scripts/run_multi_seed_experiments.py'

# 读取脚本内容
with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 删除强制使用 CPU 的代码
content = content.replace('os.environ["CUDA_VISIBLE_DEVICES"] = ""', '# os.environ["CUDA_VISIBLE_DEVICES"] = ""')
content = content.replace('device="cpu"', 'device="auto"')

# 写回文件
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 已修改脚本以启用 GPU")

# 验证 GPU 可用
import torch
print(f"GPU 可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU 型号: {torch.cuda.get_device_name(0)}")
```

**方法 2：在本地永久修改**

如果你想在本地修改脚本，打开 `scripts/run_multi_seed_experiments.py`：

1. 找到第 20-21 行：
   ```python
   # 强制使用 CPU（AMD 显卡环境）
   os.environ["CUDA_VISIBLE_DEVICES"] = ""
   ```
   改为：
   ```python
   # 强制使用 CPU（AMD 显卡环境）
   # os.environ["CUDA_VISIBLE_DEVICES"] = ""  # 在 Colab 上注释掉
   ```

2. 找到第 183 行：
   ```python
   model = PPO("MlpPolicy", env, verbose=0, seed=seed, device="cpu")
   ```
   改为：
   ```python
   model = PPO("MlpPolicy", env, verbose=0, seed=seed, device="auto")
   ```

3. 重新打包 `colab_upload.zip` 并上传到 Colab

---

## ⚠️ 注意事项

### 1. 必须启用 GPU
- 在 Colab 菜单中：**运行时 → 更改运行时类型 → GPU**
- 如果显示"设备: CPU (强制)"，说明需要修改脚本（见上面的 GPU 启用说明）

### 2. 文件会被删除
- Colab 的文件在会话结束后会被删除
- **务必下载结果**：运行完成后立即下载 `results.zip`

### 3. GPU 配额限制
- 免费版有 GPU 使用时长限制
- 如果提示 GPU 不可用，等待几小时后再试

### 4. 会话超时
- 免费版：最长 12 小时，空闲 90 分钟会断开
- 实验只需 5-10 分钟，不会超时

---

## 📥 下载结果后的操作

1. **找到下载的文件**
   - 文件在你的下载文件夹：`C:\Users\你的用户名\Downloads\results.zip`

2. **解压到项目目录**
   - 把 `results.zip` 复制到：`d:\111_temu_商品\ST455\2026-project-gaogou\fair_order_dispatch`
   - 右键解压，会覆盖现有的 `results/` 和 `figures/` 文件夹

3. **验证结果**
   - 检查 `results/` 文件夹应该有：
     - `multi_seed_results.csv`
     - `statistical_summary.csv`
     - `significance_tests.csv`
   - 检查 `figures/` 文件夹应该有更新的图表

---

## 📞 常见问题

### 问题 1：显示"设备: CPU (强制)"
**原因**：脚本默认强制使用 CPU  
**解决**：运行实验前，先运行上面"启用 GPU 加速"部分的修改代码

### 问题 2：文件夹无法上传
**原因**：Colab 拖拽不支持文件夹  
**解决**：使用 ZIP 文件上传（本指南推荐的方法）

### 问题 3：找不到 scripts 文件
**原因**：工作目录不对  
**解决**：确保运行了第四步的验证代码，所有文件都显示 ✅

### 问题 4：GPU 不可用
**原因**：未启用 GPU 运行时  
**解决**：菜单 → 运行时 → 更改运行时类型 → 选择 GPU → 保存

### 问题 5：下载的文件在哪里
**答案**：在浏览器的下载文件夹，通常是 `C:\Users\你的用户名\Downloads\`

---

**创建日期**: 2026-04-04  
**适用版本**: Google Colab (免费版/Pro)  
**预计时间**: 总共 15-20 分钟（包括上传和下载）
