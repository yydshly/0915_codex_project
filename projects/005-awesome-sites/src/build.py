"""Render the reviewed catalog to dependency-free static HTML."""
import json
import base64
import hashlib
from pathlib import Path
from html import escape as e

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'app'
cases = json.loads((APP / 'cases.json').read_text(encoding='utf-8'))
total = len(cases)
action_count = sum(c['evidence'] == 'action' for c in cases)
page_count = sum(c['evidence'] == 'page' for c in cases)
catalog_count = sum(c['evidence'] == 'catalog' for c in cases)
labels = {'action': '关键操作已验证', 'page': '原站界面已查看', 'catalog': '仅目录与预览'}
groups = list(dict.fromkeys(c['group'] for c in cases))
guide_specs = [
    ('ocean', '海洋与天空', '水面反光 · 天气氛围'),
    ('forest', '森林与光影', '植被层次 · 空间纵深'),
    ('mini-moto-park', '赛车与地形', '微缩场景 · 赛道视角'),
    ('diamond', '珠宝与材质', '折射高光 · 产品展示'),
    ('books', '书架与空间', '三维排布 · 内容索引'),
    ('daybreak-piano-film', '人物与表演', '人物动作 · 室内光照'),
]
case_by_id = {c['id']: c for c in cases}
guide_cards = []
cover_parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675" role="img" aria-labelledby="title desc"><title id="title">Awesome Sites 网页效果截图导览</title><desc id="desc">海洋、森林、赛车、珠宝、书架与钢琴表演六个原作的展厅预览截图。</desc><rect width="1200" height="675" fill="#10232c"/><g font-family="Segoe UI, Microsoft YaHei, sans-serif"><text x="30" y="49" fill="white" font-size="28" font-weight="700">Awesome Sites · 3D 相关产品收集库</text><text x="30" y="79" fill="#a8c1cc" font-size="16">从网页效果出发，寻找值得借鉴的细节</text>']
for index, (case_id, title, note) in enumerate(guide_specs):
    c = case_by_id[case_id]
    guide_cards.append(f'<a class="effect-tile" href="{e(c["url"])}" target="_blank" rel="noopener noreferrer" aria-label="打开 {e(c["name"])} 原作"><img src="images/{e(c["preview"])}" alt="{e(c["name"])} 网页效果：{e(title)}" width="720" height="338"><div><strong>{e(title)} <span aria-hidden="true">↗</span></strong><small>{e(note)}</small><span class="effect-name">{e(c["name"])}</span></div></a>')
    x, y = 30 + (index % 3) * 386, 105 + (index // 3) * 256
    encoded = base64.b64encode((APP / 'images' / c['preview']).read_bytes()).decode('ascii')
    cover_parts.append(f'<rect x="{x}" y="{y}" width="368" height="238" rx="8" fill="#1c3540"/><image x="{x}" y="{y}" width="368" height="174" preserveAspectRatio="xMidYMid meet" href="data:image/webp;base64,{encoded}"/><text x="{x+14}" y="{y+200}" fill="white" font-size="18" font-weight="600">{e(title)}</text><text x="{x+14}" y="{y+223}" fill="#b6cad3" font-size="13">{e(c["name"])}</text>')
cover_parts.append('<text x="30" y="647" fill="#a8c1cc" font-size="14">截图来源：Awesome Sites 原展厅 · 原作预览与效果参考</text></g></svg>')
(ROOT / 'assets/effect-guide.svg').write_text(''.join(cover_parts), encoding='utf-8')
cards = []
for c in cases:
    detail = ''.join(f'<dt>{title}</dt><dd>{e(c[key])}</dd>' for title, key in [('实现线索与参考方向', 'mechanism'), ('本次观察', 'observed'), ('尚未验证的部分', 'boundary'), ('体验时看什么', 'try'), ('分析结论', 'takeaway')])
    if c.get('prior_research'):
        detail += f'<dt>已有研究</dt><dd><a href="{e(c["prior_research"])}" target="_blank" rel="noopener noreferrer">昨天的 Mini Moto 研究记录 ↗</a></dd>'
    cards.append(f'''<article class="case" id="{c['id']}" data-group="{e(c['group'])}">
<a class="preview" href="{e(c['url'])}" target="_blank" rel="noopener noreferrer" aria-label="访问 {e(c['name'])} 原作"><img src="images/{e(c['preview'])}" alt="{e(c['name'])}：Awesome Sites 提供的原作预览" width="800" height="500" loading="lazy"><span>展厅预览 · 非本地复现</span></a>
<div class="case-body"><div class="meta"><span class="group">{e(c['group'])}</span><span class="evidence {c['evidence']}">{labels[c['evidence']]}</span></div><h3>{e(c['title'])}</h3><p class="english">{e(c['name'])}</p><p class="capability">{e(c['capability'])}</p><div class="value"><small>可以借鉴什么</small><p>{e(c['value'])}</p></div><p class="role">{e(c['role'])}</p><details><summary>展开参考点与验证记录</summary><dl>{detail}</dl></details></div><div class="card-footer"><a href="{e(c['url'])}" target="_blank" rel="noopener noreferrer">打开原作 ↗</a><a href="https://awesomesites.ai/" target="_blank" rel="noopener noreferrer">目录来源</a></div></article>''')
filters = ''.join(f'<button type="button" data-filter="{g}" aria-pressed="{str(g == "全部").lower()}">{g} <span>{len(cases) if g == "全部" else sum(c["group"] == g for c in cases)}</span></button>' for g in ['全部', *groups])
page = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="以 3D 场景及相关交互产品为主的 80 个作品收集：原作预览、效果与交互参考，以及与已有研究的重合和边界。"><title>Awesome Sites：3D 相关产品收集库 · 005</title><link rel="stylesheet" href="style.css?v=__STYLE_VERSION__"><script src="app.js" defer></script></head><body>
<header><a class="brand" href="../"><b>005</b> 网页案例研究</a><nav><a href="#conclusions">能力对照</a>　<a href="#method">证据与范围</a>　<a href="https://awesomesites.ai/" target="_blank" rel="noopener noreferrer">原展厅 ↗</a></nav></header>
<main><section class="intro"><div><div class="eyebrow">AWESOME SITES / PRODUCT COLLECTION</div><h1>3D 相关产品<span>收集库</span></h1><p>以 3D 场景及相关交互产品为主，也收录二维工具、内容和音乐作品。这里保留 __TOTAL__ 个原作入口与效果参考；其中很多表现方式与我们已有实践重合，当前没有确认新增的可复用技术能力。</p></div><div class="stats"><div><strong>__TOTAL__</strong><span>已收录案例</span></div><div><strong>__VISITED__</strong><span>进入原站查看</span></div><div><strong>__ACTION__</strong><span>验证关键操作</span></div></div></section>
<section class="effect-guide" aria-labelledby="effect-title"><div class="section-head"><h2 id="effect-title">先看网页效果</h2><p>6 个代表画面 · 点击截图打开原作</p></div><div class="effect-grid">__GUIDE__</div><p class="effect-credit">截图来自 Awesome Sites 原展厅，展示原作画面；完整案例与验证记录见下方。</p><a class="guide-more" href="#gallery-title">浏览全部 __TOTAL__ 个案例 ↓</a></section>
<div class="thesis"><div><strong>效果参考：明确想做成什么样</strong><p>对照材质、灯光、人物动作、场景层次和镜头。</p></div><div><strong>交互参考：看操作怎样改变结果</strong><p>借鉴参数联动、工具编辑、玩法反馈与叙事节奏。</p></div><div><strong>技术参考：有实现证据再提取</strong><p>先记录实现线索；相似效果不代表使用相同算法。</p></div></div>
<section aria-labelledby="gallery-title"><div class="section-head"><h2 id="gallery-title">案例参考集</h2><p>原有 16 个案例之后，续补 64 个。图片来自原展厅，分类与参考方向为独立整理。</p></div><div class="filters" aria-label="按用途浏览">__FILTERS__</div><p class="result-status" id="result-status" aria-live="polite">显示 __TOTAL__ / __TOTAL__ 个案例 · 全部</p><div class="gallery">__CARDS__</div></section>
<section class="section" id="conclusions"><div class="section-head"><h2>我们的理解与参考价值</h2><a class="jump" href="#gallery-title">返回案例 ↑</a></div><p>对我们而言，它主要是作品收集与对照入口。天空、天气、水面、森林、人物动作、碰撞、赛车、展厅和参数联动，已经在山居、河谷、山地巡游、人物物理、Mini Moto 与展厅项目中接触或实践过。这里的新增价值集中在具体作品的风格、精细度和交互组合。</p><p>技术思路相近不代表算法或代码相同。本项目没有逐项检查原作源码，也没有从这些案例中提取新的通用模块。已实现的方向不需要因为换了主题就重复研究。</p><div class="compare" tabindex="0" role="region" aria-label="能力对照表"><table><thead><tr><th>参考方向</th><th>代表案例</th><th>值得观察的部分</th><th>深入前还要检查</th></tr></thead><tbody>
<tr><th>观赏与氛围</th><td>Pelagic Ocean / Verdant Forest</td><td>场景、光照、材质与镜头</td><td>移动端表现、资源成本、素材复用权利</td></tr>
<tr><th>理解与探索</th><td>Booktower / Time, Amplified</td><td>内容组织、参数联动与解释</td><td>资料准确性、索引效率、教学反馈</td></tr>
<tr><th>明确的小任务</th><td>Garage Mat / Texture Maker</td><td>尺寸到数量、图层到纹理的输入输出</td><td>边界条件、导出质量、保存与恢复</td></tr>
<tr><th>更复杂的工作流</th><td>Forma / Halo / Rally</td><td>编辑状态、文件流转或多人共享</td><td>数据持久化、同步、权限与完整流程</td></tr>
<tr><th>声音与角色表演</th><td>Daybreak Piano Film / Living Operator</td><td>动作、道具、声音与镜头的配合</td><td>同步方式、模型调用、动作资产与视频导出</td></tr>
<tr><th>内容与叙事</th><td>Oath &amp; Relic / Night Parade</td><td>章节、角色、场景揭示与阅读节奏</td><td>内容质量、素材来源、交互细节</td></tr></tbody></table></div><p class="notice">后续使用方式：作为参考目录保留，不逐项复现。只有遇到明显优于现有成果的细节、尚未实现的能力，或有源码可提取的实现时，再单独深入。参考作品数量不等于新增创作能力。</p></section>
<section class="section" id="method"><h2>证据与研究范围</h2><div class="method"><div><h3>目录已补齐，实测范围单独记录</h3><p>采集日期：2026-09-15。本轮重新展开原展厅一次「Load more」，页面共显示 __TOTAL__ 个案例且不再显示加载按钮。本页已收录这些案例的名称、原作链接、预览和中文参考点；全量收录不等于全量深度测评，也不代表此后不会新增作品。</p><p>首页默认随机排序。本页按主要参考用途分组，不等同于原站标签。新增 64 个案例未逐个进入原站测试，保留原有实测记录；缺少验证不等于缺少能力。</p><p><a href="cases.json" download>下载全部案例数据与证据记录</a> · <a href="catalog-snapshot.json" download>下载目录来源快照</a> · <a href="https://awesomesites.ai/" target="_blank" rel="noopener noreferrer">核对原始目录 ↗</a></p></div><div><h3>如何理解验证标记</h3><ul><li><b>关键操作已验证 · __ACTION__ 个：</b>海洋预设切换、地砖数量联动、书架索引展开、算法参数联动、纹理图层创建。</li><li><b>原站界面已查看 · __PAGE__ 个：</b>Forma 的页面、图层、工具与设备保存提示；没有完成编辑流程测试。</li><li><b>仅目录与预览 · __CATALOG__ 个：</b>按展厅信息归纳，未在本项目验证具体交互。Mini Moto 的历史研究单独链接。</li></ul><p>本项目未检查原作源码、生成提示词、制作成本或模型调用；“由 AI 制作”不等于“每次交互都调用 AI”。参考实现线索不等于获得新增技术模块。</p></div></div></section>
</main><footer>005 · Awesome Sites 独立案例研究　｜　原作与预览图归原作者或相应权利人所有；本页仅作署名研究引用，未复制作品源码或重新托管作品。</footer></body></html>'''
for token, value in {'__STYLE_VERSION__':hashlib.sha256((APP / 'style.css').read_bytes()).hexdigest()[:12], '__TOTAL__':total, '__VISITED__':action_count + page_count, '__ACTION__':action_count, '__PAGE__':page_count, '__CATALOG__':catalog_count, '__FILTERS__':filters, '__CARDS__':''.join(cards), '__GUIDE__':''.join(guide_cards)}.items():
    page = page.replace(token, str(value))
(APP / 'index.html').write_text(page, encoding='utf-8')
snapshot = ROOT / 'notes/catalog-snapshot.json'
if snapshot.exists():
    (APP / snapshot.name).write_bytes(snapshot.read_bytes())
print(f'Rendered {len(cases)} cases')
