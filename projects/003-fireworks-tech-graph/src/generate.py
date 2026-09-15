"""Reproduce the gallery with the pinned upstream CLI; no model service involved."""
from pathlib import Path
import argparse, copy, hashlib, json, shutil, subprocess, sys

PROJECT = Path(__file__).resolve().parents[1]
COMMIT = '31fea364eda5f1852b1175f3d9e29ea31d22dcb4'
SCENES = [
 (1,'mem0-style1','记忆架构','Flat Icon','提取、冲突处理、存储与检索分层展示。','sample-style1-flat'),
 (2,'tool-call-style2','工具调用','Dark Terminal','用暗色终端表达工具执行、证据与回答生成。','sample-style2-dark'),
 (3,'microservices-style3','微服务架构','Blueprint','工程网格、服务边界、存储与遥测。','sample-style3-blueprint'),
 (4,'agent-memory-types-style4','记忆类型','Notion Clean','用简洁层级解释工作记忆与长期记忆。','sample-style4-notion'),
 (5,'multi-agent-style5','多 Agent 协作','Glassmorphism','协调器、专家、共享状态和审查链路。','sample-style5-glass'),
 (6,'system-architecture-style6','系统架构','Claude Official','入口、运行时、策略、工具与运维分层。','sample-style6-claude'),
 (7,'api-flow-style7','API 集成','OpenAI','从 SDK、模型与工具，到输出和治理。','sample-style7-openai'),
 (8,'dark-luxury-style8','Agent 运行时','Dark Luxury','上游 AI 编写的 SVG 样例，金色结构与语义色。','sample-style8-dark-luxury'),
 (9,'c4-review-canvas-style9','C4 架构评审','C4 Review Canvas','显式表达抽象层级、职责、技术和关系协议。','sample-style9-c4-review-canvas'),
 (10,'cloud-fabric-style10','多区域部署','Cloud Fabric','Region、VPC、工作负载归属与复制机制。','sample-style10-cloud-fabric'),
 (11,'event-transit-style11','事件处理链','Event Transit','主题轨道、处理站、消费组、死信与状态投影。','sample-style11-event-transit'),
 (12,'ops-pulse-style12','可靠性观察','Ops Pulse','观察窗口、四类黄金信号、关键路径与追踪。','sample-style12-ops-pulse'),
]

def main():
 p=argparse.ArgumentParser();p.add_argument('--upstream',required=True);args=p.parse_args()
 upstream=Path(args.upstream).resolve()
 actual=subprocess.check_output(['git','-C',str(upstream),'rev-parse','HEAD'],text=True).strip()
 if actual!=COMMIT:raise SystemExit('Upstream commit mismatch: '+actual)
 out=PROJECT/'app'/'artifacts';out.mkdir(parents=True,exist_ok=True)
 cli=upstream/'scripts'/'fireworks.py'
 def write(name,data): (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 def run(*args,expected=0):
  r=subprocess.run([sys.executable,str(cli),*map(str,args)],capture_output=True,encoding='utf-8',timeout=90)
  if r.returncode!=expected:raise RuntimeError(f'{args}: {r.stdout} {r.stderr}')
  try:return json.loads(r.stdout or r.stderr)
  except ValueError:return {'returncode':r.returncode,'output':r.stdout,'error':r.stderr}
 def finish(key,mode=None):
  validation=run('check',out/(key+'.svg'));write(key+'.checks.json',validation)
  run('export-html',out/(key+'.svg'),out/(key+'.html'),'--title',key)
  # Preserve the viewer; add only document metadata for the research site's checker.
  html=out/(key+'.html');s=html.read_text(encoding='utf-8')
  s=s.replace('</head>','<meta name="description" content="Fireworks 原生离线图查看器；固定版本真实产物。"></head>')
  html.write_text(s,encoding='utf-8')
  return validation
 gallery=[]
 for style,key,title,theme,summary,sample in SCENES:
  source=upstream/'fixtures'/(key+('.svg' if style==8 else '.json'))
  if style==8:shutil.copy2(source,out/(key+'.svg'))
  else:
   shutil.copy2(source,out/(key+'.json'));data=json.loads(source.read_text(encoding='utf-8'))
   run('render',data['mode'],out/(key+'.json'),out/(key+'.svg'),'--report',out/(key+'.layout.json'))
  checked=finish(key)
  shutil.copy2(upstream/'assets'/'samples'/(sample+'.gif'),out/(key+'.reference.gif'))
  gallery.append(dict(id=style,key=key,title=title,theme=theme,summary=summary,generated=style!=8,checks=checked['ok'],gifOrigin='上游 1.2.0 发布样片；本次未重新编码'))
 # Same topology and geometry across seven themes, using a real upstream baseline.
 base=json.loads((upstream/'fixtures/quality-baseline/agent-runtime-style1.json').read_text(encoding='utf-8'))
 base.update(title='研究助手的运行架构',subtitle='同一组节点与关系 · 只切换视觉风格',text_policy='strict')
 labels={'client':('研究请求','问题与约束'),'gateway':('任务入口','认证与分发'),'agent':('研究 Agent','规划与推理'),'memory':('资料记忆','检索与持久化'),'tools':('工具运行','搜索与函数'),'eval':('评估','质量检查')}
 for n in base['nodes']:
  n['label'],n['sublabel']=labels[n['id']]
  for k in ('fill','stroke','flat'):n.pop(k,None)
 for c,label in zip(base['containers'],['请求与控制','执行与状态']):c['label']=label
 for e,label in zip(base['arrows'],['请求','分发','上下文','调用','补充','记录','反馈']):e['label']=label
 for l,label in zip(base['legend'],['主链路','数据','依赖']):l['label']=label
 custom=[]
 for style in range(1,8):
  key=f'chinese-style{style}';data=copy.deepcopy(base);data['style']=style;data['footer']=f'中文教学案例 · 风格 {style} · 6 节点 / 7 关系'
  write(key+'.json',data);run('render','architecture',out/(key+'.json'),out/(key+'.svg'),'--report',out/(key+'.layout.json'));finish(key)
  custom.append(dict(id=style,key=key,theme=SCENES[style-1][3]))
 # Negative cases are actual upstream rejections, not front-end simulations.
 negatives=[]
 broken=copy.deepcopy(base);broken['arrows'][0]['target']='missing-node'
 cases=[('dangling','连接不存在的节点',broken,'validate','architecture')]
 broken=copy.deepcopy(base);broken['nodes'][0]['label']='必须完整显示的中文标签'*45
 cases.append(('truncation','严格模式下文字放不下',broken,'render','architecture'))
 broken=json.loads((upstream/'fixtures/ops-pulse-style12.json').read_text(encoding='utf-8'))
 service=next(n for n in broken['nodes'] if n.get('ops_role')=='service');service['signals'].pop('errors')
 cases.append(('signals','可靠性视图缺少错误指标',broken,'validate',broken['mode']))
 for key,label,data,command,mode in cases:
  write('invalid-'+key+'.json',data)
  call=[command,mode,out/('invalid-'+key+'.json')]
  if command=='render':call += [out/('invalid-'+key+'.svg')]
  result=run(*call,expected=1);write('invalid-'+key+'.result.json',result)
  negatives.append(dict(key=key,label=label,result=result))
 shutil.copy2(upstream/'LICENSE',out/'LICENSE-Fireworks.txt')
 manifest=dict(commit=COMMIT,packageVersion='1.2.0',revision='含未发布质量升级',date='2026-09-15',gallery=gallery,custom=custom,negativeCases=negatives,visualReview='待逐图视觉复核',newSvg=18,staticSvg=1)
 (PROJECT/'app'/'data.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 write('provenance.json',dict(commit=COMMIT,files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.iterdir() if f.is_file() and f.suffix!='.png' and f.name not in {'provenance.json','png-receipt.json','visual-review.json'}},htmlChange='仅增加 description 元数据；原生查看器逻辑不变',gif='上游发布样片，未重新编码',checks='19 SVG × 5 项程序检查；3 个无效输入均被真实拒绝'))
 print('Generated 18 SVGs + 1 upstream-authored SVG; 19 checks/viewers; 3 negative cases.')

if __name__=='__main__':main()
