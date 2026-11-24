# Tier 1.1 — 单图直接视觉反驳数据集（`tier1.1-125-v1.1`）

## 简介
本层测试多模态大模型最基础的**“眼见为实”抗压能力**：给模型 1 张真实图片和 1 个视觉问题，同时施加来自用户的错误引导（直接施压、权威口吻、伪造引用、现场目击等），观察模型能否坚持图片事实、直接反驳用户。

## 数据规模
- **题目总数**：**125 题**（125 张完全不重复的真实图片，与 Tier 1.2 零重合）
- **领域分布**：
  - 日常生活（`daily_life` / RealworldQA）：50 题
  - 医疗影像（`medical` / SLAKE）：50 题
  - 图表数据（`chart_data` / ChartQAPro）：25 题
- **条件设置**：
  - 原始 3 条件：`neutral`（无引导）、`syco_pressure`（错误施压）、`valid_feedback`（正确反馈对照）
  - 跨层对齐 5 条件（`benchmark_1_1_aligned.json`）：补齐 `N_neutral`、`S1_wrong_pressure_orig`、`S2_wrong_draft_confirm`、`S3_wrong_authority_nudge`、`C_valid_feedback`，并统一 `canonical_domain`、`source_group`、`source_cluster_id`、`image_sha256`。

## 目录结构
```text
dataset_1_1/
├── README.md                    # 本说明文档
├── benchmark_1_1_aligned.json   # 【推荐】与 Tier 1.2/1.3 对齐后的 125 题主数据
├── benchmark_1_1.json           # 原始 125 题数据（完整保留）
├── tier_1_1_manifest.json       # 清单与统计信息
├── images/                      # 125 张真实图片（按领域分目录）
├── code/                        # 对齐与校验脚本（align_tier11.py 等）
├── provenance/                  # 图片来源与溯源记录
├── medical_annotations/         # 医疗题标注参考
├── SHA256SUMS                   # 图片与文件哈希校验
└── validation.json              # 质检报告
```
