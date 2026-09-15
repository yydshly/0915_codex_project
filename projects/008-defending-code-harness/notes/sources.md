# 来源与核对记录

## 版本与范围

- 整理日期：2026-09-15。
- 上游：Anthropic 的 [defending-code-reference-harness](https://github.com/anthropics/defending-code-reference-harness)。
- 固定提交：`d3bea6b5793b5f3d59a75ebe69a58efa88383145`。
- 本次进行了文档和核心源码阅读；未执行上游程序或基准测试。
- 本子项目是中文归纳和设计分析，没有复制上游实现或模型权重。
- 下列链接均固定到研究提交，避免后续主分支变化影响核对。

## 源码与文档导航

| 来源 | 对应内容 |
| --- | --- |
| [能力与定位](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/README.md) | 交互技能、自动流水线、C/C++ 默认范围、维护状态 |
| [许可证](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/LICENSE) | Apache-2.0 |
| [依赖与入口](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/pyproject.toml) | Python 3.11+、命令入口 |
| [静态扫描](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/.claude/skills/vuln-scan/SKILL.md) | 只读源码推理，不构建运行目标 |
| [威胁模型](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/docs/threat-model.md) | 资产、入口、边界与部署上下文 |
| [分诊](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/docs/triage.md) | 源码核实、跨轮次去重、严重性调整和负责人标注 |
| [模型调用](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/agent.py) | Claude Code CLI、默认工具、消息解析、会话恢复 |
| [调度](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/cli.py) | 阶段调用、并行任务、检查点和流式报告 |
| [沙箱](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/sandbox.py) | 阶段容器、gVisor 与网络出口约束 |
| [目标配置](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/targets/drlibs/config.yaml) | 源码位置、运行程序、构建命令与攻击面 |
| [完整流水线](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/docs/pipeline.md) | 阶段条件、去重、报告与恢复 |
| [发现实现](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/find.py) | 容器内研究、PoC 和结构化字段提取 |
| [验证实现](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/grade.py) | 新容器、PoC 复制、复现元数据和模型判定解析 |
| [验证规则](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/prompts/grade_prompt.py) | 五项标准、重复运行与不可信声明 |
| [ASAN 解析](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/asan.py) | 崩溃类型、项目堆栈与摘要提取 |
| [补丁验收](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/patch_grade.py) | 直接执行 T0–T2、再次攻击和可选风格评分 |
| [补丁机制](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/docs/patching.md) | 有限预算、测试缺失时跳过与人工审查边界 |
| [适配方法](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/docs/customizing.md) | 替换语言、检测器、输入形式与验收标准 |
| [检测与响应](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/docs/detection-response.md) | 合成日志目标、独立评分和响应范围 |

## 哪些结论属于研究建议

网页深化时补充阅读：

- [Find 提示词](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/prompts/find_prompt.py)：输入构造、质量分级、最小化与排除项。
- [目标接入要求](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/targets/README.md)：配置、构建和入口封装约定。
- [配置加载器](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/harness/config.py)：字段定义与可选测试命令。
- [定制技能](https://github.com/anthropics/defending-code-reference-harness/blob/d3bea6b5793b5f3d59a75ebe69a58efa88383145/.claude/skills/customize/SKILL.md)：迁移步骤、文件映射与 canary 校准。此处作为研究对象阅读，并未执行技能或适配上游。

[复用思路](reuse.md)中的跨模型适配清单、优惠券业务测试示例和后续实验步骤，是根据上述设计提出的建议，未作为已实现功能或上游实测结论。

## 验证边界

已核对调用层使用 Claude Code、Find 与 Grade 的环境分离、验证提示的重复运行要求、补丁前三级的直接执行检查。未验证实际发现率、误报率、模型间效果、资源成本或沙箱部署效果。
