# OmniTraffic

可控的时空交通推理生成 pipeline 与基准测试。

## 下载

| 数据集 | 描述 | 链接 |
|--------|------|------|
| OmniTraffic_Dataset | 仿真数据 + 渲染图像 (scenario_dataset) | [HuggingFace](https://huggingface.co/datasets/CROHuang/Omnitraffic_Dataset) |
| OmniTraffic_Benchmark | VQA 样本 (vqa_benchmark) | [HuggingFace](https://huggingface.co/datasets/CROHuang/OmniTraffic_Benchmark) |
| Blender 环境文件 | 3D 交通环境 (`.blend`) | [GitHub Releases](https://github.com/Traffic-Alpha/OmniTraffic/releases) |

---

## 基准测试统计

| 指标 | 数值 |
|------|------|
| 交叉口数量 | 12 个真实场景 |
| 环境类型 | 仿真 + 真实世界 |
| VQA 样本数量 | 8M |
| 人工验证测试集 | 3K |
| 任务层级 | 3 级（感知 / 推理 / 决策支持） |

---

## Pipeline 概览

```
traffic_scenarios (12 个交叉口)
    ↓
scenario_collector (5 种收集策略 + 事件定义)
    ↓
scenario_dataset (仿真数据 + 渲染图像)
    ↓
vqa_benchmark (VQA 生成)
```

OmniTraffic 支持**受控**（仿真）和**自然条件**（真实世界）两种评估模式。

---

## 交通场景

![12 个交叉口概览](./assets/12_intersections.png)

基准测试包含 12 个真实世界交叉口，重建为可编辑的 3D 交通环境：

| # | 地点 | 描述 |
|---|------|------|
| 1 | Beijing_Beihuan | 北京城市交叉口 |
| 2 | Beijing_Beishahe | 住宅区交叉口 |
| 3 | Beijing_Changjianglu | 商业区交叉口 |
| 4 | Beijing_Gaojiaoyuan | 郊区交叉口 |
| 5 | Beijing_Pinganli | 市中心交叉口 |
| 6 | Beijing_Yongrunlu | 高流量走廊 |
| 7 | Chengdu_Chenghannanlu | 成都中心城区交叉口 |
| 8 | Chengdu_Guanghua | 科技区交叉口 |
| 9 | France_Massy | 欧洲城市交叉口 |
| 10 | Hongkong_YMT | 香港城市交叉口 |
| 11 | SouthKorea_Songdo | 韩国智慧城交叉口 |
| 12 | Tianjin_zhijingdao | 天津主路交叉口 |

每个交叉口包含：
- 可编辑的 3D 交通环境（Blender `.blend` 文件）
- SUMO 路网定义（`.net.xml`）
- 交通需求配置（`.rou.xml`）
- 信号相位定义

---

## 场景采集器

使用不同控制策略收集数据，生成多样化交通场景。

### 采集策略

| 策略 | 描述 |
|------|------|
| **RL** | 纯强化学习信号控制策略 |
| **Fixed Timing** | 传统固定配时方案 |
| **Random** | 随机信号相位选择 |
| **RL+Rule** | RL 策略 + 规则覆盖（紧急车辆、障碍物等特殊事件） |
| **MaxQ+Rule** | MaxQ 排队算法 + 规则覆盖 |

### 事件定义

各场景通过 SUMO 配置文件（`.sumocfg`）定义事件：

| 事件 | 描述 |
|------|------|
| `barrier` | 道路障碍物部署 |
| `crashed` | 车辆碰撞事故 |
| `fluctuating_commuter` | 通勤高峰交通需求波动 |
| `high_density` | 高交通密度时段 |
| `low_density` | 低交通密度时段 |
| `increasing_demand` | 逐渐增加的交通需求 |
| `random_perturbation` | 随机交通流量扰动 |

### 使用方法

```bash
cd /path/to/OmniTraffic

# RL 策略采集
MAP=Hongkong_YMT SCENE=normal_fluctuating_commuter_barrier python scenario_collector/collector/rl_collector.py

# 固定配时采集
MAP=France_Massy SCENE=easy_high_density_barrier python scenario_collector/collector/fixed_timing_collector.py

# 随机策略采集
MAP=France_Massy SCENE=easy_random_perturbation python scenario_collector/collector/random_collector.py

# RL + 规则混合策略
MAP=France_Massy SCENE=easy_random_perturbation_barrier python scenario_collector/collector/rl_rule_collector.py

# MaxQ + 规则混合策略
MAP=Hongkong_YMT SCENE=normal_fluctuating_commuter_barrier python scenario_collector/collector/maxq_rule_collector.py
```

### 3D 渲染

使用 Blender 将采集的场景渲染为合成图像：

```bash
# 单场景渲染
./scenario_collector/renderers/render_single.sh --start 0 --end 600 --render_mask --render_depth

# 批量渲染
./scenario_collector/renderers/render_batch.sh --scenario <路径1> --scenario <路径2>
```

每个时间步输出：
- `high_quality_rgb/` — RGB 渲染结果
- `high_quality_mask/` — 语义分割掩码
- `high_quality_depth/` — 深度图

**渲染效果示例：**

| RGB 渲染 | 语义掩码 | 深度图 | YOLO 检测 |
|:---:|:---:|:---:|:---:|
| ![RGB](./assets/rgb.png) | ![Mask](./assets/mask.png) | ![Depth](./assets/depth.png) | ![YOLO](./assets/yolo.png) |

---

## VQA 基准测试

OmniTraffic 生成同步多视角 VQA 样本，覆盖：
- 车辆状态
- 车道功能
- 视角-BEV 对应关系
- 时序动态
- 信号相位分析

### 任务层级

| 级别 | 任务 | 描述 |
|------|------|------|
| **1** | 场景感知 | 目标检测、车道功能识别、信号相位识别 |
| **2** | 多视角与时序推理 | 视角-BEV 对应关系、时序动态跟踪 |
| **3** | 决策支持 | 交通控制决策的拓扑推理 |

### VQA 生成

OmniTraffic 利用结构化交通元数据（车辆状态、车道拓扑、信号相位），在三个任务级别上生成问答对。VQA pipeline 以渲染图像和对应的仿真数据作为输入。

---

## 文件结构

```
OmniTraffic/
├── traffic_scenarios/          # 12 个交叉口 3D 环境
│   ├── Beijing_Beihuan/
│   ├── Beijing_Beishahe/
│   ├── ...
│   ├── France_Massy/
│   └── _config/                # 共享配置
│       ├── envs/               # 环境预设
│       ├── presets/            # 场景预设
│       ├── network_routes/     # 路线定义
│       └── selector.yaml       # 场景选择器
├── scenario_collector/          # 数据采集模块
│   ├── collector/               # 采集策略
│   │   ├── rl_collector.py
│   │   ├── fixed_timing_collector.py
│   │   ├── random_collector.py
│   │   ├── rl_rule_collector.py
│   │   └── maxq_rule_collector.py
│   ├── renderers/              # Blender 渲染脚本
│   └── tools/                  # 后处理工具
├── scenario_dataset/             # 采集的数据
│   ├── simulation/              # 原始仿真数据
│   └── real_world/              # 真实世界数据
├── vqa_generate_pipeline/               # VQA 生成 pipeline
├── human_validation/            # 人工验证 Web 应用
│   └── web_app/                 # Flask Web 应用
├── TransSimHub/                 # 核心仿真引擎
├── assets/                      # 文档资源
└── docs/                       # 文档
```

---

## 快速开始

### 1. 环境配置

```bash
uv sync
```

### 2. 下载数据

从 HuggingFace 下载预处理数据集（可直接使用）：
- [OmniTraffic_Dataset](https://huggingface.co/datasets/CROHuang/Omnitraffic_Dataset) → `scenario_dataset/`
- [OmniTraffic_Benchmark](https://huggingface.co/datasets/CROHuang/OmniTraffic_Benchmark) → `vqa_generate_pipeline/`

如需自定义渲染，可从 [GitHub Releases](https://github.com/Traffic-Alpha/OmniTraffic/releases) 下载 Blender 环境文件。

从 [GitHub Releases](https://github.com/Traffic-Alpha/OmniTraffic/releases) 下载 Blender 环境文件 → `traffic_scenarios/`。

### 3. 采集新场景

```bash
MAP=<交叉口> SCENE=<场景类型> python scenario_collector/collector/<策略>_collector.py
```

### 4. 生成 VQA

参见 `vqa_generate_pipeline/` 目录下的 VQA 生成 pipeline。

---

## 引用

如果您的研究使用了 OmniTraffic，请引用我们的论文。
