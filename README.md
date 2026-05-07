# OmniTraffic

A controllable generation pipeline and benchmark for spatio-temporal traffic reasoning.

## Download

| Dataset | Description | Link |
|---------|-------------|------|
| OmniTraffic_Dataset | Simulation data + rendered images (scenario_dataset) | [HuggingFace](https://huggingface.co/datasets/CROHuang/Omnitraffic_Dataset) |
| OmniTraffic_Benchmark | VQA samples (vqa_benchmark) | [HuggingFace](https://huggingface.co/datasets/CROHuang/OmniTraffic_Benchmark) |
| Blender Environment Files | 3D traffic environments (`.blend`) | [GitHub Releases](https://github.com/Traffic-Alpha/OmniTraffic/releases) |

---

## Benchmark Statistics

| Metric | Value |
|--------|-------|
| Intersections | 12 real-world sites |
| Environments | Simulation + Real-world |
| VQA Samples | 8M |
| Human-verified Test Set | 3K |
| Task Hierarchy | 3 levels (Perception / Reasoning / Decision Support) |

---

## Pipeline Overview

```
traffic_scenarios (12 intersections)
    ↓
scenario_collector (5 collection strategies + events)
    ↓
scenario_dataset (simulation data + rendered images)
    ↓
vqa_benchmark (VQA generation)
```

OmniTraffic supports both **controlled** (simulation) and **natural-condition** (real-world) evaluation.

---

## Traffic Scenarios

![12 Intersections Overview](./assets/12_intersections.png)

The benchmark includes 12 real-world intersections reconstructed into editable 3D traffic environments:

| # | Location | Description |
|---|----------|-------------|
| 1 | Beijing_Beihuan | Urban intersection in Beijing |
| 2 | Beijing_Beishahe | Residential area intersection |
| 3 | Beijing_Changjianglu | Commercial district intersection |
| 4 | Beijing_Gaojiaoyuan | Suburban intersection |
| 5 | Beijing_Pinganli | Central urban intersection |
| 6 | Beijing_Yongrunlu | High-traffic corridor |
| 7 | Chengdu_Chenghannanlu | Chengdu downtown intersection |
| 8 | Chengdu_Guanghua | Technology district intersection |
| 9 | France_Massy | European urban intersection |
| 10 | Hongkong_YMT | Hong Kong urban intersection |
| 11 | SouthKorea_Songdo | Korean smart city intersection |
| 12 | Tianjin_zhijingdao | Tianjin main road intersection |

Each intersection includes:
- Editable 3D traffic environment (`.blend` file for Blender rendering)
- SUMO network definition (`.net.xml`)
- Traffic demand configuration (`.rou.xml`)
- Signal phase definitions

---

## Scenario Collector

Data collection with controlled strategies for generating diverse traffic scenarios.

### Collection Strategies

| Strategy | Description |
|----------|-------------|
| **RL** | Pure reinforcement learning signal control policy |
| **Fixed Timing** | Traditional fixed signal timing plan |
| **Random** | Random signal phase selection |
| **RL+Rule** | RL policy with rule-based overrides for special events (emergency vehicles, barriers) |
| **MaxQ+Rule** | MaxQ queuing algorithm with rule-based overrides |

### Events

Each scenario defines events via SUMO configuration files (`.sumocfg`):

| Event | Description |
|-------|-------------|
| `barrier` | Road barrier deployed |
| `crashed` | Vehicle crash incident |
| `fluctuating_commuter` | Rush-hour traffic demand fluctuation |
| `high_density` | High traffic density period |
| `low_density` | Low traffic density period |
| `increasing_demand` | Gradually increasing traffic demand |
| `random_perturbation` | Random traffic flow perturbations |

### Usage

```bash
cd /path/to/OmniTraffic

# RL policy collection
MAP=Hongkong_YMT SCENE=normal_fluctuating_commuter_barrier python scenario_collector/collector/rl_collector.py

# Fixed timing collection
MAP=France_Massy SCENE=easy_high_density_barrier python scenario_collector/collector/fixed_timing_collector.py

# Random policy collection
MAP=France_Massy SCENE=easy_random_perturbation python scenario_collector/collector/random_collector.py

# RL + Rule hybrid
MAP=France_Massy SCENE=easy_random_perturbation_barrier python scenario_collector/collector/rl_rule_collector.py

# MaxQ + Rule hybrid
MAP=Hongkong_YMT SCENE=normal_fluctuating_commuter_barrier python scenario_collector/collector/maxq_rule_collector.py
```

### 3D Rendering

Render collected scenarios with Blender for synthetic image generation:

```bash
# Single scene rendering
./scenario_collector/renderers/render_single.sh --start 0 --end 600 --render_mask --render_depth

# Batch rendering
./scenario_collector/renderers/render_batch.sh --scenario <path1> --scenario <path2>
```

Output per timestep:
- `high_quality_rgb/` — RGB rendering
- `high_quality_mask/` — Semantic segmentation mask
- `high_quality_depth/` — Depth map

**Rendering Output Examples:**

| RGB Rendering | Semantic Mask | Depth Map | YOLO Detection |
|:---:|:---:|:---:|:---:|
| ![RGB](./assets/rgb.png) | ![Mask](./assets/mask.png) | ![Depth](./assets/depth.png) | ![YOLO](./assets/yolo.png) |

---

## VQA Benchmark

OmniTraffic generates synchronized multi-view VQA samples covering:
- Vehicle states
- Lane functions
- View-BEV correspondence
- Temporal dynamics
- Signal-phase analysis

### Task Hierarchy

| Level | Task | Description |
|-------|------|-------------|
| **1** | Scene Perception | Object detection, lane function recognition, signal phase identification |
| **2** | Multi-view & Temporal Reasoning | View-BEV correspondence, temporal dynamics tracking |
| **3** | Decision Support | Topology-grounded reasoning for traffic control decisions |

### VQA Generation

Using structured traffic metadata (vehicle states, lane topology, signal phases), OmniTraffic generates question-answer pairs across all three task levels. The VQA pipeline takes rendered images and corresponding simulation data as input.

---

## File Structure

```
OmniTraffic/
├── traffic_scenarios/          # 12 intersection 3D environments
│   ├── Beijing_Beihuan/
│   ├── Beijing_Beishahe/
│   ├── ...
│   ├── France_Massy/
│   └── _config/                # Shared configuration
│       ├── envs/               # Environment presets
│       ├── presets/            # Scenario presets
│       ├── network_routes/     # Route definitions
│       └── selector.yaml       # Scenario selector
├── scenario_collector/          # Data collection module
│   ├── collector/               # Collection strategies
│   │   ├── rl_collector.py
│   │   ├── fixed_timing_collector.py
│   │   ├── random_collector.py
│   │   ├── rl_rule_collector.py
│   │   └── maxq_rule_collector.py
│   ├── renderers/              # Blender rendering scripts
│   └── tools/                  # Post-processing tools
├── scenario_dataset/             # Collected data
│   ├── simulation/              # Raw simulation data
│   └── real_world/              # Real-world data
├── vqa_generate_pipeline/               # VQA generation pipeline
├── human_validation/            # Human evaluation web app
│   └── web_app/                 # Flask web application
├── TransSimHub/                 # Core simulation engine
├── assets/                      # Documentation assets
└── docs/                       # Documentation
```

---

## Getting Started

### 1. Environment Setup

```bash
uv sync
```

### 2. Download Data

Download pre-processed datasets from HuggingFace (ready to use directly):
- [OmniTraffic_Dataset](https://huggingface.co/datasets/CROHuang/Omnitraffic_Dataset) → `scenario_dataset/`
- [OmniTraffic_Benchmark](https://huggingface.co/datasets/CROHuang/OmniTraffic_Benchmark) → `vqa_generate_pipeline/`

Only download Blender environment files from [GitHub Releases](https://github.com/Traffic-Alpha/OmniTraffic/releases) if you want to customize rendering.

Download Blender environment files from [GitHub Releases](https://github.com/Traffic-Alpha/OmniTraffic/releases) → `traffic_scenarios/`.

### 3. Collect New Scenarios

```bash
MAP=<intersection> SCENE=<scenario_type> python scenario_collector/collector/<strategy>_collector.py
```

### 4. Generate VQA

See `vqa_generate_pipeline/` for VQA generation pipeline.

---

## Citation

If you use OmniTraffic in your research, please cite our paper.
