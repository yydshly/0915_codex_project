"""Recompute summary fields and a bounded chart probe from an upstream checkout."""
import argparse
import collections
import importlib.util
import json
import re
import statistics
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('upstream', type=Path)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
rows = json.loads((args.upstream / 'corpus/anatomy.json').read_text(encoding='utf-8'))
bookmarked = [r for r in rows if r['toc_depth'] > 0]
result = {
    'upstream_revision': 'bdc08bee5077462e1300431408c5237438a22d00',
    'scope': 'Recomputed from upstream JSON; original PDFs were not remeasured.',
    'records': len(rows),
    'pages_median': statistics.median(r['pages'] for r in rows),
    'pages_min': min(r['pages'] for r in rows),
    'pages_max': max(r['pages'] for r in rows),
    'orientations': dict(collections.Counter(r['orientation'] for r in rows)),
    'bookmark_depth_counts': dict(sorted(collections.Counter(r['toc_depth'] for r in rows).items())),
    'with_bookmarks': len(bookmarked),
    'with_at_least_two_levels': sum(r['toc_depth'] >= 2 for r in rows),
    'depth_mean_all': statistics.mean(r['toc_depth'] for r in rows),
    'depth_mean_bookmarked': statistics.mean(r['toc_depth'] for r in bookmarked),
    'color_metrics': 'Upstream-reported only; color classification was not independently reproduced.'
}
spec = importlib.util.spec_from_file_location('upstream_chart', args.upstream / 'assets/chart.py')
chart = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chart)
horizontal = chart.hbar([('up', 12), ('down', -11)])
paired = chart.paired_bars([('demo', 12, -11)])
result['bounded_chart_probe'] = {
    'data': {'positive': 12, 'negative': -11},
    'hbar_negative_widths': re.findall(r'width="(-[0-9.]+)"', horizontal),
    'paired_bars_negative_dimensions': re.findall(r'(?:width|height)="(-[0-9.]+)"', paired),
    'scope': 'SVG string probe only; not an end-to-end PDF test.'
}
encoded = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
if args.output:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded, encoding='utf-8')
print(encoded)
