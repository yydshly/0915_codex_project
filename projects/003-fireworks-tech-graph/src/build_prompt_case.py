"""Read the fixed target inventory; render authored, sourced diagrams via Fireworks."""
from pathlib import Path
from collections import Counter
from urllib.parse import quote
import argparse,hashlib,json,os,struct,subprocess,sys

PROJECT=Path(__file__).resolve().parents[1]
TARGET='1e4203a7d88873c1b37ab2d1c07074fea498c274'
FIREWORKS='31fea364eda5f1852b1175f3d9e29ea31d22dcb4'
URL='https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools'

def main():
 p=argparse.ArgumentParser();p.add_argument('--target',required=True);p.add_argument('--fireworks',required=True);a=p.parse_args()
 target=Path(a.target).resolve();fw=Path(a.fireworks).resolve();out=PROJECT/'app/prompt-case';out.mkdir(parents=True,exist_ok=True)
 for root,commit in [(target,TARGET),(fw,FIREWORKS)]:assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==commit
 files=subprocess.check_output(['git','-C',str(target),'ls-files'],text=True).splitlines()
 dirs=sorted({f.split('/')[0] for f in files if '/' in f and not f.startswith(('.github/','assets/'))})
 checks=[]
 for name in files:
  if not name.endswith('.json'):continue
  try:
   d=json.loads((target/name).read_text(encoding='utf-8'));checks.append({'file':name,'parsed':True,'topType':type(d).__name__})
  except json.JSONDecodeError as e:checks.append({'file':name,'parsed':False,'line':e.lineno,'reason':e.msg})
 sources=[('Manus Agent Tools & Prompt/Agent loop.txt',27,33,'事件、工具、执行、迭代、交付、待命'),('Manus Agent Tools & Prompt/tools.json',1,None,'29 个工具定义；仅接口说明'),('Cursor Prompts/Agent Prompt 2.0.txt',12,27,'语义检索与精确查找的选择条件'),('Cursor Prompts/Agent Tools v1.0.json',1,None,'13 个工具定义'),('Kiro/Spec_Prompt.txt',208,210,'requirements.md'),('Kiro/Spec_Prompt.txt',265,271,'design.md'),('Kiro/Spec_Prompt.txt',303,306,'tasks.md'),('Amp/gpt-5.yaml',1,10,'模型名称、角色与调试输入快照')]
 evidence=[]
 for name,start,end,meaning in sources:
  b=(target/name).read_bytes();evidence.append(dict(file=name,start=start,end=end,meaning=meaning,sha256=hashlib.sha256(b).hexdigest(),url=URL+'/blob/'+TARGET+'/'+quote(name,safe='/')+f'#L{start}'+(f'-L{end}' if end else '')))
 receipt=dict(target=URL,commit=TARGET,date='2026-09-15',trackedFiles=len(files),collectionDirectories=dirs,directoryCount=len(dirs),extensions=dict(Counter(Path(f).suffix or '(none)' for f in files)),jsonChecks=checks,evidence=evidence,files=files,limits='目录数量不等于独立产品数量；文件内容是仓库收录的快照，真实性、完整性和现行性未逐项向厂商验证。未运行其中描述的 AI 产品。')
 def write(name,obj):(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 write('research.json',receipt)
 def node(id,label,sub,x,y,kind='rect'):
  return dict(id=id,label=label,sublabel=sub,x=x,y=y,width=240,height=90,kind=kind)
 def edge(id,source,target,label,sp='right',tp='left',**kw):
  return dict(id=id,source=source,target=target,label=label,source_port=sp,target_port=tp,flow='data',**kw)
 def diagram(title,subtitle,nodes,arrows,footer):
  return dict(schema_version=1,mode='architecture',style=1,text_policy='strict',quality_profile='showcase',width=1200,height=720,title=title,subtitle=subtitle,nodes=nodes,arrows=arrows,footer=footer,footer_x=48,footer_y=685)
 overview=diagram('AI 工具提示词资料集','资料如何组织 · 基于固定版本的文件清单',[
  node('archive','资料仓库','111 个跟踪文件',480,135,'double_rect'),node('groups','按产品与来源归档','32 个一级资料目录',480,305),
  node('prompts','提示词与工作规则','83 个 TXT 文本文件',60,505,'document'),node('tools','工具接口说明','17 个 JSON 后缀文件',480,505,'document'),node('snapshots','模型配置快照','Amp 目录的 2 个 YAML',900,505,'document')
 ],[edge('organize','archive','groups','归档','bottom','top'),edge('text','groups','prompts','文本','left','top',route_points=[[180,350]]),edge('interfaces','groups','tools','接口','bottom','top'),edge('configs','groups','snapshots','配置','right','top',route_points=[[1020,350]])],
 '目录统计排除 .github 与 assets；另有 9 个文件。文件后缀不等于内容真实性；未见模型权重或完整运行服务。')
 ns=[node('events','分析事件','用户消息与执行结果',60,175),node('choose','选择工具','依据状态、计划与知识',480,175,'double_rect'),node('execute','执行动作','由外部沙箱或工具执行',900,175),node('observe','接收观察','执行结果回到事件流',900,465),node('done','判断是否完成','未完成则进入下一轮',480,465),node('deliver','交付并待命','发送结果，等待新任务',60,465)]
 loop=diagram('Manus 提示词描述的工作循环','依据仓库 Agent loop.txt 的文字整理；没有在本次运行 Manus',ns,[
  edge('select','events','choose','决定'),edge('call','choose','execute','调用'),edge('result','execute','observe','返回','bottom','top'),edge('evaluate','observe','done','判断','left','right'),edge('finish','done','deliver','完成','left','right'),edge('repeat','done','events','未完成','top','bottom',route_points=[[600,365],[180,365]],dashed=True)
 ],'来源：Manus Agent Tools & Prompt/Agent loop.txt，第 27–33 行。模型、沙箱和工具实现需要由实际产品提供。')
 flow=diagram('把参考资料变成自己的研究助手','本次分析提出的使用流程 · 尚未接入模型或执行服务',[
  node('goal','确定你的任务','例如：分析开源项目',60,175),node('read','阅读相关样例','Cursor、Kiro、Manus',480,175,'document'),node('principles','提炼可用规则','检索、计划、执行与交付',900,175),node('adapt','编写自己的指令','只描述实际存在的工具',900,465,'document'),node('test','用真实任务验证','检查结果、来源与失败',480,465),node('save','保存可复用版本','沉淀提示词与测试案例',60,465)
 ],[edge('a','goal','read','选择'),edge('b','read','principles','比较'),edge('c','principles','adapt','改写','bottom','top'),edge('d','adapt','test','试用','left','right'),edge('e','test','save','通过后','left','right')],
 '借鉴工作方法，不把工具定义当工具实现。复制一份提示词不会同时获得模型、记忆、浏览器或执行环境。')
 cli=fw/'scripts/fireworks.py'
 for key,data in [('overview',overview),('agent-loop',loop),('your-workflow',flow)]:
  write(key+'.json',data)
  for args in [('render','architecture',out/(key+'.json'),out/(key+'.svg'),'--report',out/(key+'.layout.json')),('check',out/(key+'.svg')),('export-html',out/(key+'.svg'),out/(key+'.html'),'--title',data['title'])]:
   r=subprocess.run([sys.executable,str(cli),*map(str,args)],capture_output=True,encoding='utf-8',timeout=120)
   if r.returncode:raise RuntimeError(r.stdout+r.stderr)
   if args[0]=='check':write(key+'.checks.json',json.loads(r.stdout))
  hp=out/(key+'.html');s=hp.read_text(encoding='utf-8').replace('</head>','<meta name="description" content="Fireworks 原生生成的中文仓库分析图。"></head>');hp.write_text(s,encoding='utf-8')
 env=os.environ.copy();env['FIREWORKS_PYTHON']=sys.executable
 subprocess.run(['node',str(fw/'scripts/svg2png.js'),str(out)],env=env,check=True,timeout=180)
 pngs={}
 for file in out.glob('*.png'):
  b=file.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';pngs[file.name]=dict(zip(['width','height'],struct.unpack('>II',b[16:24])))
 write('receipt.json',dict(targetCommit=TARGET,fireworksCommit=FIREWORKS,renderer='Fireworks CLI + upstream svg2png.js',authorship='资料盘点由脚本执行；关系和中文解读由本次 Agent 编写；图形由 Fireworks 渲染',svgCount=3,checks=15,png=pngs,gif='未生成；本次为自定义资料结构与流程图，不套用无关动效场景',hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.iterdir() if f.is_file() and f.name not in {'receipt.json','visual-review.json'}}))
 print(json.dumps({'files':len(files),'directories':len(dirs),'jsonParsed':sum(x['parsed'] for x in checks),'jsonRejected':sum(not x['parsed'] for x in checks),'diagrams':3},ensure_ascii=False))

if __name__=='__main__':main()
