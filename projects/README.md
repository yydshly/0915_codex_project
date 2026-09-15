# 研究子项目

实际研究项目从 `001` 开始，按编号依次增加：

```text
projects/
  001-project-slug/
    project.json     # 首页索引信息
    README.md        # 研究入口与总结
    assets/          # 截图、架构图、演示 GIF
    notes/           # 深入阅读、实验记录
    src/             # 自己编写或合法引入的实验代码
```

通过根目录说明中的新建命令生成以上结构。

## 已收录项目

| 编号 | 项目 | 能力与原理摘要 | 关联原库 |
| --- | --- | --- | --- |
| 001 | [Unique3D](001-unique3d/README.md) | 单图经扩散模型生成多视图与法线，再由 ISOMER 重建、细化并上色，导出 GLB 网格。 | [AiuniAI/Unique3D](https://github.com/AiuniAI/Unique3D) |
| 002 | [Web Starter Kit：3D 人物与舞蹈演示、接入能力](002-web-game-starter/README.md) | 已有 3D 人物模型与舞蹈动作的接入、播放和演示。当前目标参考价值有限，核心在人物与动作资产。附架构引导图与远端研究页。 | [vibegameengine/web-starter-kit](https://github.com/vibegameengine/web-starter-kit) |
| 004 | [AI 工具资料库：收集、分析与理解报告](004-ai-tool-prompts/README.md) | 收集 Manus、Kiro、Cursor、Lovable 等 AI 工具的提示词、工具说明与配置资料，供研究者解析、分析并整理成产品理解报告；对我们的实际价值仍需后续研究与验证。 | [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) |
| 005 | [Awesome Sites：3D 相关产品收集库](005-awesome-sites/README.md) | 收集 80 个 3D 相关产品及交互样例；与已有实践较多重合，保留效果、交互与实现线索参考，技术增量目前有限。 | [Awesome Sites](https://awesomesites.ai/) |
| 006 | [Huashu Report：专业报告格式整理与约束实现](006-huashu-report/README.md) | 从专业资料中梳理样式、字体、图片与图表编排、表格和分页等格式信息，形成约束与制作流程，实现相应展示效果；兼有内容组织规范，核心价值是经验整理与复用，底层技术增量有限。 | [alchaincyf/huashu-report](https://github.com/alchaincyf/huashu-report) |

- 子目录命名：三位数字编号 + 英文小写短横线名称。
- 每个项目的 `project.json` 是首页摘要和链接的来源。
- 每个项目可使用不同技术栈，在自身目录管理依赖与锁文件。
- 原始仓库如需本地克隆，放到仓库根目录的 `upstream/`；该目录已忽略。
- [完整约定](../docs/CONVENTIONS.md) · [回到总索引](../README.md)
