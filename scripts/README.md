# 项目索引工具

需要 Python 3.10+，仅使用标准库。可从任意工作目录调用脚本；它会定位脚本所在的仓库。

```sh
python scripts/projects.py new sample-project --title "示例项目" --upstream https://github.com/owner/repo --summary "项目的一句话摘要"
python scripts/projects.py sync
python scripts/projects.py check
```

- `new`：复制模板，分配编号并同步首页。不会自动下载上游代码。
- `sync`：校验元数据，按编号更新根 README 的索引和预览区。
- `check`：只检查，不写文件；数据错误或首页需要同步时返回非零退出码。

索引显示名和摘要按纯文本处理；图片必须存在于对应项目内。`cover` 与 `demo_url` 可留空。
