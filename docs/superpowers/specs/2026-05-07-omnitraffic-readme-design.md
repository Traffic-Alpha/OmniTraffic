# OmniTraffic README Design Spec

## Overview

Create bilingual README documentation (English + Chinese) for the OmniTraffic repository — a controllable generation pipeline and benchmark for spatio-temporal traffic reasoning.

## Design Decision

**Approach A (Selected)**: Single README per language (README.md + README_zh.md), unified structure with links at the top.

**Why**: Readers typically choose one language; centralized files easier to maintain.

## Content Structure

### File 1: README.md (English)
### File 2: README_zh.md (Chinese)

Both files share the same structure:

---

### Section 1: Title & Links (Top of Page)
- Project name: **OmniTraffic**
- One-line description
- HuggingFace download links:
  - Omnitraffic_Dataset: https://huggingface.co/datasets/CROHuang/Omnitraffic_Dataset
  - OmniTraffic_Benchmark: https://huggingface.co/datasets/CROHuang/OmniTraffic_Benchmark
- ArXiv paper link: [placeholder — to be added]

### Section 2: Benchmark Statistics
Key numbers in card/table format:
- 12 real-world intersections
- Simulation + Real-world environments
- 8M VQA samples
- 3K human-verified test set
- 3-tier task hierarchy

### Section 3: Pipeline Overview
Text + ASCII flow diagram:
```
traffic_scenarios (12 intersections)
    ↓
scenario_collector (5 collection strategies + events)
    ↓
scenario_dataset (simulation data + rendered images)
    ↓
vqa_benchmark (VQA generation)
```

### Section 4: Traffic Scenarios
List of 12 intersections with brief description:
1. Beijing_Beihuan
2. Beijing_Beishahe
3. Beijing_Changjianglu
4. Beijing_Gaojiaoyuan
5. Beijing_Pinganli
6. Beijing_Yongrunlu
7. Chengdu_Chenghannanlu
8. Chengdu_Guanghua
9. France_Massy
10. Hongkong_YMT
11. SouthKorea_Songdo
12. Tianjin_zhijingdao

Brief intro + instruction to view images elsewhere.

### Section 5: Scenario Collector
#### 5.1 Collection Strategies (5 types)
| Strategy | Description |
|----------|-------------|
| RL | Pure reinforcement learning policy |
| Fixed Timing | Fixed signal timing |
| Random | Random policy |
| RL+Rule | RL with rule-based overrides (emergency vehicles, barriers) |
| MaxQ+Rule | MaxQ queuing + rule-based overrides |

#### 5.2 Events
Defined in each scenario's sumocfg files:
- barrier: Road barrier event
- crashed: Vehicle crash event
- fluctuating_commuter: Traffic demand fluctuation
- high_density: High traffic density
- low_density: Low traffic density
- increasing_demand: Gradually increasing demand
- random_perturbation: Random traffic perturbations

### Section 6: VQA Benchmark
#### 6.1 Task Hierarchy (3 levels)
- **Level 1: Scene Perception** — object detection, lane function, signal phase
- **Level 2: Multi-view & Temporal Reasoning** — view-BEV correspondence, temporal dynamics
- **Level 3: Decision Support** — topology-grounded reasoning

#### 6.2 VQA Generation
Brief description of how VQA samples are generated from structured traffic metadata.

### Section 7: File Structure
Directory tree of the repository:
```
OmniTraffic/
├── traffic_scenarios/     # 12 intersection 3D environments
├── scenario_collector/    # Data collection with different strategies
├── scenario_dataset/      # Collected simulation + rendered data
├── vqa_benchmark/         # VQA generation pipeline
├── human_validation/      # Human evaluation web app
├── TransSimHub/          # Core simulation engine
└── docs/                 # Documentation
```

### Section 8: Getting Started
Minimal quick-start commands:
1. Environment setup (uv)
2. Data download (HuggingFace)
3. Run scenario collector
4. Generate VQA

---

## Language Conventions

- **English README**: English headings, English prose
- **Chinese README**: 中文标题, Chinese prose
- Code blocks, commands, technical terms: Keep in English

## Acceptance Criteria

1. Both README files exist and are well-structured
2. All 8 sections present in both languages
3. HuggingFace links correctly placed at top
4. ArXiv link placeholder clearly marked for user to fill
5. Pipeline flow diagram is clear
6. All 12 scenarios listed
7. All 5 collection strategies explained
8. Task hierarchy (3 levels) clearly described
9. File structure matches actual repository
