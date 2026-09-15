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

- 子目录命名：三位数字编号 + 英文小写短横线名称。
- 每个项目的 `project.json` 是首页摘要和链接的来源。
- 每个项目可使用不同技术栈，在自身目录管理依赖与锁文件。
- 原始仓库如需本地克隆，放到仓库根目录的 `upstream/`；该目录已忽略。
- [完整约定](../docs/CONVENTIONS.md) · [回到总索引](../README.md)
