"""Publish app files and selected assets, never the whole research repository."""
from pathlib import Path
import html
import shutil
from projects import ROOT, projects, upstream_label

def build():
    public = ROOT / 'web'
    public.mkdir(exist_ok=True)
    cards, rows = [], []
    for item in projects():
        name = f"{item['id']}-{item['slug']}"
        project = ROOT / 'projects' / name
        if not (project / 'app/index.html').is_file():
            continue
        target = public / name
        shutil.copytree(project / 'app', target, dirs_exist_ok=True)
        if item['cover']:
            dest = target / item['cover']
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(project / item['cover'], dest)
        title, summary, upstream = map(html.escape, (item['title'], item['summary'], item['upstream']))
        source_name = html.escape(upstream_label(item['upstream']))
        cover = f'<img src="{name}/{html.escape(item["cover"])}" alt="{title}架构与效果引导图">' if item['cover'] else ''
        cards.append(f'<article><a href="{name}/">{cover}</a><div><span>RESEARCH / {item["id"]}</span><h2><a href="{name}/">{title}</a></h2><p>{summary}</p><a class="go" href="{name}/">阅读研究 →</a> <a class="upstream" href="{upstream}">{source_name} ↗</a></div></article>')
        rows.append(f'<tr><td>{item["id"]}</td><th><a href="{name}/">{title}</a></th><td>{summary}</td><td><a href="{upstream}">{source_name} ↗</a></td></tr>')
    page = '''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>开源研究手记｜项目索引</title><meta name="description" content="开源项目的能力、原理、效果与应用边界。每项研究关联原始仓库与完整说明。"><style>
    *{box-sizing:border-box}body{margin:0;background:#f3f0e9;color:#202b30;font-family:"Segoe UI","Microsoft YaHei",sans-serif;line-height:1.8}a{color:inherit;text-decoration:none}a:hover{color:#bb4c30}a:focus-visible{outline:3px solid #bb4c30;outline-offset:4px}main,header,footer{max-width:1170px;margin:auto;padding:25px 35px}header{border-bottom:1px solid #d9dcd2;display:flex;justify-content:space-between;font-size:13px}.brand{font-weight:650}header a{font-size:12px}h1{font-size:50px;line-height:1.3;font-weight:550;letter-spacing:-2px;margin:25px 0 18px}.intro{color:#64716f;max-width:760px}.eyebrow,article span{color:#236d67;font-size:10px;letter-spacing:2px}.hero{padding:35px 0 45px}article{border:1px solid #d9dcd2;background:#fcfbf7;margin:0 0 45px;border-radius:5px;overflow:hidden;display:grid;grid-template-columns:1.25fr 1fr}article>a{display:flex;align-items:center;background:white}article img{width:100%;height:auto;display:block}article>div{padding:32px}h2{font-size:25px;line-height:1.5;margin:15px 0}article p{color:#64716f;font-size:13px}.go{display:inline-block;background:#202b30;color:white;padding:9px 16px;font-size:12px;margin-top:15px}.upstream{font-size:12px;margin-left:15px}.table-scroll{overflow:auto}table{border-collapse:collapse;width:100%;min-width:680px;font-size:12px;text-align:left}td,th{padding:20px 15px;border-bottom:1px solid #d9dcd2;vertical-align:top}thead{color:#64716f;font-weight:400}td:first-child{color:#236d67}th{min-width:140px}footer{font-size:11px;color:#64716f;margin-top:45px;border-top:1px solid #d9dcd2}@media(max-width:700px){main,header,footer{padding:22px}h1{font-size:37px}.hero{padding-top:20px}article{grid-template-columns:1fr}article>div{padding:24px}article h2{font-size:23px}.intro{font-size:14px}}
    </style></head><body><header><a class="brand" href="./">R. 开源研究手记</a><a href="https://github.com/yydshly/0915_codex_project">研究仓库 ↗</a></header><main><section class="hero"><span class="eyebrow">OPEN SOURCE / FIELD NOTES</span><h1>理解工具，<br>也理解它的边界。</h1><p class="intro">从能力与底层机制出发，连接实际效果、使用场景和扩展方向。每一项结论保留来源，每一种效果说明验证范围。</p></section>'''
    page += ''.join(cards) + '<h2>项目索引</h2><div class="table-scroll" tabindex="0" role="region" aria-label="项目索引"><table><thead><tr><th>编号</th><th>研究项目</th><th>能力与实现原理摘要</th><th>关联原库</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div></main><footer>2026 · GitHub 项目研究笔记 · 原始项目与独立研究分别署名</footer></body></html>'
    (public / 'index.html').write_text(page, encoding='utf-8')
    (public / '.nojekyll').touch()
    print(f'Built {len(cards)} research pages into web/')

if __name__ == '__main__':
    build()
