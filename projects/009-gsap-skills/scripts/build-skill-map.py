"""Editable map of existing GSAP skills and a proposed customization workflow."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1900" viewBox="0 0 1600 1900" role="img" aria-labelledby="title desc">
<title id="title">GSAP Skill 能力与定制开发地图</title>
<desc id="desc">上游已有八类指导能力；定制时填写任务、触发条件、决策规则、工程约束和验收指标，按需组织 SKILL.md、references、scripts、assets，通过基线、实现、测量与反馈改进。上游文字指导与建议新增的执行验证明确区分。</desc>
<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10" fill="#346e61"/></marker></defs>
<rect width="1600" height="1900" fill="#f4f4ed"/>
<style>text{font-family:'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif;fill:#203b35}.muted{fill:#567068}.white{fill:white}.green{fill:#27735f}.orange{fill:#a3562d}</style>''']

def t(x,y,s,size=22,kind='',weight=400):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{kind}" font-weight="{weight}">{escape(s)}</text>')

def box(x,y,w,h,fill='#fff',stroke='#d7e0d8'):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}"/>')

def arrow(path,dash=False):
    parts.append(f'<path d="{path}" fill="none" stroke="#346e61" stroke-width="2.5" marker-end="url(#arr)"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')

t(56,52,'009 / 从研究资料到可复用的 AI 开发指导',20,'green',600)
t(56,111,'GSAP Skill：能力与定制开发地图',46,weight=700)
t(56,155,'核心价值：把使用经验变成可复用的决策规则，让 AI 少遗漏、少误用，并用实测判断结果。',25)
box(56,181,1488,65,'#203b35','#203b35')
t(80,223,'Skill 提供指导 → AI 生成代码 → GSAP 执行动画；真正的优化还需要检查与测量。',26,'white',600)

t(56,299,'01  上游已有：八类指导能力',28,weight=700)
t(970,299,'绿色区域 = 已有知识与示例',22,'green')
cards=[
('gsap-core','基础动画与适配','属性、缓动、错峰、媒体条件'),
('gsap-timeline','编排动画节奏','顺序、重叠、标签、播放控制'),
('gsap-scrolltrigger','把滚动连接到内容','触发、固定、联动、刷新与清理'),
('gsap-plugins','选择专用效果工具','文字、SVG、拖拽、Flip、物理'),
('gsap-utils','处理动画输入与数值','映射、限幅、吸附、插值'),
('gsap-react','接入 React 生命周期','useGSAP、作用域、卸载清理'),
('gsap-frameworks','接入其他框架','Vue / Svelte 生命周期与加载'),
('gsap-performance','减少不必要的工作','变换属性、复用、批量读写')]
for i,(name,title,body) in enumerate(cards):
    x=56+(i%4)*378;y=323+(i//4)*153
    box(x,y,354,132,'#e1eee5')
    t(x+20,y+32,name,21,'green',600)
    t(x+20,y+70,title,24,weight=600)
    t(x+20,y+108,body,19)

t(56,667,'02  你来定制：先填写这五项',28,weight=700)
t(966,667,'米色区域 = 建议新增的项目规则',22,'orange')
custom=[('目标与范围','做哪类页面？','优化卡顿或开发质量？','明确不处理的任务'),('触发与输入','何时加载此 Skill？','框架、GSAP 版本、设备','参考效果与现有代码'),('选择与参数','何时用 CSS / GSAP？','哪些场景需要插件？','时长、距离按设计配置'),('工程约束','高频更新复用动画','组件卸载与中断清理','保留功能与减少动效'),('验收与停止','怎样算优化成功？','测试设备、指标、容差','通过即停；失败再定位')]
for i,(title,*lines) in enumerate(custom):
    x=56+i*303
    box(x,692,276,169,'#fff0df','#e7d2b9')
    t(x+18,729,title,24,weight=600)
    for j,line in enumerate(lines): t(x+18,770+j*30,line,19)
t(56,897,'写规则的方式：适用条件 + 建议动作 + 原因 + 检查方法。必需约束与可选建议分开写。',23,'orange',600)

t(56,950,'03  优化规则示例：让 AI 知道何时改、怎么验',28,weight=700)
box(56,975,1488,246)
cols=[80,403,818,1240]
for x,label in zip(cols,['识别情形','指导 AI 的动作','希望减少的问题','验证证据']): t(x,1010,label,22,'green',600)
rows=[('只是移动位置','优先 x / y，而非 left / top','布局计算；需保持视觉一致','布局耗时与画面'),('鼠标连续更新','使用 quickTo 复用补间','反复创建与解析动画','帧耗时与创建情况'),('切换页面或组件','清理补间、触发器与监听','重复执行、残留状态','多次进入 / 退出'),('内容很长或设备较弱','减少同时运行；按需启停','无效更新与持续资源消耗','帧耗时与内存变化'),('偏好减少动态效果','提供静态路径与状态反馈','动态负担、功能依赖动画','关闭动效仍可操作')]
for i,row in enumerate(rows):
    y=1052+i*34
    for x,label in zip(cols,row):t(x,y,label,20)

t(56,1280,'04  如何落到自己的 Skill 文件',28,weight=700)
files=[('SKILL.md · 必需','name / description：何时使用','正文：目标、核心规则、引用入口'),('references/ · 按需','场景案例、版本差异、规则细节','只加载当前任务需要的资料'),('scripts/ · 按需新增','可重复的检查、测量与结果汇总','脚本必须运行验证；不是文字承诺'),('assets/ · 按需','可复用页面模板、样式与素材','放入产物使用，不作为指令加载')]
for i,(title,a,b) in enumerate(files):
    x=56+i*378
    box(x,1304,354,125)
    t(x+18,1340,title,22,weight=600)
    t(x+18,1378,a,19)
    t(x+18,1408,b,18,'muted')

t(56,1486,'05  建议建立的验证流程：让规范有结果依据',28,weight=700)
stages=[('同条件基线','记录设备、页面与指标'),('AI 实现 / 修改','按相关规则完成代码'),('运行与测量','看功能、帧耗时和清理'),('对比后决定','通过交付；退化修正')]
for i,(title,sub) in enumerate(stages):
    x=56+i*378
    box(x,1510,354,105,'#e1eee5')
    t(x+22,1551,title,24,weight=600)
    t(x+22,1587,sub,20)
    if i<3:arrow(f'M{x+355} 1562H{x+376}')
arrow('M1370 1616V1650H220V1618',True)
box(543,1630,515,42,'#f4f4ed','#f4f4ed')
t(565,1659,'反复出现且可验证的问题 → 更新对应规则',22,'green',600)

box(56,1700,1488,137,'#203b35','#203b35')
t(80,1739,'下一次定制的填写清单',25,'white',600)
t(80,1778,'页面类型 ____   技术栈 / 版本 ____   目标设备 ____   优化问题 ____   指标与容差 ____',24,'white')
t(80,1814,'先选任务与规则，再决定是否需要脚本和模板。保持 Skill 简洁，只加入能改变 AI 决策的信息。',21,'white')
t(56,1876,'边界：上游是文字指导，不含自动调优保证；新增测量流程需自行实现。参考 gsap-skills 固定版本及 skill-creator 规范。',19,'muted')
parts.append('</svg>')
for relative in ('assets/skill-development-map.svg','app/assets/skill-development-map.svg'):
    target=ROOT/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('\n'.join(parts),encoding='utf-8')
print('Updated skill development map for README and browser')
