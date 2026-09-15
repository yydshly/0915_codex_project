# 能力、历史对照与价值分析

## 1. 定位与能力

Fireworks 是 Agent Skill 与绘图 CLI 的组合。SKILL 和 references 指导宿主 AI 理解图类型、内容和风格；Python 脚本接收结构化 JSON 或 SVG，生成、检查与导出。自然语言理解依赖宿主 AI，而非仓库中的独立模型服务。

固定提交提供 11 个 JSON 风格生成器配置与 1 个 AI 编写 Dark Luxury SVG 路径。通用技术图指导覆盖架构、流程、时序、类、ER 及 Agent/RAG/记忆等领域。本研究按文档整理 33 个图型与领域条目并提供实际效果；15 项由原生 JSON 生成，18 项由 AI 按规范绘制后导出（含 3 项近似适配）。[完整盘点](diagram-types.md)。README 将部分图型统称完整 UML 支持，其中混列 ER；本研究不将宣传表述或通用检查当作 UML 标准一致性证明。

## 2. 技术原理

1. **外部事实和描述**：用户提供，或 Agent 阅读有来源资料，选择节点、关系、位置和分组。
2. **JSON / IR**：`diagram_ir.py` 使用 NodeIR、EdgeIR、DiagramIR 统一数据，兼容旧输入，拒绝重复 ID、悬空引用、非有限坐标与非法路径点。
3. **工程语义检查**：`semantic_contracts.py` 对 C4、云、事件、可观测性设定规则。例如每个观测服务要求 latency、traffic、errors、saturation，且需要观察窗口与连续关键链路。
4. **几何与路由**：`generate-from-template.py` 读取节点位置，按端口、障碍物和走廊提示生成正交路线；必要时在可见性网格上用优先队列搜索。距离、弯折、交叉和重叠增加路径代价。
5. **构图与 SVG**：应用主题、形状、语义箭头、标题与图例。showcase 配置约束交叉、弯折、节点间距、容器留白和标签净空，无法满足时需调整位置或拆图。
6. **校验与视觉检查**：`validate_svg.py` 检查 XML、marker、碰撞、几何和构图。文字宽度只是启发式估算，实际 PNG 的字体、截断和可读性仍需查看。
7. **交付**：SVG 为规范产物；CairoSVG/librsvg 或 Chromium 导出 PNG；`interactive_html.py` 提供离线查看器。GIF 由受支持语义场景经过 Chromium/Puppeteer 逐帧渲染及 FFmpeg/FFprobe 编码与验证。

自动路由不等于全图自动布局，不保证任意密集关系都有零交叉表达。GIF 有角色、顺序、阶段、路径与场景约束，任意同风格 SVG 不一定可动画化。工程规则检查也不能证明业务事实真实。

## 3. 以前确实研究过的项目

### Archify：最直接的同类

证据是 `0909_codex_project/projects/003-archify/README.md` 与 `web/receipts/`。研究版本为 2.17.0-dev.1 / `1072200`。已经完成：

- 架构、工作流、时序、数据流、生命周期五类图与架构模型差异；
- 研究仓库架构，以及 Archify 自身五类中文图；
- 固定提交中的源码定位；
- 搜索、上下游、有向路径追踪和章节讲解；
- 多格式导出、输入损坏时保留旧预览的实验。

Archify 同样需要作者/Agent 整理事实与 JSON。模型差异比较两个已提供规格，不能理解成自动解读 Git diff；源码链接有效也不等于全部架构语义已有证明。

### Graphify：关系提取与查询

证据是 `0911_codex_project/projects/009-graphify/README.md` 与 `app/dist/native/fastapi/receipt.json`。研究版本为 0.9.57 / `3f82bf7`。当时分析 FastAPI 核心包 48 个 Python 文件，得到 747 节点、1,971 关系、46 社区，模型 token 为 0。代码通过 tree-sitter/AST 提取关系；多模态资料语义抽取需要其他依赖或模型。

已有网络、树、调用流程、报告、Wiki 和多格式导出，另验证 Query/Explain/Path/Affected、MCP 与小型增量更新。这些是历史结果，本次没有重跑 Graphify。静态关系并非实际运行轨迹，社区也不是人工确认业务模块。

### Lieflat Charts：相邻的可视化路线

Archify 历史研究还关联 0902 的 Lieflat Charts，侧重数据图表和报告，与系统关系绘图属于不同任务。本次主要核对 Archify 与 Graphify，没有重新验证 Lieflat 的全部能力。

## 4. 差异

| 维度 | Fireworks | Archify | Graphify |
| --- | --- | --- | --- |
| 核心责任 | 语义风格、SVG 绘制与图片质量 | 系统设计图与交互阅读 | 从资料提取关系、建图和查询 |
| 事实来源 | 用户 / AI 提供 | 用户 / AI 提供 | 从受支持输入抽取，包含推断 |
| 视觉重点 | 12 风格，工程图领域规则 | 四预设 × 深浅色、五类图与模型差异 | 关系网络与结构分析视图 |
| 阅读方式 | 平移、缩放、主题、导出 | 搜索、聚焦、上下游、路径、章节 | 查询相关子图与图算法分析 |
| 变更能力 | 本次未见模型差异功能 | 比较两个已提供架构模型 | 增量更新提取图谱 |
| 适合交付 | README、文章、方案、演示配图 | 系统导览、评审与团队交接 | 源码导航、资料关系、Agent 上下文 |

比较针对固定研究版本，不是对最新版本能力缺失的断言。美观与可控性、交互说明能力、关系提取能力是不同评价轴，不宜给出统一排名。

## 5. 对我们的价值

### 可立即利用

- **统一研究配图**：各子项目都要解释能力与原理，复用风格规则与 SVG 可降低重复排版工作。
- **质量要求可检查**：交叉、遮挡、边界、文字不全及工程字段缺失可由程序发现。
- **保留生成证据**：输入、固定版本、结果、检查报告一起保存，便于复查与修改。
- **补充已有工具**：图片表达选 Fireworks；交互追踪与模型差异选 Archify；提取关系选 Graphify。

### 尚待实现与验证

- Graphify 提取的关系经 Agent 筛选后生成 Fireworks 聚焦图；需要实体映射、来源保留、关系类型转换和确认，不能直接全量塞入。
- 从同一份经过核验的事实模型生成架构、部署、事件与运维多视图。
- 接入研究仓库构建流程，由输入变更触发重绘和失败报告。

上述组合没有接通。商业上可探索技术文档交付或内嵌导出能力，但本次没有客户需求、付费意愿、量化效率或成本收益数据。

## 6. 后续如何判断是否值得替换旧方案？

选择同一套有来源系统事实，分别用 Fireworks、Archify 生成架构与工作流。记录事实整理时间、首次可读时间、修正次数、文字完整性、导出质量与修改后的维护成本，再让实际读者完成定位组件、追踪请求等任务。本次同结构实验只验证风格与生成稳定性，没有完成跨项目效率评测。

## 来源

- [Fireworks 固定源码](https://github.com/yizhiyanhua-ai/fireworks-tech-graph/tree/31fea364eda5f1852b1175f3d9e29ea31d22dcb4)
- [Archify 既有研究](https://yydshly.github.io/0909_codex_project/projects/003-archify/)
- [Archify 固定源码](https://github.com/tt-a1i/archify/tree/10722002bb8777ecb639d93c49586fae4adf3ae4)
- [Graphify 既有研究](https://yydshly.github.io/0911_codex_project/009-graphify/)
- [Graphify 固定源码](https://github.com/Graphify-Labs/graphify/tree/3f82bf7f837a07fb0f7668fbdbd5662801906942)
