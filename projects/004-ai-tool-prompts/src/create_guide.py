"""Draw an original architecture guide as matching PNG and editable SVG."""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont
import shutil

ROOT = Path(__file__).resolve().parents[1]
W, H = 2000, 1740
BG, PANEL, BORDER = '#0d141c', '#15222f', '#354758'
WHITE, MUTED, LIME, BLUE = '#eef3f8', '#b9c8d6', '#d0f778', '#91d5fa'
im = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">从已有 AI 产品的资料，到理解报告</title>',
       '<desc id="desc">两个仓库收录产品提示词和工具资料；研究者收集资料、解析信息、分析理解，最后整理能力说明、双库对比、案例和证据。x1xhlol 的应用与 Agent 案例较突出，asgeirtj 的厂商产品与版本资料较突出。材料分析不等于产品实测。</desc>']

def rect(x,y,w,h,fill,stroke=None,r=12):
    draw.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=stroke,width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="2"/>')

def text(x,y,value,size=28,color=WHITE,bold=False):
    font=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',size)
    draw.text((x,y),value,font=font,fill=color,anchor='lt')
    svg.append(f'<text x="{x}" y="{y}" font-family="Microsoft YaHei, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" dominant-baseline="text-before-edge">{escape(value)}</text>')

def line(points,color=BORDER,width=3):
    draw.line(points,fill=color,width=width)
    svg.append(f'<polyline points="{" ".join(str(x)+","+str(y) for x,y in points)}" fill="none" stroke="{color}" stroke-width="{width}"/>')

def arrow(x,y,x2,y2,color=LIME):
    line([(x,y),(x2,y2)],color,3)
    if x==x2: pts=[(x2-9,y2-11),(x2,y2),(x2+9,y2-11)]
    else: pts=[(x2-11,y2-9),(x2,y2),(x2-11,y2+9)]
    line(pts,color,3)

rect(0,0,W,H,BG,r=0)
text(70,43,'研究 004 / 架构引导图',25,LIME,True)
text(70,93,'从已有产品的资料，到理解报告',58,WHITE,True)
text(70,177,'依据提示词与工具材料，分析市场上已有 AI 产品的能力描述与工作方式。',29,MUTED)

rect(70,245,1860,124,PANEL,BORDER)
text(104,265,'研究对象：市场上已有的 AI 产品',32,WHITE,True)
text(104,318,'Manus · Kiro · Cursor · Lovable · Claude · ChatGPT · Gemini · Grok …',28,MUTED)
text(1505,284,'产品相关材料',28,BLUE)
arrow(1000,378,1000,415)

text(70,418,'01  资料来源',28,LIME,True)
text(335,418,'仓库负责收录与归档，供研究者查阅',27,MUTED)
for x,c in [(70,LIME),(1030,BLUE)]:
    rect(x,469,900,285,PANEL,BORDER)
    rect(x,469,900,5,c,r=0)
text(104,490,'本次研究',23,LIME,True)
text(104,529,'x1xhlol',40,WHITE,True)
text(104,584,'system-prompts-and-models-of-ai-tools',23,MUTED)
text(104,632,'偏向：应用与 Agent 产品的工作流程案例',28,LIME,True)
text(104,688,'例如 Manus / Kiro / Cursor：任务、工具、交付',26,MUTED)
text(1064,490,'对照已有研究',23,BLUE,True)
text(1064,529,'asgeirtj',40,WHITE,True)
text(1064,584,'system_prompts_leaks',23,MUTED)
text(1064,632,'偏向：厂商产品的版本、功能与模式档案',28,BLUE,True)
text(1064,688,'例如 Claude / ChatGPT / Gemini：版本与功能',26,MUTED)
rect(70,777,1860,92,'#1b2c2a')
text(104,791,'共同能力：收录提示词、工具说明及相关配置，提供可比较的研究材料。',28,LIME,True)
text(104,830,'两库收录有交叉；差异主要在覆盖与组织方式，不是两套不同的分析技术。',26,MUTED)
arrow(1000,880,1000,919)

text(70,925,'02  分析过程',28,LIME,True)
text(335,925,'研究者 / 我们完成：从材料中提炼有依据的理解',27,MUTED)
steps=[('1','收集资料',['选定产品与样本','保存来源、版本和文件','形成资料清单']),
       ('2','解析信息',['阅读文本，检查文件格式','识别角色、工具与流程','区分指令、接口与自述']),
       ('3','分析理解',['串起任务推进的方式','比较不同产品的做法','区分原文事实与推断']),
       ('4','汇集报告',['整合能力与原理说明','加入案例、对比与来源','用网页和图示表达'])]
for i,(num,title,rows) in enumerate(steps):
    x=70+475*i
    rect(x,982,435,213,PANEL,BORDER)
    text(x+25,1004,num,31,LIME,True)
    text(x+73,1004,title,33,WHITE,True)
    for j,row in enumerate(rows): text(x+25,1065+j*36,row,25,MUTED)
    if i<3: arrow(x+442,1088,x+466,1088,BLUE)
arrow(1000,1208,1000,1248)

rect(70,1270,1860,229,'#1a2921','#74974a')
text(104,1293,'03  最终成果：有来源、有解释、有边界的理解报告',34,LIME,True)
outputs=[('能力与原理','材料描述了什么能力','任务是如何组织的'),('产品与双库对比','共同点、差异与侧重点','哪些内容能够互相补充'),('具体案例与展示','Manus 等工作流程解读','中文网页、图示与教学案例'),('价值与证据','值得借鉴的方法与用途','来源、推断及未验证事项')]
for i,(a,b,c) in enumerate(outputs):
    x=104+459*i
    text(x,1360,a,29,WHITE,True)
    text(x,1405,b,25,MUTED)
    text(x,1443,c,25,MUTED)

text(70,1539,'如何理解它的价值？',29,LIME,True)
text(420,1539,'通过已有产品的设计样本，建立自己的理解，提炼可借鉴的工作方法。',28,WHITE)
line([(70,1604),(1930,1604)])
text(70,1630,'结论边界：材料中的能力描述 ≠ 产品实测；真实效果需要另行接入模型与工具进行验证。',26,MUTED)
text(70,1687,'依据两个仓库的固定版本与 Manus / Kiro / Cursor 样本整理 · 中文分析与图示为本研究原创 · 2026-09-15',21,MUTED)
svg.append('</svg>')
for folder in [ROOT/'assets', ROOT/'app/assets']:
    folder.mkdir(exist_ok=True)
    (folder/'research-guide.svg').write_text('\n'.join(svg),encoding='utf-8')
    im.save(folder/'research-guide.png')
print('Created research-guide.png and research-guide.svg (2000 × 1740)')
