"""Check local links, image alt text, fragment anchors and descriptions."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
ROOT = Path(__file__).resolve().parents[1] / 'web'
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.errors = set(), [], []
        self.description = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append(f'duplicate id {a["id"]}')
            self.ids.add(a['id'])
        if tag == 'meta' and a.get('name') == 'description':
            self.description = bool(a.get('content'))
        if tag == 'img' and not a.get('alt'):
            self.errors.append('image missing descriptive alt')
        self.refs += [a[k] for k in ('href', 'src') if a.get(k)]
pages, errors, count = {}, [], 0
for path in ROOT.rglob('*.html'):
    p = Page()
    p.feed(path.read_text(encoding='utf-8'))
    pages[path.resolve()] = p
for path, p in pages.items():
    errors += [f'{path}: {e}' for e in p.errors]
    if not p.description:
        errors.append(f'{path}: missing description')
    for ref in p.refs:
        u = urlsplit(ref)
        if u.scheme or u.netloc:
            continue
        dest = (path.parent / unquote(u.path)).resolve() if u.path else path
        if dest.is_dir():
            dest = dest / 'index.html'
        count += 1
        if not dest.is_relative_to(ROOT.resolve()) or not dest.is_file():
            errors.append(f'{path}: invalid local file {ref}')
        elif u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:
            errors.append(f'{path}: missing anchor {ref}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Checked {len(pages)} HTML pages and {count} local links; images, anchors and descriptions valid.')
