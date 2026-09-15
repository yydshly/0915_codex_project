# Fireworks 图类型总结与效果展示

[打开交互展厅](../app/diagram-types.html)

## 结论

它可以表达系统结构、数据关系、消息时序、对象状态、并行活动、时间计划、概念分类和方案比较，范围超过业务流程说明。其优势在于把人工或 AI 已整理的关系制作成图。它本身不替代事实调查、源码理解或数据库建模。

本次按固定提交的文档列出 33 个展示条目：14 个主图型、UML 映射补充的 9 个视图、4 个工程视图、6 个 AI 领域变体。部分名称重叠，同义名称合并；这不是上游官方标准图型总数。

## 实现方式与产物

- 原生 JSON：15 项，作者提供节点、坐标和关系，原库通用生成器绘制。
- 按规范绘制：15 项，本次 AI 按上游记法编写 SVG，再由原库检查和导出。
- 近似适配：3 项，通信、Timing、交互概览；属于上述 AI 编写路线。
- 共 33 份 SVG、33 份 PNG、33 份离线 HTML；其中复用既有 10 项，新增 23 项。
- 每项都可查输入与程序检查。GIF 仅适用于上游限定语义场景，本页不声称全部图型支持动画。

## 完整类型清单

### 通用表达

| 类型与效果 | 用来回答什么 | 本次实现方式 |
| --- | --- | --- |
| [流程图](../app/types/flowchart.png) | 步骤如何推进？遇到条件走哪条分支？ | 按规范绘制 |
| [比较矩阵](../app/types/comparison.png) | 多个方案在哪些维度上不同？ | 按规范绘制 |
| [时间轴 / 甘特图](../app/types/timeline.png) | 每项工作持续多久、何时开始、何时交付？ | 按规范绘制 |
| [思维导图 / 概念图](../app/types/mindmap.png) | 一个主题有哪些分支与关联概念？ | 按规范绘制 |

### 系统与工程

| 类型与效果 | 用来回答什么 | 本次实现方式 |
| --- | --- | --- |
| [系统架构图](../app/types/architecture.png) | 系统由哪些服务与存储组成？ | 原生 JSON |
| [C4 评审视图](../app/types/c4.png) | 在同一抽象层级上，职责和协议是否清楚？ | 原生 JSON |
| [云部署视图](../app/types/cloud.png) | Region、VPC、工作负载与复制归属是什么？ | 原生 JSON |
| [事件流视图](../app/types/event.png) | 主题、处理器、消费组与异常出口怎样连接？ | 原生 JSON |
| [可靠性 / 可观测性视图](../app/types/observability.png) | 黄金信号、关键路径与追踪如何关联？ | 原生 JSON |
| [网络拓扑图](../app/types/network.png) | 网络设备如何连接、流量经过哪些边界？ | 原生 JSON |
| [UML 部署图](../app/types/deployment.png) | 软件制品部署到哪些运行节点？ | 按规范绘制 |

### 数据与结构

| 类型与效果 | 用来回答什么 | 本次实现方式 |
| --- | --- | --- |
| [数据流图](../app/types/dataflow.png) | 数据从哪里来，经过什么加工，保存到哪里？ | 原生 JSON |
| [ER 实体关系图](../app/types/er.png) | 数据库有哪些实体、键与一对多关系？ | 按规范绘制 |
| [对象图](../app/types/object.png) | 某个时刻有哪些实例，实例间怎样关联？ | 按规范绘制 |
| [组件图](../app/types/component.png) | 组件的职责、端口和依赖是什么？ | 按规范绘制 |
| [包图](../app/types/package.png) | 代码按哪些包组织？包之间依赖什么？ | 按规范绘制 |
| [组合结构图](../app/types/composite.png) | 一个组件内部有哪些部件、端口和连接器？ | 按规范绘制 |

### UML 与行为

| 类型与效果 | 用来回答什么 | 本次实现方式 |
| --- | --- | --- |
| [时序图](../app/types/sequence.png) | 一次请求里，谁先调用谁，谁返回什么？ | 按规范绘制 |
| [状态机图](../app/types/state.png) | 同一个订单有哪些状态？什么事件触发变化？ | 按规范绘制 |
| [类图](../app/types/class.png) | 软件有哪些类、属性、方法与关系？ | 按规范绘制 |
| [用例图](../app/types/usecase.png) | 谁可以使用系统的哪些功能？ | 按规范绘制 |
| [活动图](../app/types/activity.png) | 哪些动作可以并行？在哪里汇合？ | 按规范绘制 |
| [通信图](../app/types/communication.png) | 对象怎样互相发消息？编号顺序是什么？ | 近似适配 |
| [时序波形图（Timing）](../app/types/timing.png) | 对象状态随时间如何变化？ | 近似适配 |
| [交互概览图](../app/types/interaction-overview.png) | 多个交互片段如何按条件组织？ | 近似适配 |

### AI 与领域模式

| 类型与效果 | 用来回答什么 | 本次实现方式 |
| --- | --- | --- |
| [Agent 架构图](../app/types/agent.png) | 规划、模型、记忆、工具与评估如何协作？ | 原生 JSON |
| [记忆架构图](../app/types/memory.png) | 记忆如何写入、合并、存储和检索？ | 原生 JSON |
| [多 Agent 协作图](../app/types/multiagent.png) | 协调器如何分工、审查与汇总？ | 原生 JSON |
| [工具调用图](../app/types/toolcall.png) | 模型如何选择工具、拿回结果并继续？ | 原生 JSON |
| [Agent 记忆分类图](../app/types/memorytypes.png) | 工作、情景、语义等记忆有什么层次？ | 原生 JSON |
| [RAG 检索增强图](../app/types/rag.png) | 回答怎样引用外部资料？ | 原生 JSON |
| [Agentic RAG 图](../app/types/agentic-rag.png) | Agent 如何决定检索与补充资料？ | 原生 JSON |
| [Agentic Search 图](../app/types/agentic-search.png) | 多步搜索如何规划、执行与综合？ | 原生 JSON |

## 选择建议

- 读程序调用：时序图；理解数据库：ER 图；理解类型关系：类图。
- 排查订单状态：状态机图；解释并发步骤：活动图。
- 做部署评审：C4、云部署或 UML 部署图；梳理消息系统：事件流图。
- 安排时间：甘特图；比较方案：矩阵；整理主题：思维导图。
- Agent、RAG、记忆和工具调用图属于领域视图，很多仍使用架构或数据流记法。

## 验证边界

全部 33 项通过上游 XML、marker、碰撞、几何、构图五项通用检查；逐项检查记录在展厅可下载。该检查不能认证完整 UML 语义，也不能证明教学设定是真实业务事实。网络示例为逻辑路径，Agentic 示例仅展开资料充足时的主路径。

33 张 PNG 已通过拼图总览进行目视检查；时序图与类图修订后另行放大检查。网页通过静态链接、资源和脚本语法检查，未逐项验收原生 HTML 的浏览器交互控件。

## 固定来源

研究提交：`31fea364eda5f1852b1175f3d9e29ea31d22dcb4`。

- [图型与 UML 映射](https://github.com/yizhiyanhua-ai/fireworks-tech-graph/blob/31fea364eda5f1852b1175f3d9e29ea31d22dcb4/references/diagram-layout-reference.md)
- [风格与工程视图矩阵](https://github.com/yizhiyanhua-ai/fireworks-tech-graph/blob/31fea364eda5f1852b1175f3d9e29ea31d22dcb4/references/style-diagram-matrix.md)
- [原生通用生成器](https://github.com/yizhiyanhua-ai/fireworks-tech-graph/blob/31fea364eda5f1852b1175f3d9e29ea31d22dcb4/scripts/generate-from-template.py)
