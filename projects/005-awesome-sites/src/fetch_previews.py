"""Save the preview assets observed in the source gallery; reuse saved files."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from urllib.request import Request, urlopen
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'app/images'
OUT.mkdir(parents=True, exist_ok=True)
cases = json.loads((ROOT / 'app/cases.json').read_text(encoding='utf-8'))
def fetch(case):
    dest = OUT / case['preview']
    if dest.exists():
        return dest.name, dest.stat().st_size
    url = 'https://awesomesites.ai/previews/' + case['preview']
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=35) as response:
        data = response.read()
    if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        raise ValueError(f'Invalid WebP: {url}')
    dest.write_bytes(data)
    return dest.name, len(data)
with ThreadPoolExecutor(max_workers=6) as pool:
    for name, size in pool.map(fetch, cases):
        print(name, size)
