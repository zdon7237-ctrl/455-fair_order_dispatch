# 在 Google Colab 上运行实验指南

## 🎯 为什么用 Colab？

- ✅ **免费 GPU 加速**：比本地 CPU 明显更快
- ✅ **无需本地配置**：不需要安装 PyTorch 等依赖
- ✅ **随时随地运行**：只需要浏览器
- ✅ **预计时间**：15-30 分钟（GPU）vs 60 分钟以上（CPU）

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

⚠️ **重要**：建议启用 GPU，否则实验会很慢（CPU 通常需要 60 分钟以上）

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
```

**确保所有文件都显示 ✅ 存在**，然后继续下一步。

---

## ⚙️ 第五步：安装依赖并设置环境

在新的代码框中运行：

```python
# 安装依赖
print("📥 安装依赖...")
!pip install -q -r requirements.txt

# 检查 GPU
import torch
print(f"\n🖥️ PyTorch 版本: {torch.__version__}")
print(f"🖥️ GPU 可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"🖥️ GPU 型号: {torch.cuda.get_device_name(0)}")
else:
    print("⚠️ 警告：GPU 未启用！实验会很慢（通常 60 分钟以上）")
    print("   请检查：运行时 → 更改运行时类型 → 选择 GPU")

# 设置 Python 路径
import sys
sys.path.insert(0, os.path.abspath('src'))

# 创建结果目录
os.makedirs('results', exist_ok=True)
os.makedirs('figures', exist_ok=True)

print("\n✅ 环境设置完成！")
```

---

## 🧪 第六步：运行实验

在新的代码框中运行：

```python
print("🧪 开始运行实验...")
print("预计时间: 15-30 分钟（GPU）或 60 分钟以上（CPU）\n")

!python scripts/evaluate_baselines.py
!python scripts/train_ppo.py --seed 0 --total-timesteps 20000
!python scripts/run_multi_seed_experiments.py --total-timesteps 20000

print("\n✅ 实验完成！")
```

**等待实验完成**：前两条命令会生成 baseline/PPO 的收入快照，第三条命令会运行 `60` 个多种子实验。

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
!pip install -q -r requirements.txt

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

# 6. 运行实验
print("\n🧪 步骤 4: 运行实验（15-30 分钟）")
!python scripts/evaluate_baselines.py
!python scripts/train_ppo.py --seed 0 --total-timesteps 20000
!python scripts/run_multi_seed_experiments.py --total-timesteps 20000

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

## 🔧 GPU 使用说明

当前脚本已经使用 `device="auto"`，不需要在 Colab 里手动改代码。只要运行时类型选择 GPU，`stable-baselines3`/PyTorch 会自动使用可用设备；如果 Colab 没有分配 GPU，脚本仍然可以在 CPU 上运行，只是会明显更慢。

---

## ⚠️ 注意事项

### 1. 必须启用 GPU
- 在 Colab 菜单中：**运行时 → 更改运行时类型 → GPU**
- 如果显示 GPU 不可用，先确认运行时类型已经切换到 GPU，再重新运行依赖安装和实验代码。

### 2. 文件会被删除
- Colab 的文件在会话结束后会被删除
- **务必下载结果**：运行完成后立即下载 `results.zip`

### 3. GPU 配额限制
- 免费版有 GPU 使用时长限制
- 如果提示 GPU 不可用，等待几小时后再试

### 4. 会话超时
- 免费版：最长 12 小时，空闲 90 分钟会断开
- GPU 下通常可以在一个会话内完成；CPU 会慢很多，建议不要让页面长时间空闲。

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
     - `baseline_shock_incomes.csv`
     - `ppo_shock_incomes.csv`
   - 检查 `figures/` 文件夹应该有更新的图表

---

## 📞 常见问题

### 问题 1：GPU 不可用或运行很慢
**原因**：Colab 没有分配 GPU，或运行时类型仍是 CPU。  
**解决**：菜单 → 运行时 → 更改运行时类型 → 选择 GPU → 保存，然后重新运行依赖安装和实验代码。

### 问题 2：文件夹无法上传
**原因**：Colab 拖拽不支持文件夹  
**解决**：使用 ZIP 文件上传（本指南推荐的方法）

### 问题 3：找不到 scripts 文件
**原因**：工作目录不对  
**解决**：确保运行了第四步的验证代码，所有文件都显示 ✅

### 问题 4：没有生成 `shock_income_cdf.png`
**原因**：没有先运行 `evaluate_baselines.py` 和 `train_ppo.py`，缺少司机收入快照。  
**解决**：按第六步的完整顺序重新运行三条实验命令，再运行 `statistical_analysis.py`。

### 问题 5：下载的文件在哪里
**答案**：在浏览器的下载文件夹，通常是 `C:\Users\你的用户名\Downloads\`

---

**创建日期**: 2026-04-04  
**适用版本**: Google Colab (免费版/Pro)  
**预计时间**: 总共 20-40 分钟（包括上传和下载，取决于 Colab GPU 分配情况）
