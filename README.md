# GitHub 项目研究笔记

记录值得深入研究的开源项目：理解设计、运行验证、动手改造，并沉淀可复用的结论。

这里是研究总仓库。首页只保留项目摘要、顺序索引、预览图和演示入口；源码实验、运行方法和研究笔记收纳在各子项目中。

## 项目索引

按三位数字编号升序排列。编号分配后保持不变，不因完成、暂停或归档而重新编号。

<!-- PROJECT_INDEX:START -->
暂未收录项目。第一个研究项目将从 **001** 开始。
<!-- PROJECT_INDEX:END -->

## 项目预览

<!-- PROJECT_CARDS:START -->
收录项目后，此处将展示每个项目的一句话摘要、预览图和研究入口。
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

当前处于仓库初始化阶段，尚未收录实际项目或发布 Web 演示。
