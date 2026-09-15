#!/usr/bin/env python3
"""Create numbered research projects and keep the root README in sync."""

import argparse
import html
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"待研究", "研究中", "已复现", "已总结", "已归档"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
FIELDS = {"id", "slug", "title", "summary", "upstream", "status", "tags", "cover", "demo_url"}


def https_url(value):
    parsed = urlsplit(value)
    return (parsed.scheme == "https" and bool(parsed.hostname)
            and not parsed.username and not parsed.password
            and not any(c.isspace() or ord(c) < 32 for c in value)
            and "\\" not in value)


def validate(data, directory):
    if not isinstance(data, dict) or set(data) != FIELDS:
        raise ValueError(f"{directory.name}: project.json 字段须与模板一致")
    for key in FIELDS - {"tags"}:
        if not isinstance(data[key], str):
            raise ValueError(f"{directory.name}: {key} 必须是字符串")
        if data[key] != data[key].strip() or any(ord(c) < 32 for c in data[key]):
            raise ValueError(f"{directory.name}: {key} 不能包含控制字符或首尾空白")
    if not re.fullmatch(r"[0-9]{3}", data["id"]) or data["id"] == "000":
        raise ValueError(f"{directory.name}: id 必须在 001–999 之间")
    if not SLUG.fullmatch(data["slug"]):
        raise ValueError(f"{directory.name}: slug 必须使用小写英文、数字和短横线")
    if directory.name != f'{data["id"]}-{data["slug"]}':
        raise ValueError(f"{directory.name}: 目录名与 id、slug 不一致")
    if not data["title"] or not data["summary"]:
        raise ValueError(f"{directory.name}: title 和 summary 不能为空")
    if data["status"] not in STATUSES:
        raise ValueError(f"{directory.name}: 不支持的研究状态")
    if not isinstance(data["tags"], list) or any(
        not isinstance(tag, str) or not tag.strip() for tag in data["tags"]
    ):
        raise ValueError(f"{directory.name}: tags 必须是非空字符串组成的数组")
    if not https_url(data["upstream"]) or (data["demo_url"] and not https_url(data["demo_url"])):
        raise ValueError(f"{directory.name}: 上游与演示地址必须是完整 HTTPS 链接")
    if data["cover"]:
        relative = Path(data["cover"])
        cover = (directory / relative).resolve()
        if (relative.is_absolute() or "\\" in data["cover"]
                or not cover.is_relative_to(directory.resolve()) or not cover.is_file()
                or cover.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}):
            raise ValueError(f"{directory.name}: cover 必须指向项目内已有的图片文件")


def projects():
    result = []
    seen = set()
    for directory in sorted((ROOT / "projects").iterdir()):
        if not directory.is_dir():
            continue
        if directory.is_symlink():
            raise ValueError(f"{directory.name}: 项目目录不能使用符号链接")
        metadata = directory / "project.json"
        if not metadata.is_file() or not (directory / "README.md").is_file():
            raise ValueError(f"{directory.name}: 缺少 project.json 或 README.md")
        data = json.loads(metadata.read_text(encoding="utf-8"))
        validate(data, directory)
        if data["id"] in seen:
            raise ValueError(f'重复的项目编号: {data["id"]}')
        seen.add(data["id"])
        result.append(data)
    return sorted(result, key=lambda item: int(item["id"]))


def plain(value):
    value = html.escape(" ".join(value.split()), quote=False)
    return re.sub(r"([\\`*_{\[\]}()#+.!|~-])", r"\\\1", value)


def link(label, url):
    return f'[{plain(label)}]({quote(url, safe="/:#?=&%+@,;~-")})'


def upstream_label(url):
    """Use the original repository name; use the host for non-repository sources."""
    parsed = urlsplit(url)
    parts = [part for part in parsed.path.split('/') if part]
    if parsed.hostname == "github.com" and len(parts) >= 2:
        return unquote(parts[1]).removesuffix(".git")
    return parsed.hostname or url


def sections(items):
    if not items:
        return ("暂未收录项目。第一个研究项目将从 **001** 开始。",
                "收录项目后，此处将展示每个项目的一句话摘要、预览图和研究入口。")
    rows = ["| 编号 | 项目 | 摘要 | 状态 | 上游 | 演示 |",
            "| --- | --- | --- | --- | --- | --- |"]
    cards = []
    for item in items:
        folder = f'projects/{item["id"]}-{item["slug"]}'
        research = link(item["title"], f"{folder}/README.md")
        upstream = link(upstream_label(item["upstream"]), item["upstream"])
        demo = link("在线演示", item["demo_url"]) if item["demo_url"] else "暂未部署"
        rows.append(f'| {item["id"]} | {research} | {plain(item["summary"])} | '
                    f'{item["status"]} | {upstream} | {demo} |')
        card = [f'### {item["id"]} · {plain(item["title"])}', "", plain(item["summary"]), ""]
        if item["cover"]:
            card += ["!" + link(f'{item["title"]}预览', f'{folder}/{item["cover"]}'), ""]
        else:
            card += ["*截图待补充。*", ""]
        card += [f'{link("研究笔记", f"{folder}/README.md")} · {upstream} · {demo}', "",
                 f'状态：{item["status"]}' +
                 (" · 标签：" + " / ".join(plain(tag) for tag in item["tags"]) if item["tags"] else "")]
        cards.append("\n".join(card))
    return "\n".join(rows), "\n\n".join(cards)


def rendered_readme(items):
    content = (ROOT / "README.md").read_text(encoding="utf-8")
    for name, body in zip(("PROJECT_INDEX", "PROJECT_CARDS"), sections(items)):
        start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
        if content.count(start) != 1 or content.count(end) != 1 or content.index(start) >= content.index(end):
            raise ValueError(f"README.md: 缺少或重复、错序的 {name} 标记")
        head, remainder = content.split(start, 1)
        _, tail = remainder.split(end, 1)
        content = f"{head}{start}\n{body}\n{end}{tail}"
    return content


def sync(check=False):
    items = projects()
    expected = rendered_readme(items)
    readme = ROOT / "README.md"
    if check:
        if readme.read_text(encoding="utf-8") != expected:
            raise ValueError("首页索引需要更新，请运行 python scripts/projects.py sync")
        print(f"检查通过：{len(items)} 个项目，首页索引一致。")
    else:
        readme.write_text(expected, encoding="utf-8", newline="\n")
        print(f"首页已同步：{len(items)} 个项目。")


def create(args):
    items = projects()
    rendered_readme(items)  # Validate markers before creating files.
    number = max((int(item["id"]) for item in items), default=0) + 1
    if number > 999:
        raise ValueError("编号已达到 999，请先扩展编号规范")
    if not SLUG.fullmatch(args.slug):
        raise ValueError("slug 必须使用小写英文、数字和短横线")
    if any(item["slug"] == args.slug for item in items):
        raise ValueError(f"项目名称已存在: {args.slug}")
    directory = ROOT / "projects" / f"{number:03d}-{args.slug}"
    data = {"id": f"{number:03d}", "slug": args.slug, "title": args.title,
            "summary": args.summary, "upstream": args.upstream, "status": "待研究",
            "tags": [], "cover": "", "demo_url": ""}
    validate(data, directory)
    template = ROOT / "templates" / "project"
    shutil.copytree(template, directory)
    (directory / "project.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    document = (directory / "README.md").read_text(encoding="utf-8")
    replacements = {"ID": data["id"], "TITLE": plain(data["title"]),
                    "SUMMARY": plain(data["summary"]),
                    "UPSTREAM": quote(data["upstream"], safe="/:#?=&%+@,;~-")}
    document = re.sub(r"\{\{(ID|TITLE|SUMMARY|UPSTREAM)\}\}",
                      lambda match: replacements[match[1]], document)
    (directory / "README.md").write_text(document, encoding="utf-8", newline="\n")
    sync()
    print(f"已创建：projects/{directory.name}/")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new", help="新建编号研究项目")
    new.add_argument("slug")
    new.add_argument("--title", required=True)
    new.add_argument("--upstream", required=True)
    new.add_argument("--summary", required=True)
    commands.add_parser("sync", help="同步首页索引和预览")
    commands.add_parser("check", help="只检查元数据和首页一致性")
    args = parser.parse_args()
    try:
        if args.command == "new":
            create(args)
        else:
            sync(check=args.command == "check")
    except (ValueError, OSError) as error:
        print(f"错误：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
