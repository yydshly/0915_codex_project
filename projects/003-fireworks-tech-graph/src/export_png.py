"""Export with upstream Chromium renderer, or record an already completed export."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, struct, subprocess, sys
PROJECT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--upstream',required=True);p.add_argument('--record-existing',action='store_true');args=p.parse_args()
 upstream=Path(args.upstream).resolve();out=PROJECT/'app/artifacts'
 env=os.environ.copy();env['FIREWORKS_PYTHON']=sys.executable
 if not args.record_existing:subprocess.run(['node',str(upstream/'scripts/svg2png.js'),str(out)],env=env,check=True,timeout=240)
 sizes={}
 for svg in out.glob('*.svg'):
  png=svg.with_suffix('.png');b=png.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';w,h=struct.unpack('>II',b[16:24]);sizes[png.name]={'width':w,'height':h,'sha256':hashlib.sha256(b).hexdigest()}
 (out/'png-receipt.json').write_text(json.dumps({'renderer':'upstream scripts/svg2png.js / Puppeteer 25.3.0 / Chromium','images':sizes},indent=2)+'\n',encoding='utf-8')
 shutil.copy2(out/'chinese-style1.png',PROJECT/'assets/preview.png')
 provenance=json.loads((out/'provenance.json').read_text(encoding='utf-8'));provenance['png']=sizes
 (out/'provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Recorded',len(sizes),'PNGs; signatures and dimensions read back.')
if __name__=='__main__':main()
