# 多项目 Web 演示

## 发布结构

GitHub Pages 每个仓库提供一个站点。多个静态应用可以发布到该站点的不同子路径：

```text
https://yydshly.github.io/0915_codex_project/
https://yydshly.github.io/0915_codex_project/001-project-slug/
https://yydshly.github.io/0915_codex_project/002-project-slug/
```

这些地址仅说明未来的路径约定，当前尚未部署。

源码保留在各研究子项目中；发布时汇总需要公开的静态内容：

```text
web/
  index.html                 # 将来添加的站点导航首页
  001-project-slug/           # 第一个应用构建后的静态文件
    index.html
  002-project-slug/           # 第二个应用构建后的静态文件
    index.html
```

## 首次接入步骤

1. 在子项目中实现并验证 Web 演示，记录其构建命令和依赖版本。
2. 将应用的资源基础路径配置为 `/0915_codex_project/<编号-名称>/`。简单静态页面也可使用相对资源路径。
3. 为单页应用使用 hash 路由，或提供经验证的静态路由方案，避免刷新子页面时出现 404。
4. 在构建流程中将各应用的发布产物汇总到 `web/<编号-名称>/`，添加 `web/index.html` 作为导航。不要直接发布整个研究仓库。
5. 在仓库 Settings → Pages 选择 GitHub Actions，按官方文档添加构建、上传 Pages 产物和部署流程；上传目录设为 `web/`。
6. 验证线上地址、图片和刷新行为，随后填写对应 `project.json` 的 `demo_url` 并同步首页。

暂时只预留目录与规范。等首个应用的技术栈确定后再接入真实构建和部署流程，避免创建没有应用可发布的工作流。

## 运行范围

GitHub Pages 托管 HTML、CSS、JavaScript 等静态文件，不运行 Python、Node.js 服务或数据库。需要后端的研究项目应将服务部署到合适的平台，在子项目文档中说明配置，并将实际演示链接填入 `demo_url`。

## 官方参考

- [GitHub Pages 的站点类型与限制](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [使用 GitHub Actions 发布 Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
