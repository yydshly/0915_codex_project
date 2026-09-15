"""Merge the source-observed additions without replacing prior verification."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'app/cases.json'
cases = json.loads(path.read_text(encoding='utf-8'))
by_name = {c['name']: c for c in cases}
rows = (ROOT / 'notes/catalog-additions.tsv').read_text(encoding='utf-8').splitlines()
for row in rows:
    name, address, preview, group, title, capability, reference, boundary = row.split('|')
    if name in by_name:
        continue
    item = dict(id=re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-'), name=name,
        title=title, group=group, url='https://' + address, preview=preview,
        capability=capability, value=reference, role='效果与交互参考 · 具体实现待核查',
        mechanism=reference + '这是观察方向，不是已核实的底层实现。', boundary=boundary,
        evidence='catalog', observed='2026-09-15 重新展开原展厅目录，核对名称、简介、原作地址和预览图地址；本轮未进入该原作测试。',
        **{'try': reference.replace('参考', '进入原作时关注', 1), 'takeaway': '先用作效果与交互参照；找到源码或技术说明后，再判断是否值得提取实现。'})
    if name == 'Mini Moto Park':
        item['prior_research'] = 'https://yydshly.github.io/0913_codex_project/010-mini-moto-comparison/'
        item['takeaway'] = '与昨天已研究的原作相同，优先复用已有记录，避免重复研究。本轮仍按目录收录标记。'
    if name == 'Moonlit Forge Studio':
        item['takeaway'] = '简介不足以判断能力，暂作作品线索收藏。'
    if name == 'Sketch Golf':
        item['takeaway'] = '名称易让人联想到高尔夫，但本次严格按目录的代码绘画实验介绍收录，尚未核验原作。'
    cases.append(item)
    by_name[name] = item
assert len(cases) == 80, len(cases)
assert len({c['id'] for c in cases}) == len(cases)
assert len({c['url'] for c in cases}) == len(cases)
path.write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
snapshot = dict(source='https://awesomesites.ai/', observed_at='2026-09-15',
    method='Read visible gallery headings, descriptions, links and preview img src after clicking Load more once.',
    visible_count=80, load_more_remaining=False,
    items=[{'name':c['name'], 'url':c['url'], 'preview_url':'https://awesomesites.ai/previews/'+c['preview']} for c in sorted(cases,key=lambda c:c['name'].lower())])
(ROOT / 'notes/catalog-snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Merged catalog: {len(cases)} cases; retained existing verification records.')
