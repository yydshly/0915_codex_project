# 静态 Web 发布目录

研究静态站点的构建目录。源码在各子项目的 `app/`，此处生成页面与所需图片，不提交重复构建产物。Unique3D 网页与已确认的引导图已发布至 GitHub Pages，2026-09-15 完成线上验证。

运行 `python scripts/build_web.py` 生成导航首页及子页面，运行 `python scripts/check_web.py` 检查本地链接、锚点和图片说明。Unique3D 路径为 `web/001-unique3d/`；发布工作流位于 `.github/workflows/pages.yml`。

详见 [Web 演示接入说明](../docs/WEB_DEMOS.md)。
