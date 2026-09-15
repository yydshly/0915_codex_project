# GitHub 项目研究笔记

记录值得深入研究的开源项目：理解设计、运行验证、动手改造，并沉淀可复用的结论。

这里是研究总仓库。首页只保留项目摘要、顺序索引、预览图和演示入口；源码实验、运行方法和研究笔记收纳在各子项目中。

## 项目索引

按三位数字编号升序排列。编号分配后保持不变，不因完成、暂停或归档而重新编号。

<!-- PROJECT_INDEX:START -->
| 编号 | 项目 | 摘要 | 状态 | 上游 | 演示 |
| --- | --- | --- | --- | --- | --- |
| 001 | [Unique3D：从一张图片到三维网格](projects/001-unique3d/README.md) | 单张物体图片经预训练扩散模型生成多视图与法线，再由 ISOMER 重建、细化并上色，导出 GLB 网格；整理模型与算法分工、效果边界及三维技术路线对比。 | 已总结 | [GitHub](https://github.com/AiuniAI/Unique3D) | [在线演示](https://yydshly.github.io/0915_codex_project/001-unique3d/) |
<!-- PROJECT_INDEX:END -->

## 项目预览

<!-- PROJECT_CARDS:START -->
### 001 · Unique3D：从一张图片到三维网格

单张物体图片经预训练扩散模型生成多视图与法线，再由 ISOMER 重建、细化并上色，导出 GLB 网格；整理模型与算法分工、效果边界及三维技术路线对比。

![Unique3D：从一张图片到三维网格预览](projects/001-unique3d/assets/architecture-guide.png)

[研究笔记](projects/001-unique3d/README.md) · [GitHub](https://github.com/AiuniAI/Unique3D) · [在线演示](https://yydshly.github.io/0915_codex_project/001-unique3d/)

状态：已总结 · 标签：图生3D / 扩散模型 / 几何重建 / 研究网页
<!-- PROJECT_CARDS:END -->

## 新增研究项目

需要 Python 3.10 或以上版本，无需安装第三方依赖。在仓库根目录运行：

```sh
python scripts/projects.py new sample-project --title "示例项目" --upstream https://github.com/owner/repo --summary "用一句话说明它解决什么问题，以及为什么值得研究。"
```

命令会自动分配下一个编号、创建研究目录并更新首页。上面的名称与链接仅为使用示例，请替换为实际项目。

1. 完善子项目的 `README.md`，记录上游版本、运行方法和研究结论。
2. 将截图放到子项目的 `assets/`，在 `project.json` 的 `cover` 中填写相对路径，例如 `assets/cover.png`。
3. 修改摘要、状态或演示链接后，运行 `python scripts/projects.py sync` 更新首页。
4. 提交前运行 `python scripts/projects.py check`，检查元数据和首页是否一致。

## 目录导航

| 位置 | 内容 |
| --- | --- |
| [projects/](projects/) | 按编号管理的研究子项目 |
| [templates/project/](templates/project/) | 统一的研究记录和截图模板 |
| [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | 编号、状态、截图与源码管理约定 |
| [docs/WEB_DEMOS.md](docs/WEB_DEMOS.md) | 多个 Web 演示的路径和发布方案 |
| [web/](web/) | 未来统一发布的静态 Web 目录 |
| [scripts/](scripts/) | 新建项目与同步索引工具 |

## 研究方式

**收录 → 阅读 → 复现 → 实验 → 总结**

每个子项目独立管理运行环境和依赖。记录上游仓库、许可证与研究使用的版本；引用或修改第三方代码时保留原有许可与署名。

已收录 Unique3D 研究，完成能力摘要、实现原理、路线对比和网页。引导图已于 2026-09-15 获用户确认，网页已部署至 GitHub Pages，线上页面、图片与交互验证通过。
