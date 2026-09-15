"""Validate artifacts and meaningful same-topology invariants."""
from pathlib import Path
import hashlib,json,struct,xml.etree.ElementTree as ET
PROJECT=Path(__file__).resolve().parents[1];APP=PROJECT/'app';OUT=APP/'artifacts'
d=json.loads((APP/'data.json').read_text(encoding='utf-8'))
keys=[s['key'] for s in d['gallery']+d['custom']]
assert len(keys)==19
for key in keys:
 ET.parse(OUT/(key+'.svg'))
 checks=json.loads((OUT/(key+'.checks.json')).read_text(encoding='utf-8'))
 assert checks['ok'] and set(checks['checks'])=={'xml','markers','collisions','geometry','composition'}
 assert all(c['ok'] for c in checks['checks'].values())
 b=(OUT/(key+'.png')).read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n'
 assert all(v>0 for v in struct.unpack('>II',b[16:24]))
 assert (OUT/(key+'.html')).is_file()
baseline=None
for s in d['custom']:
 spec=json.loads((OUT/(s['key']+'.json')).read_text(encoding='utf-8'))
 graph={'nodes':spec['nodes'],'arrows':spec['arrows'],'containers':spec['containers']}
 if baseline is None:baseline=graph
 assert graph==baseline,'Same-topology experiment changed content or coordinates'
 report=json.loads((OUT/(s['key']+'.layout.json')).read_text(encoding='utf-8'))
 assert report['typography']['complete_text']
for case in d['negativeCases']:
 assert case['result'].get('ok') is False
 assert not (OUT/('invalid-'+case['key']+'.svg')).exists()
provenance=json.loads((OUT/'provenance.json').read_text(encoding='utf-8'))
for name,digest in provenance['files'].items():assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==digest,name
for name,item in provenance['png'].items():assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==item['sha256'],name
for s in d['gallery']:
 b=(OUT/(s['key']+'.reference.gif')).read_bytes();assert b[:6] in [b'GIF87a',b'GIF89a']
assert (APP/'comparison/archify.png').is_file() and (APP/'comparison/graphify.svg').is_file()
receipt={'date':'2026-09-15','svgFiles':19,'nativeHtml':19,'pngFiles':19,'programChecksPassed':95,'identicalChineseTopologies':7,'negativeCasesRejected':3,'historicalGifReferences':12,'inputAndOutputHashes':'passed','browserInteractionQA':'not performed','siteScreenshotQA':'not performed','limits':'Program checks are not a full visual or business-fact audit. Comparisons reuse prior fixed-version research.'}
(APP/'verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
