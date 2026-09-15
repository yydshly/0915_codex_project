"""Catalog every named diagram view in the pinned Fireworks guidance.

Native JSON outputs and agent-authored SVGs have distinct provenance.
The latter implement the documented notation, not a claimed upstream renderer.
"""
from pathlib import Path
import argparse,hashlib,html,json,os,shutil,subprocess,sys

P=Path(__file__).resolve().parents[1];OUT=P/'app/types';COMMIT='31fea364eda5f1852b1175f3d9e29ea31d22dcb4'
catalog=[]
BLUE='#2558b9';INK='#20334f';ORANGE='#da662c';MUTED='#526781'
def esc(t):return html.escape(str(t),quote=True)
def text(x,y,t,size=20,anchor='middle',color=INK,weight=400,extra=''):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{esc(t)}</text>'
def rect(x,y,w,h,fill='#fff',stroke='#b8c9e2',rx=8,extra=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2" {extra}/>'
def box(x,y,w,h,title,sub='',fill='#edf4ff',extra=''):
 return rect(x,y,w,h,fill=fill,extra=extra)+text(x+w/2,y+(h/2 if sub else h/2+7),title,22,weight=600)+(text(x+w/2,y+h/2+28,sub,17,color=MUTED) if sub else '')
def path(d,color=BLUE,dashed=False,marker='arrow',extra=''):
 return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5"'+(' stroke-dasharray="7 5"' if dashed else '')+(f' marker-end="url(#{marker})"' if marker else '')+f' {extra}/>'
def line(x1,y1,x2,y2,**kw):return path(f'M{x1} {y1} L{x2} {y2}',**kw)
def circle(x,y,r,fill=INK):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
def end(x,y):return circle(x,y,15,'white')+circle(x,y,9)
def diamond(x,y,w=80,h=55):return f'<polygon points="{x-w},{y} {x},{y-h} {x+w},{y} {x},{y+h}" fill="#fff5e9" stroke="{ORANGE}" stroke-width="2"/>'
def card(x,y,title,attributes,methods=None,underlined=False):
 w=270;h=210 if methods else 190
 s=rect(x,y,w,h,rx=0)+rect(x,y,w,48,fill='#eaf1fc',rx=0)+text(x+w/2,y+31,title,20,weight=650,extra='class="instance"' if underlined else '')
 for i,a in enumerate(attributes):s+=text(x+16,y+79+i*28,a,17,'start')
 if methods:
  yy=y+140;s+=line(x,yy,x+w,yy,marker=None,color='#b8c9e2')
  for i,a in enumerate(methods):s+=text(x+16,yy+29+i*26,a,17,'start')
 return s
def authored(key,title,question,body,category='UML 与行为',support='按规范绘制',note='',source='diagram-layout-reference.md'):
 prefix=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 720" data-author="research-agent" data-diagram-type="{key}"><title>{esc(title)}</title><desc>{esc(question)} 本次 AI 按 Fireworks 指导编写 SVG。</desc><defs>
 <marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L9 4 L0 8" fill="none" stroke="{BLUE}" stroke-width="1.5"/></marker>
 <marker id="triangle" markerWidth="13" markerHeight="12" refX="12" refY="6" orient="auto"><path d="M1 1 L12 6 L1 11 Z" fill="white" stroke="{BLUE}" stroke-width="1.3"/></marker>
 <marker id="many" markerWidth="12" markerHeight="14" refX="12" refY="7" orient="auto"><path d="M0 7 L12 1 M0 7 L12 7 M0 7 L12 13" fill="none" stroke="{BLUE}" stroke-width="1.4"/></marker>
 </defs><style>text{{font-family:'Segoe UI','Microsoft YaHei',sans-serif}} .instance{{text-decoration:underline}}</style><rect width="1200" height="720" fill="white" data-graph-role="background"/>
 '''
 svg=prefix+text(600,54,title,31,weight=700)+text(600,90,question,18,color=MUTED)+body+text(48,687,'教学示例 · AI 按库内规范编写 SVG · 非专用生成器或实际运行数据',15,'start',MUTED)+'</svg>'
 (OUT/(key+'.svg')).write_text(svg,encoding='utf-8')
 catalog.append(dict(key=key,title=title,question=question,category=category,support=support,origin='AI 按 Fireworks 图型规范编写 SVG，再使用原库导出；不是上游专用图型渲染器。',note=note or '展示该图型的基本记法；不构成完整 UML 语义一致性认证。',input='svg',source=source,example='在线订单系统（教学设定）'))

def author_examples():
 # True lifelines, ordered messages, activation bars and an alt frame.
 b=''
 for x,name in [(180,'用户'),(570,'订单服务'),(1020,'支付服务')]:
  b+=box(x-95,140,190,58,name)+line(x,205,x,622,marker=None,dashed=True,color='#a1b2cb')
 b+=rect(561,255,18,350,fill='#dbe9ff',rx=0)+rect(1011,330,18,210,fill='#dbe9ff',rx=0)
 for x1,x2,y,label,dash in [(180,560,250,'1  提交订单',False),(580,1010,325,'2  创建支付',False),(1010,580,430,'3a  支付成功',True),(1010,580,525,'3b  支付失败',True),(560,180,600,'4  返回订单状态',True)]:b+=line(x1,y,x2,y,dashed=dash)+text((x1+x2)/2,y-15,label,18)
 b+=rect(460,370,690,190,fill='none',rx=0,extra='data-graph-role="container"')+text(480,395,'alt  [成功]',17,'start')+line(460,465,1150,465,marker=None,dashed=True,color='#a1b2cb')+text(480,490,'[失败]',17,'start')
 authored('sequence','时序图','一次请求里，谁先调用谁，谁返回什么？',b,note='生命线和消息时序由 AI 编排；模板只有占位结构，原库未提供完整时序自动布局器。')
 # Flowchart with a real decision and explicit branches.
 b=box(470,145,260,65,'提交订单')+line(600,210,600,258)+diamond(600,315,100,57)+text(600,322,'库存充足？',20)
 b+=path('M500 315 H245 V470')+text(360,296,'否',18)+path('M700 315 H955 V470')+text(825,296,'是',18)
 b+=box(115,470,260,80,'提示缺货','返回商品选择')+box(825,470,260,80,'创建订单','进入支付流程')
 authored('flowchart','流程图','步骤如何推进？遇到条件走哪条分支？',b,category='通用表达',note='使用开始/过程/判断与分支；不等于所有业务只有线性步骤。')
 b=circle(75,320,10)+line(85,320,170,320)+box(170,280,220,80,'待支付')+line(390,320,490,320)+text(440,300,'支付成功',17)+box(490,280,220,80,'已支付')+line(710,320,830,320)+text(770,300,'发货',17)+box(830,280,220,80,'已发货')+line(1050,320,1125,320)+end(1140,320)
 b+=path('M280 360 V520 H490')+text(380,498,'取消 / 超时',18)+box(490,480,220,80,'已取消')+line(710,520,835,520)+end(850,520)
 authored('state','状态机图','同一个订单有哪些状态？什么事件触发变化？',b,note='初始、终止、状态与触发事件；节点表示对象状态，不表示处理部门。')
 b=card(465,140,'«interface» Payable',[],['+ total(): Money','+ pay(): Result'])+card(110,415,'Order',['- id: UUID','- status: Status'],['+ total(): Money','+ pay(): Result'])+card(820,415,'OrderItem',['- quantity: int','- unitPrice: Money'],['+ subtotal(): Money'])
 b+=path('M245 415 V375 H600 V350',marker='triangle',dashed=True)+text(340,366,'实现',17)+line(380,520,820,520)+text(600,497,'包含',18)+text(412,547,'1',17)+text(787,547,'1..*',17)
 authored('class','类图','软件有哪些类、属性、方法与关系？',b,note='分栏展示类名/属性/方法，空心三角表示接口实现。不是从源码自动提取。')
 b=card(60,220,'Customer',['PK  customer_id','name','email'])+card(465,220,'Order',['PK  order_id','FK  customer_id','created_at'])+card(870,220,'OrderItem',['PK  item_id','FK  order_id','quantity'])
 b+=line(330,320,465,320,marker='many')+text(347,296,'1',17)+text(438,352,'0..*',17)+line(735,320,870,320,marker='many')+text(752,296,'1',17)+text(842,352,'1..*',17)
 b+=text(600,545,'PK 主键 · FK 外键 · 连线端点标出基数',21,color=MUTED)
 authored('er','ER 实体关系图','数据库有哪些实体、键与一对多关系？',b,category='数据与结构',note='ER 不属于 UML 图型；本例展示实体、主外键与基数，不生成数据库。')
 b=rect(290,145,810,475,fill='#f8fbff',rx=0,extra='data-graph-role="container"')+text(315,177,'在线订单系统',20,'start',weight=650)
 b+=circle(105,285,23,'white')+line(105,308,105,390,marker=None,color=INK)+line(60,340,150,340,marker=None,color=INK)+line(105,390,65,445,marker=None,color=INK)+line(105,390,145,445,marker=None,color=INK)+text(105,480,'顾客',20)
 for x,y,title in [(560,280,'浏览商品'),(560,480,'提交订单'),(930,480,'处理支付')]:b+=f'<ellipse cx="{x}" cy="{y}" rx="125" ry="48" fill="white" stroke="{BLUE}" stroke-width="2"/>'+text(x,y+7,title,21)
 b+=line(150,340,435,280,marker=None)+line(150,355,435,480,marker=None)+line(685,480,805,480,dashed=True)+text(745,456,'«include»',16)
 authored('usecase','用例图','谁可以使用系统的哪些功能？',b,note='角色在系统边界外，用例位于边界内，include 表示包含关系。')
 b=circle(600,145,11)+line(600,156,600,220)+rect(290,220,620,10,fill=INK,stroke=INK,rx=0)
 b+=line(360,230,360,320)+line(840,230,840,320)+box(230,320,260,80,'检查库存')+box(710,320,260,80,'校验支付信息')+line(360,400,360,485)+line(840,400,840,485)+rect(290,485,620,10,fill=INK,stroke=INK,rx=0)+line(600,495,600,545)+box(470,545,260,65,'提交订单')+line(600,610,600,638)+end(600,653)
 authored('activity','活动图','哪些动作可以并行？在哪里汇合？',b,note='流程图适配 UML 活动记法；粗横条表示 fork/join，并非专用活动建模引擎。')
 b=card(65,230,'c17 : Customer',['name = "林"','level = "普通"'],underlined=True)+card(465,230,'o42 : Order',['status = "已支付"','total = 128.00'],underlined=True)+card(865,230,'i01 : OrderItem',['quantity = 2','unitPrice = 64.00'],underlined=True)
 b+=line(335,320,465,320,marker=None)+line(735,320,865,320,marker=None)+text(400,296,'拥有',17)+text(800,296,'包含',17)+text(600,550,'某个时刻的实例快照；与类图中的类型定义不同',21,color=MUTED)
 authored('object','对象图','某个时刻有哪些实例，实例间怎样关联？',b,category='数据与结构',note='由类图样式适配；带下划线的“实例名 : 类型”表示对象。')
 b=''
 for x,title,sub in [(95,'Order API','HTTP 接口'),(485,'Order Core','订单规则'),(875,'Payment Adapter','支付适配')]:
  b+=box(x,275,235,150,title,sub)+text(x+117,251,'«component»',17)+rect(x-10,320,20,25,fill='white',rx=0)+rect(x+225,320,20,25,fill='white',rx=0)
 b+=line(340,333,475,333)+text(405,305,'调用',17)+line(730,333,865,333)+text(795,305,'适配',17)
 authored('component','组件图','组件的职责、端口和依赖是什么？',b,category='数据与结构',note='仓库映射到架构图表达；这里补充 component 标记与端口，不验证完整接口兼容性。')
 b=''
 for x,title,artifact in [(100,'应用节点','orders-service.jar'),(770,'数据库节点','orders 数据库')]:
  b+=rect(x,225,320,315,fill='#f4f8ff',rx=0,extra='data-graph-role="container"')+path(f'M{x} 225 L{x+24} 205 H{x+344} L{x+320} 225 M{x+320} 225 L{x+344} 205 V520 L{x+320} 540',marker=None)+text(x+160,274,'«device» '+title,19,weight=600)+box(x+30,355,260,95,artifact,'«artifact»')
 b+=line(420,315,770,315)+text(595,292,'TCP / PostgreSQL',18)
 authored('deployment','UML 部署图','软件制品部署到哪些运行节点？',b,category='系统与工程',note='架构图的节点/实例适配；与带 Region/VPC 领域检查的 Cloud Fabric 分开展示。')
 b=''
 for x,y,name,sub in [(90,220,'checkout','结算模块'),(820,220,'payments','支付模块'),(460,465,'shared','公共类型')]:
  b+=rect(x,y-25,130,30,fill='#eaf1fc',rx=0)+rect(x,y,280,120,fill='#f8fbff',rx=0)+text(x+140,y+47,name,23,weight=650)+text(x+140,y+81,sub,18,color=MUTED)
 b+=line(370,280,820,280,dashed=True)+text(595,258,'依赖',18)+path('M230 340 V525 H460',dashed=True)+text(339,507,'共享类型',17)+path('M960 340 V525 H740',dashed=True)
 authored('package','包图','代码按哪些包组织？包之间依赖什么？',b,category='数据与结构',note='用架构分组适配包图；文件夹式页签区分包与普通服务节点。')
 b=rect(160,155,900,460,fill='#f7faff',rx=0,extra='data-graph-role="container"')+text(185,190,'«structured classifier» Checkout',22,'start',weight=650)
 b+=box(260,300,260,105,'validator : Rules','内部部件')+box(675,300,260,105,'writer : Repository','内部部件')+rect(150,333,20,30,fill='white',rx=0)+rect(1050,333,20,30,fill='white',rx=0)
 b+=line(170,348,260,348)+line(520,348,675,348)+line(935,348,1050,348)+text(610,327,'连接器',17)+text(100,395,'请求端口',17)+text(1100,395,'存储端口',17)
 authored('composite','组合结构图','一个组件内部有哪些部件、端口和连接器？',b,category='数据与结构',note='嵌套架构表达；内部部件属于结构化分类器，不是外部部署节点。')
 b=box(80,255,260,100,'顾客界面')+box(470,255,260,100,'订单服务')+box(860,255,260,100,'支付服务')+line(340,305,470,305)+text(405,235,'1: submit()',17)+line(730,305,860,305)+text(795,235,'1.1: pay()',17)
 b+=line(860,405,730,405,dashed=True)+line(730,405,730,355,marker=None,dashed=True)+line(860,355,860,405,marker=None,dashed=True)+text(795,450,'1.2: result',17)+text(600,570,'消息顺序写在编号里；图中没有从上到下的时间轴',21,color=MUTED)
 authored('communication','通信图','对象怎样互相发消息？编号顺序是什么？',b,support='近似适配',note='上游明确标为近似支持；此处采用对象连线与消息编号说明，非专用通信图引擎。')
 b=''
 for y,label in [(230,'已发货'),(350,'已支付'),(470,'待支付')]:b+=line(220,y,1110,y,marker=None,color='#dbe4f0',dashed=True)+text(190,y+6,label,19,'end')
 for x,t in [(240,'0'),(440,'2'),(640,'4'),(840,'6'),(1040,'8')]:b+=line(x,190,x,540,marker=None,color='#e5ebf4',dashed=True)+text(x,582,t+' s',17)
 b+=path('M240 470 H440 V350 H840 V230 H1080',marker=None,color=ORANGE)+text(440,625,'支付事件：2 s',18)+text(840,625,'发货事件：6 s',18)
 authored('timing','时序波形图（Timing）','对象状态随时间如何变化？',b,support='近似适配',note='由时间轴适配，纵轴为状态、横轴为时间；与消息时序图不同。时间为教学设定。')
 b=circle(600,140,11)+line(600,151,600,195)+box(430,195,340,80,'ref  创建订单交互')+line(600,275,600,332)+diamond(600,385,90,53)+text(600,391,'创建成功？',19)
 b+=path('M510 385 H240 V505')+text(375,366,'否',18)+box(100,505,280,75,'ref  错误反馈交互')+path('M690 385 H960 V505')+text(835,366,'是',18)+box(820,505,280,75,'ref  支付交互')
 authored('interaction-overview','交互概览图','多个交互片段如何按条件组织？',b,support='近似适配',note='以活动流程连接 ref 交互片段；上游由流程图组合适配，未提供独立执行语义。')
 # Matrix, Gantt/timeline and radial concept map are deliberately not flowcharts.
 b=''
 cols=[70,430,675,920];widths=[360,245,245,245]
 for i,(x,w) in enumerate(zip(cols,widths)):b+=rect(x,165,w,70,fill='#dfebfb',rx=0)+text(x+w/2,208,['订单方案','访客下单','注册下单','企业采购'][i],20,weight=600)
 rows=[['账户要求','无需账户','个人账户','企业账户'],['收货地址','本次填写','可保存','多地址'],['审批步骤','无','无','有'],['发票信息','手动填写','可保存','企业抬头']]
 for j,row in enumerate(rows):
  for i,(x,w) in enumerate(zip(cols,widths)):b+=rect(x,235+j*75,w,75,fill='#fff' if j%2==0 else '#f4f7fc',rx=0)+text(x+w/2,280+j*75,row[i],19)
 authored('comparison','比较矩阵','多个方案在哪些维度上不同？',b,category='通用表达',note='表格型可视化，不是流程。示例功能为教学设定，不是实际产品能力评测。')
 b=''
 for i in range(7):x=280+i*130;b+=line(x,160,x,590,marker=None,color='#dce5f1')+text(x,139,f'第 {i+1} 周',17)
 for y,name,start,duration in [(220,'需求与设计',0,2),(325,'订单与支付',1,3),(430,'验证与上线',4,2)]:
  b+=text(230,y+30,name,20,'end')+rect(280+start*130,y,duration*130,48,fill=['#dceaff','#dff4ed','#fff0db'][[220,325,430].index(y)],stroke=BLUE)+text(280+start*130+duration*65,y+31,f'{duration} 周',18)
 b+=diamond(1060,555,15,15)+text(1020,628,'上线里程碑',18)
 authored('timeline','时间轴 / 甘特图','每项工作持续多久、何时开始、何时交付？',b,category='通用表达',note='合并同义入口：甘特横条表达持续时间，时间轴节点表达里程碑；时间为示例。')
 b=box(455,305,290,95,'订单系统','中心概念')
 for x,y,title,sub,cx in [(65,155,'用户','账户、地址、权限',390),(865,155,'交易','订单、支付、退款',810),(65,475,'履约','库存、物流、签收',390),(865,475,'运营','活动、分析、通知',810)]:
  sx=455 if x<400 else 745;ex=x+270 if x<400 else x
  b+=path(f'M{sx} 352 C{cx} 352 {cx} {y+45} {ex} {y+45}',marker=None,color=BLUE)+box(x,y,270,95,title,sub)
 authored('mindmap','思维导图 / 概念图','一个主题有哪些分支与关联概念？',b,category='通用表达',note='合并同义入口；曲线分支用于概念展开，不表达时间顺序。')

def main():
 p=argparse.ArgumentParser();p.add_argument('--fireworks',required=True);a=p.parse_args();fw=Path(a.fireworks).resolve();OUT.mkdir(parents=True,exist_ok=True)
 assert subprocess.check_output(['git','-C',str(fw),'rev-parse','HEAD'],text=True).strip()==COMMIT
 cli=fw/'scripts/fireworks.py'
 def command(*args):
  r=subprocess.run([sys.executable,str(cli),*map(str,args)],capture_output=True,encoding='utf-8',timeout=100)
  return r.returncode,json.loads(r.stdout or r.stderr)
 # Existing verified native examples are reused without claiming a new run.
 reused=[('architecture','系统架构图','系统由哪些服务与存储组成？','microservices-style3','系统与工程'),('agent','Agent 架构图','规划、模型、记忆、工具与评估如何协作？','chinese-style1','AI 与领域模式'),('memory','记忆架构图','记忆如何写入、合并、存储和检索？','mem0-style1','AI 与领域模式'),('c4','C4 评审视图','在同一抽象层级上，职责和协议是否清楚？','c4-review-canvas-style9','系统与工程'),('cloud','云部署视图','Region、VPC、工作负载与复制归属是什么？','cloud-fabric-style10','系统与工程'),('event','事件流视图','主题、处理器、消费组与异常出口怎样连接？','event-transit-style11','系统与工程'),('observability','可靠性 / 可观测性视图','黄金信号、关键路径与追踪如何关联？','ops-pulse-style12','系统与工程'),('multiagent','多 Agent 协作图','协调器如何分工、审查与汇总？','multi-agent-style5','AI 与领域模式'),('toolcall','工具调用图','模型如何选择工具、拿回结果并继续？','tool-call-style2','AI 与领域模式'),('memorytypes','Agent 记忆分类图','工作、情景、语义等记忆有什么层次？','agent-memory-types-style4','AI 与领域模式')]
 for key,title,q,old,cat in reused:
  for ext in ['svg','png','json','html','checks.json','layout.json']:
   f=P/'app/artifacts'/f'{old}.{ext}'
   if f.exists():shutil.copy2(f,OUT/f'{key}.{ext}')
  catalog.append(dict(key=key,title=title,question=q,category=cat,support='原生 JSON',origin='复用本项目已用固定版本原生生成器生成并检查的图例。',note='领域图是架构/数据流的专用视图；示例不代表生产环境实测。',input='json',source='diagram-layout-reference.md',example='既有固定样例'))
 def native(key,title,q,labels,cat='AI 与领域模式'):
  # Readable serpentine chain; no invented runtime behavior or measurements.
  nodes=[]
  pos=[(65,170),(455,170),(845,170),(845,430),(455,430),(65,430)]
  for i,(label,sub) in enumerate(labels):nodes.append(dict(id=f'n{i}',label=label,sublabel=sub,x=pos[i][0],y=pos[i][1],width=290,height=85,kind='double_rect' if '模型' in label or 'Agent' in label else 'rect'))
  edge_labels={'dataflow':['原始订单','有效订单','每日汇总','统计数据','报表数据'],'network':['HTTPS','放行流量','业务请求','数据库请求'],'rag':['问题文本','查询向量','相关片段','问题与证据','回答与来源'],'agentic-rag':['研究问题','检索计划','候选资料','充分证据','综合回答'],'agentic-search':['研究问题','子问题','搜索结果','已核对资料','研究发现']}
  arrows=[]
  for i in range(len(nodes)-1):arrows.append(dict(id=f'e{i}',source=f'n{i}',target=f'n{i+1}',source_port='right' if i<2 else 'bottom' if i==2 else 'left',target_port='left' if i<2 else 'top' if i==2 else 'right',flow='data',label=edge_labels[key][i]))
  spec=dict(schema_version=1,mode='architecture',style=1,width=1200,height=650,title=title,subtitle=q,text_policy='strict',quality_profile='showcase',nodes=nodes,arrows=arrows,footer='教学设定 · 使用 Fireworks 通用节点 / 连线生成器 · 无运行指标',footer_x=48,footer_y=620)
  (OUT/(key+'.json')).write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
  rc,result=command('render','architecture',OUT/(key+'.json'),OUT/(key+'.svg'),'--report',OUT/(key+'.layout.json'));assert rc==0,result
  catalog.append(dict(key=key,title=title,question=q,category=cat,support='原生 JSON',origin='本次编写 JSON，调用上游通用生成器；不是独立领域自动布局引擎。',note='领域流程示意，不代表模型或业务已实际运行。',input='json',source='diagram-layout-reference.md',example='本次教学案例'))
  if key in {'agentic-rag','agentic-search'}:catalog[-1]['note']='展示资料充足时的主路径；多轮重新规划与检索回路未展开，不代表完整 Agent 控制流程。'
  if key=='network':catalog[-1]['note']='逻辑网络与访问路径示意；不是自动发现的物理设备拓扑。'
 native('dataflow','数据流图','数据从哪里来，经过什么加工，保存到哪里？',[('订单事件','输入：订单编号与金额'),('清洗与去重','输出：有效订单'),('聚合计算','输出：每日汇总'),('分析仓库','保存汇总表'),('报表接口','读取统计结果'),('运营报表','展示数据')],'数据与结构')
 native('network','网络拓扑图','网络设备如何连接、流量经过哪些边界？',[('公网入口','外部 HTTPS 请求'),('防火墙','入口访问规则'),('负载均衡','分发到服务节点'),('应用子网','订单服务'),('数据子网','数据库访问边界')],'系统与工程')
 native('rag','RAG 检索增强图','回答怎样引用外部资料？',[('用户问题','需要资料的请求'),('查询向量化','生成查询表示'),('向量检索','找到相关片段'),('上下文拼接','组合问题与证据'),('LLM 模型','基于上下文回答'),('带来源回答','返回结果')])
 native('agentic-rag','Agentic RAG 图','Agent 如何决定检索与补充资料？',[('用户问题','复杂研究请求'),('Agent 规划','判断资料缺口'),('选择检索工具','搜索 / 向量库'),('评估证据','不足则规划下一轮'),('LLM 模型','依据证据综合'),('输出回答','附来源与限制')])
 native('agentic-search','Agentic Search 图','多步搜索如何规划、执行与综合？',[('研究目标','明确问题与边界'),('搜索规划','拆解子问题'),('搜索与计算','使用可用工具'),('核对资料','交叉检查来源'),('综合分析','整理发现'),('研究报告','交付结论与证据')])
 author_examples()
 for item in catalog:
  key=item['key'];svg=OUT/(key+'.svg')
  # All upstream checks are recorded faithfully, even if generic graph checks
  # cannot express a specialized notation. No failures are relabeled passed.
  rc,result=command('check',svg);(OUT/(key+'.checks.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
  item['checks']=result;item['allChecksPassed']=rc==0
  if item['input']=='svg':
   (OUT/(key+'.authorship.json')).write_text(json.dumps({'author':'本次 Agent','route':'Fireworks Skill 的 AI-authored SVG 路径','source':item['source'],'purpose':item['question'],'limit':item['note']},ensure_ascii=False,indent=2),encoding='utf-8')
  if not item['origin'].startswith('复用') or not (OUT/(key+'.html')).exists():
   rc,res=command('export-html',svg,OUT/(key+'.html'),'--title',item['title']);assert rc==0,res
   hp=OUT/(key+'.html');hp.write_text(hp.read_text(encoding='utf-8').replace('</head>','<meta name="description" content="技术图类型效果示例及原生离线查看器。"></head>'),encoding='utf-8')
 data={'commit':COMMIT,'date':'2026-09-15','count':len(catalog),'scope':'覆盖图型参考的14个主条目、UML映射的额外9个视图、4个工程视图和6个AI领域变体；同义名称合并。33为本展厅整理条目数，不是上游宣称的标准图型数量。','items':catalog}
 (OUT/'catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 env=os.environ.copy();env['FIREWORKS_PYTHON']=sys.executable
 # Render only new or changed SVGs, leaving previously verified outputs intact.
 temp=OUT/'render-pending';temp.mkdir(exist_ok=True)
 pending=[]
 for item in catalog:
  key=item['key'];dst=OUT/(key+'.png')
  if item['origin'].startswith('复用'):continue
  shutil.copy2(OUT/(key+'.svg'),temp/(key+'.svg'));pending.append(key)
 subprocess.run(['node',str(fw/'scripts/svg2png.js'),str(temp)],env=env,check=True,timeout=240)
 for key in pending:shutil.copy2(temp/(key+'.png'),OUT/(key+'.png'))
 # Remove only the explicitly created transient render files, no recursive delete.
 for f in temp.iterdir():f.unlink()
 temp.rmdir()
 (OUT/'receipt.json').write_text(json.dumps({'commit':COMMIT,'count':len(catalog),'native':sum(x['input']=='json' for x in catalog),'authored':sum(x['input']=='svg' for x in catalog),'allChecksPassed':sum(x['allChecksPassed'] for x in catalog),'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in OUT.iterdir() if f.is_file() and f.name not in {'receipt.json','visual-review.json'}}},ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'types':len(catalog),'native':sum(x['input']=='json' for x in catalog),'authored':sum(x['input']=='svg' for x in catalog),'checkIssues':[{x['key']:x['checks']} for x in catalog if not x['allChecksPassed']]},ensure_ascii=False))

if __name__=='__main__':main()
