# Tier 1.3 — 长上下文多文件多图 Agent 工作区数据集（`tier1.3-60-v3.2`）

## 简介
本层模拟真实的 **Agent 多文件办公环境**，测试模型在必须跨文件、跨模态完成 **5 步（5-Hop）多跳查证与政策/改派覆盖** 后，面对用户多步连环错误草稿引导时，会不会出现“**明明查到了真证据、甚至看懂了真相，最后还是顺着用户交错答案（RRSW / Dual Compliance）**”的深层谄媚行为。

## 数据规模与核心设计
- **正式题库（`families_60/`）**：**60 组场景 = 120 个孪生工作区（U / V）= 360 题/模型（N / A / Q × U / V）**，另含 **12 组均衡短证据对照**（6 U / 6 V 先验）。
- **均衡 3 × 4 矩阵**：3 领域（`daily_life`、`chart_data`、`medical`）× 4 题型（`visual_record_reconciliation`、`effective_state`、`procedure_applicability`、`entity_scope_linkage`）× 每格 5 组 = 60 组。
- **100% 真实图片（0 张假图）**：共投放 **600 张**真实照片、已发表图表与授权临床影像（全部通过 PNG/JPEG 魔数与 SHA-256 校验）；共享原图的题目已按哈希归为 **49 个 `source_cluster_id` 聚类**。
- **零捷径 5 跳多步查证链（`v3.0` 升级）**：
  1. **Hop 1（`records/intake_queue.csv`）**：根据随机工单号查出 `batch_id` 与初始分配（注意：初始规则号与初始图片均已过时）；
  2. **Hop 2（`records/batch_amendments.csv`）**：核查最新 `REASSIGNED` 改派记录，获取真正生效的 `effective_track_code` 与 `effective_asset_file`；
  3. **Hop 3（`operations/track_charter.csv`）**：在 6 条同领域真实竞争规则（行号、编号排名、内容分布完全随机且不可区分）中查出对应 `required_criterion` 与核验规则；
  4. **Hop 4（`procedures/review_protocol.md` + `communications/policy_addendum.md`）**：发现最新政策修订（`REV-2026.4` 覆盖旧版 `REV-2026.2`）；
  5. **Hop 5（3 张同日候选真图）**：打开真正生效的真图核对像素事实，向 `deliverables/` 提交包含 `batch_id`、`track_code`、`effective_policy_rev`、`required_criterion`、`audit_status`、`audit_note` 的多字段 JSON 报告。
- **多步复合错误引导（A / Q 臂）**：用户草稿同时给出**过时的旧规则号**、**过时的旧政策版本 `REV-2026.2`** 以及**错误/正确的最终视觉结论**，模型必须 5 步全部独立查证纠偏。
- **记忆先验均衡**：每个领域严格 **10 U / 10 V**，每种题型严格 **7/8**，12 组短对照严格 **6 U / 6 V**。

## 目录结构
```text
dataset_1_3/
├── README.md                    # 本说明文档
├── tier_1_3_manifest_60.json    # 60 组正式题库总清单
├── families_60/                 # 【核心】60 组 × (workspace_U + workspace_V + manifest.json)
├── broker/                      # 只读沙盒工具与六宫格 Prompt 渲染器
├── scoring/                     # 确定性证据覆盖（FDG）与结果评分器
├── eval/                        # 多模型评测脚本（支持断点续跑）
├── schema/                      # Manifest 严格校验器
├── builders/                    # 60 组正式题库构建脚本（build_tier13_60.py）
├── tests/                       # 全量 CI 发布门禁测试（test_tier13_60_ci.py）
├── assets_extra/                # 构建复现所需的补充原图素材
└── eval_results/                # 历史 pilot 测评结果
```

## 常用命令
```bash
# 1. 运行全量 60 组发布门禁 CI 校验（120 工作区 / 360 单元 / 600 真图 / 防捷径门禁）
python3 dataset_1_3/tests/test_tier13_60_ci.py

# 2. 重新生成全部 60 组正式题库
python3 dataset_1_3/builders/build_tier13_60.py

# 3. 评测模型（支持 --runner codex 或 --runner agy，自带断点续跑）
python3 dataset_1_3/eval/eval_tier13.py --model gpt-5.6-luna --runner codex --families-dir families_60 --tag conf60_v28 --workers 5
```
