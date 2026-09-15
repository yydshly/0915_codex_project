# 001 · Unique3D：从一张图片到三维网格

**能力与原理摘要：**单张物体图片经预训练图像扩散模型生成多视图和表面法线，再由 ISOMER 算法重建、细化与上色，输出带顶点颜色的 GLB 网格。适合快速制作资产初稿，隐藏区域来自推测，不能当作精确测量。

[返回总索引](../../README.md) · [关联原库 AiuniAI/Unique3D](https://github.com/AiuniAI/Unique3D) · [完整理解](notes/research.md) · [网页源码](app/index.html) · [在线阅读](https://yydshly.github.io/0915_codex_project/001-unique3d/)

## 架构与效果引导图

![单图入口、预训练模型、ISOMER 算法、GLB 出口与应用示意](assets/architecture-guide.png)

图为内置 image_gen 生成的架构与效果示意，非 Unique3D 本机实测结果。**图片已于 2026-09-15 获用户确认。** [完整绘图提示词](assets/guide-prompt.txt) · [图片来源](assets/README.md)

## 研究信息

| 项目 | 内容 |
| --- | --- |
| 原始仓库 | [AiuniAI/Unique3D](https://github.com/AiuniAI/Unique3D) |
| 论文 | [NeurIPS 2024 · Unique3D](https://arxiv.org/abs/2405.20343) |
| 上游快照 | `6311af200ee197544e82e0f2557cd890edd60416`，2026-09-15 查询 |
| 上游代码许可 | MIT；模型、数据与第三方素材许可独立 |
| 本次范围 | 阅读与源码分析、静态研究网页、引导图 |
| 推理验证 | 未安装上游环境、未加载权重、未进行本机生成或性能测试 |
| 发布状态 | 已发布至 GitHub Pages，2026-09-15 线上验证通过 |

## 网页内容

能力摘要、高清引导图、五阶段交互流程、模型与算法分工、官方效果入口、输入输出边界、六类路线对比、扩展方向、常见问题和来源。默认导出使用顶点颜色；网页没有运行 Unique3D 生成后端。

## 本地预览

在研究仓库根目录执行：

```sh
python scripts/projects.py sync
python scripts/projects.py check
python scripts/build_web.py
python scripts/check_web.py
python -m http.server 8155 --bind 127.0.0.1 --directory web
```

访问 `http://127.0.0.1:8155/001-unique3d/`。统一发布目录为 `web/`，Pages 工作流随本次提交启用。正式路径为仓库 Pages 的 `/001-unique3d/`；线上验证通过后已填写 `demo_url`。

## 下一步

先以雕像、花盆、卡通摆件进行同输入验证，再做资产减面、颜色烘焙、批量生成与质量检测；多图约束和领域训练属于进一步开发。详见[完整研究](notes/research.md)。
