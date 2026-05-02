<<<<<<< Updated upstream:fair_order_dispatch-作业版本/README.md
# Fair Order Dispatch - 项目文件结构说明

## 📁 项目组织

```
fair_order_dispatch/
│
├── 📄 final_submission_cn.ipynb    ⭐ 主要交付物（课程作业提交文件）
├── 📄 README.md                    📖 项目说明（本文件）
├── 📄 requirements.txt             📦 Python 依赖列表
├── 📄 pyproject.toml               ⚙️ 项目配置
│
├── 📂 docs/                        📚 项目文档
│   ├── PLAN.md                     详细执行计划（三阶段改进路线）
│   ├── CHANGELOG.md                修改日志（记录所有变更）
│   ├── PROGRESS.md                 当前进度追踪
│   ├── task_plan.md                任务计划（历史记录）
│   ├── findings.md                 研究发现和决策记录
│   └── progress_old.md             旧的进度记录（存档）
│
├── 📂 src/                         💻 源代码
│   └── fair_dispatch/
│       ├── __init__.py
│       ├── config.py               配置参数
│       ├── environment.py          仿真环境
│       ├── metrics.py              评价指标
│       ├── baselines.py            基线算法
│       └── rl_interface.py         强化学习接口
│
├── 📂 scripts/                     🔧 实验脚本
│   ├── evaluate_baselines.py      基线评估
│   ├── train_ppo.py                PPO 训练
│   ├── generate_plots.py          生成图表
│   ├── run_multi_seed_experiments.py  ⭐ 多种子实验（新）
│   └── statistical_analysis.py    ⭐ 统计分析（新）
│
├── 📂 tests/                       🧪 测试代码
│   ├── test_environment.py
│   ├── test_metrics.py
│   ├── test_baselines.py
│   └── test_notebook_deliverable.py
│
├── 📂 notebooks/                   📓 Notebook 草稿
│   └── fair_order_dispatch_report.ipynb
│
├── 📂 results/                     📊 实验结果
│   ├── baseline_results.csv       基线结果
│   ├── ppo_results.csv             PPO 结果
│   ├── shock_calibration.json      冲击校准
│   ├── multi_seed_results.csv      ⭐ 多种子结果（待生成）
│   ├── statistical_summary.csv     ⭐ 统计汇总（待生成）
│   └── significance_tests.csv      ⭐ 显著性检验（待生成）
│
└── 📂 figures/                     📈 图表
    ├── episode_revenue_by_scene.png
    ├── final_gini_by_scene.png
    ├── shock_income_cdf.png
    └── alpha_tradeoff.png
```

---

## ⭐ 重要文件标记

### 🔴 最重要（课程作业提交）
- **`final_submission_cn.ipynb`** - 最终提交的 notebook，包含所有代码、结果和说明

### 🟠 核心脚本（运行实验）
- **`scripts/run_multi_seed_experiments.py`** - 运行多种子实验（5个种子，60个实验）
- **`scripts/statistical_analysis.py`** - 统计分析和显著性检验

### 🟡 配置和依赖
- **`requirements.txt`** - 安装依赖：`pip install -r requirements.txt`
- **`src/fair_dispatch/config.py`** - 实验参数配置

### 🟢 文档（了解项目）
- **`docs/PLAN.md`** - 三阶段改进计划（作业→会议→期刊）
- **`docs/CHANGELOG.md`** - 所有修改记录
- **`docs/PROGRESS.md`** - 当前进度和待办事项

---

## 🚀 快速开始

### 1. 安装依赖
```bash
cd "d:\111_temu_商品\ST455\2026-project-gaogou\fair_order_dispatch"
pip install -r requirements.txt
```

### 2. 运行多种子实验（30-60分钟）
```bash
C:\Users\Administrator\AppData\Local\Programs\Python\Python39\python.exe scripts/run_multi_seed_experiments.py
```

### 3. 运行统计分析（几秒钟）
```bash
C:\Users\Administrator\AppData\Local\Programs\Python\Python39\python.exe scripts/statistical_analysis.py
```

### 4. 在 Jupyter 中查看结果
```bash
jupyter notebook final_submission_cn.ipynb
```
然后点击 "Run All"

---

## 📋 当前状态

### ✅ 已完成
- [x] 修复 notebook 中的5处编码问题
- [x] 补充参考文献到8条
- [x] 创建多种子实验脚本
- [x] 创建统计分析脚本
- [x] 创建依赖管理文件
- [x] 整理项目文件结构

### ⏳ 待完成
- [ ] 运行多种子实验
- [ ] 运行统计分析
- [ ] 更新 notebook 的结果表格和图表
- [ ] 在 Jupyter 中测试 Run All
- [ ] 添加小组贡献说明
- [ ] 最终检查和提交

---

## 💡 技术说明

- **硬件环境**: AMD 显卡，使用 CPU 版本 PyTorch
- **Python 版本**: 3.9.8
- **代码语言**: 所有代码和注释使用中文
- **实验时间**: 单次训练约1-2分钟，完整实验约30-60分钟

---

## 📞 团队协作

本项目使用团队协作模式完成：
- **doc-writer**: 补充参考文献和文档
- **notebook-fixer**: 修复编码问题
- **experiment-runner**: 编写实验脚本
- **stats-analyzer**: 编写统计分析脚本

所有修改都记录在 `docs/CHANGELOG.md` 中。

---

## 📚 更多信息

- 详细执行计划：`docs/PLAN.md`
- 修改日志：`docs/CHANGELOG.md`
- 当前进度：`docs/PROGRESS.md`
- 研究发现：`docs/findings.md`

---

**最后更新**: 2026-04-04  
**项目状态**: 准备运行实验
=======
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/BgjVEvds)
# ST455 projects

You are expected to work in a group of 4 (feel free to form your own teams) to conduct a project on reinforcement learning and write a report. Please provide percentage contributions to the project at the end of the report (e.g., member A 30%, member B 30%, member C 20%, member D 20%). These ratios are proportional to your project grade which are calculated as follows:

$$\textrm{member}\~\~\textrm{grade} = \textrm{project}\~\~\textrm{grade} \times \frac{\textrm{member}\~\~\textrm{contribution}}{\textrm{maximum}\~\~\textrm{contribution}}$$

For example, for a group with 4 members contributing, respectively, 50%, 30%, 10%, 10%, and
the project grade is 72 (out of 100), the individuals grades are:

$$72\times \frac{50}{50}=72,\quad 72\times \frac{30}{50} =43.2,\quad 72\times\frac{10}{50}=14.4.$$

If not provided, I assume the four of you contribute equally to the project. 

## Project marking rubrics:

You can find it in the repo.

## Project topics 
 
Your project should demonstrate an understanding of concepts, methods and models in the area of Reinforcement Learning and how to use/apply them using software frameworks in Python. This should involve using knowledge acquired in the course and building on this knowledge through an independent study to go more deeply into a specific subject. Your project may cover different aspects of _reinforcement learning_ methods, demonstrating an understanding of their suitability for a given class of problems, how to implement and validate them using synthetic and/or real datasets. The project can also comprise case studies involving specialised and/or complex scenarios in which you can experiment with different actions, states, rewards and policies. You may consider establishing some theoretical properties regarding RL methods or proposing your own methods. Development of the new theories and methodologies are **not** necessary, but you will get a high mark if these developments contain enough novelty.
 
Your **report would typically be in the form of a Jupyter notebook**, containing code, **along with a Markdown text** explaining different parts. You may want to provide a tutorial-like exposition for certain subjects covered in your project. For example, this may include instructions for loading specific libraries and/or packages you have used, preprocessing tasks you have applied to your datasets and specific requirements for running your models. **Your report and any other project related material should be submitted in the GitHub classroom repo** that will be assigned to your project.
 
It is expected from **your report to be** presented up to a high professional standard. This means that it has to be **structured well**, neat and polished. 
Your report should have a title, abstract, main content body, conclusion, and a list of references. 
In the abstract, please make sure to briefly describe what is the problem addressed by your project, why is the problem a problem, 
what is your solution and why you have chosen given solution. The abstract should be short, a paragraph of 5-10 sentences. 

You may use **visualizations** in your report, for example using Matplotlib, Tensorboard and other Python libraries. 

Your **report may describe a working prototype application**. In this case, your report should contain a clear and full description of the steps that one needs to follow in order to run your application. 

Your **report should cite any references that you use** (including the reference for the code). You may also discuss and cite any previously proposed alternative solutions to your problem. The conclusion section should briefly summarise the results of your project, highlight your main findings, and briefly discuss any interesting avenues for future research.

You are allowed to discuss your project topic with Chengchun. The list of candidate projects is given below to give you some idea about potential project topics. **You may (but you are not expected) to take one of the project topics listed below**. 

## Candidate project topics

Here you'll find references to various resources such as research papers and blogs that may inspire your choice of the course project. You may also check references provided in the lecture materials.

You're welcome to propose a topic that is not included in the list below.

#### RLVR and LLM reasoning

* Shao et al., [DeepSeekMath: Pushing the Limits of Mathematical
Reasoning in Open Language Models](https://arxiv.org/pdf/2402.03300)
* Liu et al., [Understanding R1-Zero-Like Training: A Critical Perspective
](https://arxiv.org/pdf/2503.20783)
* Chu et al., [GPG: A SIMPLE AND STRONG REINFORCEMENT
LEARNING BASELINE FOR MODEL REASONING](https://arxiv.org/pdf/2504.02546)
* Zhou et al., [Demystifying Group Relative Policy Optimization: Its Policy
Gradient is a U-Statistic](https://arxiv.org/pdf/2603.01162)

#### RLHF and LLM alignment

* Ouyang et al., [Training language models to follow instructions
with human feedback](https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf)
* Rafailov et al., [Direct Preference Optimization:
Your Language Model is Secretly a Reward Model](https://arxiv.org/pdf/2305.18290)
* Xu et al., [Doubly Robust Alignment for Large Language Models](https://arxiv.org/pdf/2506.01183)
* Ye et al., [ROBUST REINFORCEMENT LEARNING FROM HUMAN FEEDBACK FOR
LARGE LANGUAGE MODELS FINE-TUNING](https://arxiv.org/pdf/2504.03784)
* Lee et al., [PEBBLE: Feedback-Efficient Interactive Reinforcement Learning
via Relabeling Experience and Unsupervised Pre-training](https://arxiv.org/pdf/2106.05091)
* Liang et al., [REWARD UNCERTAINTY FOR EXPLORATION IN
PREFERENCE-BASED REINFORCEMENT LEARNING](https://openreview.net/pdf?id=OWZVD-l-ZrC)


#### Causal Reinforcement Learning
* Li et al., [Causal Reinforcement Learning: An Instrumental Variable Approach](https://arxiv.org/abs/2103.04021)
* Shi et al., [A Minimax Learning Approach to Off-Policy Evaluation in Confounded Partially Observable Markov Decision Processes](https://arxiv.org/abs/2111.06784)
* Tennenholtz et al., [Off-Policy Evaluation in Partially Observable Environments](https://arxiv.org/pdf/1909.03739.pdf)
* Xu et al., [An Instrumental Variable Approach to
Confounded Off-Policy Evaluation](https://arxiv.org/pdf/2212.14468.pdf)
* Zhang et al., [Markov Decision Processes with Unobserved
Confounders: A Causal Approach](https://www.cs.purdue.edu/homes/eb/mdp-causal.pdf)

#### Games
* Atari [zoo](https://eng.uber.com/atari-zoo-deep-reinforcement-learning/)
* [Model based reinforcement learning for Atari](https://arxiv.org/pdf/1903.00374.pdf) 

#### Optimization

* Zhu et al, [Causal Discovery with Reinforcement Learning](https://arxiv.org/pdf/1906.04477.pdf)
* [TraceIn](https://ai.googleblog.com/2021/02/tracin-simple-method-to-estimate.html#:~:text=TracIn%20is%20a%20simple%2C%20easy,github%20linked%20in%20the%20paper.) A Simple Method to Estimate the Training Data Influence 
* Microsoft [MARO (Multi-Agent Resource Optimization)](https://github.com/microsoft/maro) 
* Kool et al, [Attention, Learn to Solve Routing Problems!](https://openreview.net/forum?id=ByxBFsRqYm) 
* Mao et al, [Resource management with deep reinforcement learning](https://people.csail.mit.edu/alizadeh/papers/deeprm-hotnets16.pdf), Hotnets 2016
* Mirhoseini et al, [Device placement optimization with reinforcement learning](https://arxiv.org/abs/1706.04972), ICML 2017
* Mirhoseini et al, [A hierarhical model for device placement](https://openreview.net/pdf?id=Hkc-TeZ0W), ICLR 2018
* Bello et al, [Neural combinatorial optimization with reinforcement learning](https://arxiv.org/pdf/1611.09940.pdf), ICLR 2017

#### Medical application

* Gao et al., [Offline Learning of Closed-Loop Deep Brain Stimulation
Controllers for Parkinson Disease Treatment](https://arxiv.org/pdf/2302.02477.pdf)
* Komorowski et al., [The Artificial Intelligence Clinician learns optimal treatment strategies for sepsis in intensive care](https://www.nature.com/articles/s41591-018-0213-5)
* Li et al., [Testing Stationarity and Change Point Detection in Reinforcement Learning
](https://arxiv.org/abs/2203.01707)
* Luckett et al., [Estimating Dynamic Treatment Regimes in Mobile Health Using V-Learning](https://www.tandfonline.com/doi/abs/10.1080/01621459.2018.1537919)
* Shi et al., [Does the Markov Decision Process Fit the Data:
Testing for the Markov Property in Sequential Decision Making](http://proceedings.mlr.press/v119/shi20c/shi20c.pdf)
* Zhou et al., [Estimating Optimal Infinite Horizon Dynamic
Treatment Regimes via pT-Learning](https://arxiv.org/pdf/2110.10719.pdf)

#### Ridesharing

* Xu et al., [large scale fleet management a planning and learning approach](https://users.wpi.edu/~yli15/courses/DS504Fall18/includes/p1774-lin.pdf)
* Shi et al., [Off-Policy Confidence Interval Estimation
with Confounded Markov Decision Process](https://arxiv.org/pdf/2202.10589.pdf)
* Shi et al., [Dynamic Causal Effects Evaluation in A/B Testing with a Reinforcement Learning Framework](https://www.tandfonline.com/doi/full/10.1080/01621459.2022.2027776)
* Tang et al., [A Deep Value-network Based Approach for Multi-Driver Order
Dispatching](https://arxiv.org/pdf/2106.04493.pdf)
* Wan et al., [Pattern Transfer Learning for Reinforcement Learning in Order Dispatching](https://arxiv.org/pdf/2105.13218.pdf)

#### Protein structure prediction

* Senior et al, [AlphaFold: Improved protein structure prediction using potentials from deep learning](https://deepmind.com/research/publications/AlphaFold-Improved-protein-structure-prediction-using-potentials-from-deep-learning)

#### Finance

* Deng et al, [Deep direct reinforcement learning for financial
signal representation and trading](http://www.cslt.org/mediawiki/images/a/aa/07407387.pdf), IEEE Trans. on Neural Networks and Learning Systems, 2016

### Some past project topics

* Creating a conversational ChatBot using deep Q-network
* Fairness or efficiency: strategy analysis for coronavirus medical treatment using RL
* Financial portfolio management using deep RL
* Deep direct recurrent reinforcement learning for algorithmic trading
* Reinforcement learning for trade execution with Alpha and risk aversion
* Solving ATT48 by deep reinforcement learning
* Stock trading by deep reinforcement learning
>>>>>>> Stashed changes:submission_ready/README.md
