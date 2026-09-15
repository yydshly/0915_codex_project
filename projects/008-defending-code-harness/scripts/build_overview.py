"""Generate the same editable SVG diagram and standalone PNG from one layout.

Requires Pillow; default fonts are Microsoft YaHei on the Windows research host.
No upstream code or imagery is copied. All nodes are original research summaries.
"""
from pathlib import Path
from html import escape
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H = 1920, 3160
PAPER, INK, MUTED = '#f5f3ed', '#233530', '#59675f'
GREEN, LIGHT, LINE = '#246953', '#e5ede0', '#ced7c9'
ORANGE, SAND, WHITE = '#ac4b29', '#f5e6d7', '#fffef9'
FONT = Path('C:/Windows/Fonts/msyh.ttc')
BOLD = Path('C:/Windows/Fonts/msyhbd.ttc')
canvas = Image.new('RGB', (W, H), PAPER)
draw = ImageDraw.Draw(canvas)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">Defending Code 完整思路：相比直接让 AI 检测代码，多了什么</title>',
       '<desc id="desc">包含直接审查对照、人与模型的分工、八阶段执行闭环、工程支撑、四种定制深度、能力边界、后续复用与其他分支。所有内容为固定提交的源码研究归纳，未实测扫描。</desc>',
       f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
fonts = {}
def font(size, bold=False):
    key = (size, bold)
    if key not in fonts:
        fonts[key] = ImageFont.truetype(str(BOLD if bold else FONT), size)
    return fonts[key]

def rect(x, y, w, h, fill=WHITE, stroke=LINE, radius=8):
    draw.rounded_rectangle((x,y,x+w,y+h), radius=radius, fill=fill, outline=stroke, width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def text(x, y, value, size=23, fill=INK, bold=False):
    draw.text((x,y), value, font=font(size,bold), fill=fill, anchor='lt')
    # Align raster and vector using the same font ascent and glyph bounding box.
    bbox = font(size,bold).getbbox(value or ' ')
    baseline = y - bbox[1] + font(size,bold).getmetrics()[0]
    svg.append(f'<text x="{x}" y="{baseline}" fill="{fill}" font-family="Microsoft YaHei, PingFang SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}">{escape(value)}</text>')

def wrap(value, width, size=22, bold=False):
    lines=[]
    for para in value.split('\n'):
        line=''
        for char in para:
            if line and draw.textlength(line+char, font=font(size,bold)) > width:
                lines.append(line); line=char
            else: line+=char
        lines.append(line)
    return lines

def para(x, y, value, width, size=22, fill=MUTED, leading=34, bold=False):
    lines=wrap(value,width,size,bold)
    for i,line in enumerate(lines): text(x,y+i*leading,line,size,fill,bold)
    return y + len(lines)*leading

def arrow(points, color=GREEN, dashed=False, width=3):
    for (x1,y1),(x2,y2) in zip(points,points[1:]):
        if dashed:
            distance=math.hypot(x2-x1,y2-y1)
            for s in range(0,int(distance),15):
                a=s/distance; b=min(s+8,distance)/distance
                draw.line((x1+(x2-x1)*a,y1+(y2-y1)*a,x1+(x2-x1)*b,y1+(y2-y1)*b),fill=color,width=width)
        else: draw.line((x1,y1,x2,y2),fill=color,width=width)
    x,y=points[-1]; prev=points[-2]; angle=math.atan2(y-prev[1],x-prev[0])
    head=[(x,y),(x-11*math.cos(angle-.5),y-11*math.sin(angle-.5)),(x-11*math.cos(angle+.5),y-11*math.sin(angle+.5))]
    draw.polygon(head,fill=color)
    svg.append(f'<polyline points="{" ".join(f"{a},{b}" for a,b in points)}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="8 7"' if dashed else '')+'/>')
    svg.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in head)}" fill="{color}"/>')

def heading(y, num, title, note=''):
    text(60,y,num,22,GREEN,True); text(120,y-4,title,31,INK,True)
    if note: text(120,y+40,note,21,MUTED)

def card(x,y,w,h,tag,title,body,fill=WHITE,accent=GREEN,size=22):
    rect(x,y,w,h,fill)
    text(x+22,y+18,tag,19,accent,True)
    end=para(x+22,y+53,title,w-44,26,INK,36,True)
    end=para(x+22,end+12,body,w-44,size,MUTED,33)
    if end > y+h-10: raise ValueError(f'Card text overflow: {tag}: {end} > {y+h-10}')

# Header
text(60,42,'008 / DEFENDING CODE · 方法与工程能力总图',23,GREEN,True)
text(60,90,'相比直接让 AI 检测代码，多了什么？',53,INK,True)
text(60,166,'核心增量：把常规安全研究方法，组织成可执行、可复核、可积累的自动流程。',26,MUTED)

# A. Fair comparison
rect(60,220,1800,250)
text(84,241,'对照基线',20,GREEN,True)
text(84,286,'一次性代码审查',25,INK,True)
text(400,286,'代码 / 提问',24); arrow([(585,302),(655,302)],MUTED)
text(690,286,'模型阅读与推理',24); arrow([(909,302),(979,302)],MUTED)
text(1010,286,'候选问题与修改建议',24)
text(1425,286,'执行和复核需另外安排',22,MUTED)
text(84,342,'这个参考框架',25,GREEN,True)
text(400,342,'上下文 + 可运行目标',24,GREEN); arrow([(685,358),(745,358)])
text(775,342,'分阶段探索 + 独立验证',24,GREEN); arrow([(1085,358),(1145,358)])
text(1175,342,'复现证据 + 候选补丁 + 历史记录',24,GREEN)
para(84,408,'公平比较：能使用工具的 AI 也能完成这些步骤；框架把步骤、环境和验收固定下来，并不自动提高模型本身的分析能力。',1748,22,MUTED)

# B. Scope vs reasoning
heading(509,'01','谁决定关注什么？','你定方向；默认提示词给常见检查方法；模型从具体代码中推导实际路径与测试值。')
xs=[60,520,980,1440]
card(xs[0],598,420,215,'人 / 业务背景','定义真实范围','入口、权限、资产、需求与限制。\n例如：外部用户可上传文件；\n重点检查长度与格式边界。')
card(xs[1],598,420,215,'框架 / 默认指令','给出检查方向','零值、极大值、截断、字段矛盾；\n关注内存越界、释放后使用等。\n规定证据要求与排除条件。')
card(xs[2],598,420,215,'模型 / 具体推理','选择位置和用例','读到上限 1024 → 尝试\n0、1、1023、1024、1025；\n追踪分配、复制及前置校验。')
card(xs[3],598,420,215,'工具 / 观察结果','提供实际反馈','运行目标并记录诊断与状态。\n模型据此修正假设；业务对错\n需要有独立的规范和断言。')

# C. Main loop snake
heading(852,'02','从入口到证据，再到修复与下一轮','绿色箭头为主流程；橙色文字为反馈循环。编号中的“增加”对应相对一次性审查的工程增量。')
node_y=942; node_h=250
card(xs[0],node_y,420,node_h,'1 / 增加：明确范围','威胁建模与检查口径','入口 → 可控输入 → 权限 / 限制\n写清部署前提、优先级、排除项。\n产物：威胁模型与范围说明。\n减少无关或不可达路径误报。',LIGHT)
card(xs[1],node_y,420,node_h,'2 / 增加：任务分区','可运行环境 + Recon','固定版本，构建检测器生效的目标。\n按解析器 / 子系统分配搜索区域。\n可手写 focus_areas；Recon 可选。\n并行探索，不等于证明完整覆盖。',LIGHT)
card(xs[2],node_y,420,node_h,'3 / 增加：实际证据','分析 → 构造 → 运行','追踪危险路径，形成可检验假设。\n生成输入；看输出；最小化 PoC。\n提交文件、命令、诊断与去重说明。\n无证据 → 调整假设或输入继续试。',LIGHT)
card(xs[3],node_y,420,node_h,'4 / 增加：独立复核','Grade 在新环境复现','同一原始镜像；不继承环境改动。\n传递 PoC 与必要复现元数据。\n查非空、重复崩溃、非 OOM / 超时、\n项目堆栈与一致性；模型综合判断。',LIGHT)
for i in range(3): arrow([(xs[i]+420,node_y+125),(xs[i+1],node_y+125)])
second=1252
arrow([(1650,node_y+node_h),(1650,second)])
card(xs[3],second,420,node_h,'5 / 增加：去重与解释','Judge → Report','判断新增、较好样例或重复问题。\n流式 Judge 串行，另有签名聚类。\n分析可达性、影响与前提，独立评分。\n多轮 Triage：重排优先级与归属。',LIGHT)
card(xs[2],second,420,node_h,'6 / 增加：候选修复','Patch 单独启动','结合 PoC、源码与诊断修改根因。\n检查同类调用位置，尽量缩小改动。\n产物：patch.diff 与迭代记录。\n失败证据反馈 → 继续修改。',LIGHT)
card(xs[1],second,420,node_h,'7 / 增加：修复验收','执行检查 + 再次攻击','T0 能构建；T1 原输入不再触发。\nT2 现有测试通过，缺失则跳过。\n新智能体尝试绕过，默认 50 轮。\n可选风格评分仅供参考；人工审查。',LIGHT)
card(xs[0],second,420,node_h,'8 / 增加：持续积累','记录 → 校准 → 下一轮','保存已知问题、去重结果和修复。\n更新关注范围，减少重复研究。\n跨轮次分诊和按优先级修复。\n记录耗时、成本和真实发现质量。',LIGHT)
for i in range(3,0,-1): arrow([(xs[i],second+125),(xs[i-1]+420,second+125)])
arrow([(730,1504),(730,1545),(1190,1545),(1190,1504)],ORANGE,True)
text(797,1519,'验收失败 → 再修复',21,ORANGE,True)
arrow([(270,1504),(270,1577),(1650,1577)],ORANGE,True)
text(365,1591,'外循环：已知问题 / 修复 / 人工反馈 → 更新范围与验证器 → 再跑一轮',22,ORANGE)

# D. Infrastructure
heading(1660,'03','让上述步骤可以稳定运行的工程支撑')
infra=[('环境隔离','Docker / gVisor + 出口限制；\n不同阶段使用独立容器，\n约束自主操作和目标执行。'),('产物与可追溯性','PoC、命令、诊断、JSON、\n报告、补丁、交互记录落盘；\n便于人工复核与后续接入。'),('预算、重试与恢复','控制并行数、轮数与重试；\n记录检查点与会话，支持\n中断恢复，保留已完成成果。'),('效果校准与人工反馈','已知漏洞目标 + 正常对照；\n看误报、漏报、重复和成本，\n调整提示、范围与验收标准。')]
for i,(title,body) in enumerate(infra): card(xs[i],1720,420,214,'支撑 / '+str(i+1),title,body,size=21)

# E. customization
heading(1950,'04','定制不是都要改代码：先判断变化发生在哪一层')
custom=[('关注点变化','补充背景、--focus / --extra、\nfocus_areas 与误报规则。\n模型仍自己分析具体位置和用例。'),('同类目标变化','新增 Dockerfile、config.yaml\n和入口封装；保持文件 + ASAN\n约定时，通常无需改调度层。'),('问题类型变化','Web / 业务问题：重定义输入、\n失败信号、结果、去重与修复验收；\n提示词和检测代码需配套改。'),('模型或流程变化','替换 Claude CLI、工具循环、\n输出 / 会话 / 认证适配；\n若调整阶段顺序，则改调度代码。')]
for i,(title,body) in enumerate(custom): card(xs[i],2010,420,214,'定制深度 / '+str(i+1),title,body,fill=SAND,accent=ORANGE,size=21)
text(80,2227,'/customize 的作用：Claude 读改造指南 → 澄清需求 → 确认文件改动 → 修改框架 → 用预埋问题校准。',23,ORANGE)

# F. limits and extra considerations
heading(2292,'05','补齐边界：执行过、复现过、验证过，各自意味着什么？')
card(60,2355,880,310,'已有实现的边界','它提供证据链，不提供安全证明','• 默认针对 C/C++ 内存漏洞；现成调用层依赖 Claude Code。\n• 静态审查 / 分诊不执行目标；崩溃不自动等于可利用漏洞。\n• 独立会话可能使用同一模型，仍会共享认知偏差。\n• 没有 PoC 可能是未发现或运行中断；需同时核对任务状态。\n• 再次攻击有限；补丁过检不等于根因完全修好或能直接合并。',size=21)
card(980,2355,880,310,'后续项目还需补齐','把参考流程变成适合自己的测试系统','• 业务检测：需求来源、明确断言、初始数据与可重复状态。\n• 永久回归：动态补丁阶段不会自动为每个漏洞写长期测试。\n• 可观测性：区分正常拒绝、资源故障、未覆盖与真实问题。\n• 校准与成本：看漏报 / 误报 / 重复 / 耗时；不能只数报告。\n• 人工把关：影响、优先级、补丁语义、发布与责任归属。',fill=SAND,accent=ORANGE,size=21)

# G. supporting tracks and conclusion
rect(60,2695,1800,108,WHITE)
text(82,2715,'其他分支',22,GREEN,True)
text(250,2715,'交互静态审查：威胁建模 → 扫描 → 分诊 → 候选补丁（缺少动态复现证据）',22)
text(250,2755,'日志检测与响应：查日志 → 分析事件与影响 → 提出响应方案；示例为合成场景，不自动执行处置。',22)
rect(60,2830,1800,206,INK,INK)
text(85,2854,'我们的取舍 / 保留为后续开发参考',23,'#c8dcbd',True)
text(85,2898,'优先复用：明确范围 → 构造真实用例 → 独立复核 → 修复验收',34,WHITE,True)
text(85,2953,'小项目先跑通一个场景；规模增大后再加并行、去重、恢复和持续扫描。',24,'#d1ddca')
text(85,2995,'方法比较常规；当前新增研究价值有限。主要参考价值是流程自动化与证据管理，没有额外的模型智能保证。',22,'#d1ddca')
text(60,3065,'依据：anthropics/defending-code-reference-harness · d3bea6b · README / pipeline / customize / grade / patch_grade',20,MUTED)
text(60,3103,'2026-09-15 独立研究归纳 · 未运行漏洞扫描 · Web / 业务迁移为建议 · 已读版本声明不再维护 · 完整来源见研究网页',20,MUTED)

svg.append('</svg>')
(ROOT/'assets').mkdir(exist_ok=True)
(ROOT/'app').mkdir(exist_ok=True)
(ROOT/'app'/'overview-map.svg').write_text('\n'.join(svg),encoding='utf-8')
canvas.save(ROOT/'assets'/'overview-map.png')
print(f'Generated overview-map.svg and overview-map.png ({W} x {H}).')
