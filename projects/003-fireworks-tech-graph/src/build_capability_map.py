"""One editable, source-grounded capability infographic; no model image service."""
from pathlib import Path
from html import escape

P=Path(__file__).resolve().parents[1]
OUT=P/'app/capability-map'
OUT.mkdir(exist_ok=True)
s=[]
INK='#17324b';MUTED='#536c80';BLUE='#2563b5';TEAL='#087f78'
def text(x,y,t,size=24,color=INK,weight=400):
 s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(t)}</text>')
def rect(x,y,w,h,fill='#fff',stroke='#d8e3eb',r=16):
 s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')
def path(d):s.append(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#arrow)"/>')
def lines(x,y,ts,size=23,gap=34,color=MUTED):
 for i,t in enumerate(ts):text(x,y+i*gap,t,size,color)
def card(x,y,w,h,n,title,color=BLUE):
 rect(x,y,w,h);rect(x+22,y+22,40,35,color,color,8);text(x+33,y+48,n,22,'white',650);text(x+77,y+49,title,28,INK,650)

rect(0,0,1800,1780,'#f1f6fa','#f1f6fa',0)
rect(0,0,1800,165,'#17324b','#17324b',0)
text(60,66,'Fireworks Tech Graph',44,'white',700)
text(60,118,'把已理解的系统与关系，制成可交付的技术图',30,'#d5e6f2')
text(60,196,'01  从材料到成图：大模型理解内容，Fireworks 提供绘图规范与工具',26,INK,650)

card(60,225,360,300,'1','输入材料')
lines(84,319,['代码库 / GitHub 仓库','文档、需求、自然语言说明'],23)
rect(82,383,316,116,'#edf5fc','#d8e3eb',10)
text(98,417,'或：已经整理好的图纸',23,INK,600)
lines(98,451,['Fireworks 格式 JSON','或按其规范编写的 SVG'],22,29)

card(465,225,360,300,'2','大模型 / 作者')
lines(489,319,['读取源码、文档与证据','提取模块、调用、数据关系','确定范围，核对事实','选择图型、文字与布局','写成图纸 JSON 或 SVG'],23,37)

card(870,225,430,300,'3','Fireworks 处理',TEAL)
text(894,317,'路线 A：图纸 JSON → 渲染 SVG',23,INK,600)
text(894,353,'绘制节点、样式、连线与路由',23,MUTED)
text(894,394,'路线 B：AI 已编写 SVG → 检查',23,INK,600)
text(894,430,'参照图型规范、模板和风格规则',23,MUTED)
text(894,479,'两路均可检查、修订、导出',24,TEAL,650)

card(1345,225,395,300,'4','输出与使用')
lines(1369,321,['SVG  · 可编辑矢量源图','PNG  · 文档、汇报、配图','HTML · 离线查看与交互','GIF   · 限定场景的动态演示','附带图纸、布局与检查记录'],23,37)
for x1,x2 in [(420,461),(825,866),(1300,1341)]:path(f'M{x1} 359 H{x2}')
path('M240 525 V587 H1085 V529')
text(465,578,'已有合规 JSON / SVG，可直接进入处理',23,BLUE,600)

rect(60,613,1680,170,'#e5f0f6','#cbdfe9')
text(84,653,'怎样控制图？给的是“图纸”，不是随意一份 JSON。',27,INK,650)
text(84,695,'内容：节点、文字、分组与关系；布局：坐标、尺寸；外观：图型与风格。',25,INK)
text(84,736,'常见字段：nodes（id / label / x / y / width / height）、arrows（source / target / label）、mode、style。',22,MUTED)
text(84,767,'程序检查：XML、箭头、碰撞、几何、构图；部分工程风格另有领域规则。内容是否真实，仍需作者核实。',22,MUTED)

text(60,837,'02  什么时候用哪张图？按固定版本文档整理为 33 个展示条目',29,INK,700)
text(60,873,'图型决定表达什么；12 种视觉风格决定长什么样；SVG / PNG / HTML / GIF 是交付形式。',24,MUTED)

groups=[
 ('通用表达 · 4 项',[
 '流程图｜说明步骤与条件分支',
 '比较矩阵｜对比方案、功能与取舍',
 '时间轴 / 甘特图｜安排工期与里程碑',
 '思维导图 / 概念图｜整理主题与分支'],BLUE),
 ('系统与工程 · 7 项',[
 '系统架构图｜交代服务与存储分层',
 'C4 评审视图｜评审职责、边界与协议',
 '云部署视图｜说明区域、VPC 与工作负载',
 '事件流视图｜梳理主题、消费与异常出口',
 '可观测性视图｜展示指标与请求追踪',
 '网络拓扑图｜解释设备连接与访问边界',
 'UML 部署图｜说明制品部署到哪些节点'],TEAL),
 ('数据与结构 · 6 项',[
 '数据流图｜追踪数据加工与存储',
 'ER 实体关系图｜设计实体、键与基数',
 '对象图｜查看某一时刻的实例关系',
 '组件图｜说明组件、端口与依赖',
 '包图｜整理代码包与依赖',
 '组合结构图｜拆解内部部件与连接器'],BLUE),
 ('UML 与行为 · 8 项',[
 '时序图｜追踪消息调用的先后顺序',
 '状态机图｜梳理状态与触发事件',
 '类图｜描述类、属性、方法与关系',
 '用例图｜说明角色能使用哪些功能',
 '活动图｜说明并行步骤与汇合',
 '通信图*｜查看对象消息与编号顺序',
 'Timing 波形图*｜观察状态随时间变化',
 '交互概览图*｜组织多个交互片段'],TEAL),
 ('AI 领域模式 · 8 项',[
 'Agent 架构图｜拆解规划、记忆与工具',
 '记忆架构图｜梳理写入、合并与检索',
 '多 Agent 协作图｜解释分工与汇总',
 '工具调用图｜说明调用与结果回传',
 'Agent 记忆分类图｜区分记忆层次',
 'RAG 图｜说明检索如何支撑回答',
 'Agentic RAG 图｜解释自主检索决策',
 'Agentic Search 图｜解释多步搜索策略'],BLUE),
 ('支持边界：不要把数量当成引擎数',[
 '33 = 本次图型与领域变体的整理数',
 '其中部分名称共享架构 / 数据流记法',
 '本次展示：15 项由原生 JSON 生成',
 '另 18 项由 AI 按规范绘制 SVG',
 '这 18 项中有 3 项近似适配（*）',
 '不代表 33 个专用自动绘图引擎',
 '也不代表全部图型都能一键生成 GIF'],TEAL)
]
for i,(title,rows,color) in enumerate(groups):
 x=60+(i%3)*570;y=911+(i//3)*356
 rect(x,y,540,336)
 rect(x,y,540,7,color,color,0)
 text(x+22,y+44,title,25,INK,650)
 lines(x+22,y+83,rows,22,31,MUTED)

text(60,1666,'核心价值：把已经确认的技术关系，转成统一风格、可检查、可复用的图。',29,INK,650)
text(60,1707,'源码理解由外部大模型 / 作者完成；原库不是自动读取任意仓库并保证结论正确的代码分析器。',24,MUTED)
text(60,1747,'依据：Fireworks 固定提交 31fea364 · 图型规范 / 风格矩阵 / 生成器 · 本图由 AI 编写 SVG 并经原库导出',20,MUTED)

svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 1780"><title>Fireworks 能力全景：输入、处理、图型、场景与输出</title><defs><marker id="arrow" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#2563b5"/></marker></defs><style>text{font-family:"Microsoft YaHei","Segoe UI",sans-serif}</style>'+''.join(s)+'</svg>'
(OUT/'fireworks-capabilities.svg').write_text(svg,encoding='utf-8')
print(OUT/'fireworks-capabilities.svg')
