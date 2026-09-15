"""Build a standalone, editable SVG guide for README and the research page."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1330" viewBox="0 0 1440 1330" role="img" aria-labelledby="title desc">
<title id="title">GSAP Skills：从 AI 使用指南到完整网页体验</title>
<desc id="desc">gsap-skills 指导 AI 编写代码，GSAP 在浏览器执行动画。Product Design 提供设计，Canvas UI 提供可选特效。耳机案例串联入场、滚动讲解、细节、搭配和试听计划。27个实验、8类技能、6项接入资料的验证范围分别标注。</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10" fill="#4b7168"/></marker></defs>
<rect width="1440" height="1330" fill="#f4f4ed"/>
<style>text{font-family:'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif;fill:#203b35}.muted{fill:#536b65}.white{fill:#fff}.accent{fill:#257460}</style>''']

def text(x,y,s,size=22,cls='',weight=400):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" class="{cls}">{escape(s)}</text>')

def box(x,y,w,h,fill='#ffffff',stroke='#d8e1d9'):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}"/>')

def arrow(path):
    parts.append(f'<path d="{path}" fill="none" stroke="#4b7168" stroke-width="2.5" marker-end="url(#arrow)"/>')

text(56,55,'009 / 开源研究手记 · 能力与体验引导',19,'accent',600)
text(56,112,'GSAP Skills：从使用指南到网页体验',43,weight=700)
text(56,157,'核心差异：GSAP 是动画引擎；gsap-skills 是教 AI 使用它的说明书。',24)

text(56,221,'01  能力架构',25,weight=700)
text(280,221,'设计决定表达什么，代码把表达变成可运行的网页。',21,'muted')
box(56,250,400,137)
text(80,286,'设计层 / Product Design',23,weight=700)
text(80,323,'依据产品目标组织内容与视觉',21)
text(80,359,'布局 · 配色 · 层次 · 操作路径',20,'muted')
box(505,250,879,137,'#e0eee5')
text(531,286,'指导层 / gsap-skills',25,weight=700)
text(531,323,'AI 读取技能文件 → 参考规则与示例 → 编写 GSAP 代码',23)
text(531,359,'提供插件用法、响应式与清理规范；本身不播放动画。',20,'muted')
arrow('M256 387V424H650V444')
arrow('M945 387V424H795V444')
box(468,448,504,76,'#203b35','#203b35')
text(506,495,'AI 编写网页内容、样式与交互代码',23,'white',600)
arrow('M720 524V552H256V579')
arrow('M720 524V579')
arrow('M720 552H1184V579')

for x,title,a,b,fill in [
    (56,'HTML / CSS · 页面结构','标题、图片、版式和操作入口','承载产品内容与阅读顺序','#ffffff'),
    (520,'GSAP · 动画运行引擎','随时间、滚动和输入改变属性','入场 · 缩放 · 转场 · 布局变化','#e0eee5'),
    (984,'Canvas UI · 可选视觉特效','用 WebGL / WebGPU 绘制效果','云雾 · 冰霜 · 水波 · 粒子','#ffffff')]:
    box(x,584,400,134,fill)
    text(x+23,622,title,22,weight=700)
    text(x+23,660,a,20)
    text(x+23,693,b,19,'muted')
text(56,751,'协作方式：GSAP 可连接特效参数来编排变化；耳机案例使用 GSAP，未接入 Canvas UI。',21,'muted')

text(56,817,'02  实际场景：MONO ONE 耳机新品发布页',25,weight=700)
steps=[('01','产品入场','引导注意力','Timeline / SplitText'),('02','滚动讲解','分步解释卖点','ScrollTrigger'),('03','细节放大','观察耳罩与头梁','图片位移与缩放'),('04','搭配选择','看清选择变化','Flip / 数值补间'),('05','试听计划','确认操作结果','弹窗 / 状态过渡')]
for i,(n,title,purpose,api) in enumerate(steps):
    x=56+i*269
    box(x,845,252,168)
    text(x+20,877,n,19,'accent',600)
    text(x+20,914,title,25,weight=700)
    text(x+20,950,purpose,21)
    text(x+20,986,api,18,'muted')
    if i<4: arrow(f'M{x+253} 927H{x+267}')
text(56,1053,'体验顺序：阅读详细介绍 → 打开场景实战 → 关闭动效作对比 → 回到实验室拆解效果',22,'accent',600)

box(56,1090,1328,181,'#203b35','#203b35')
text(82,1129,'03  已沉淀的成果与验证范围',24,'white',600)
text(82,1167,'27 个真实交互实验  /  8 类 AI 技能目录  /  6 项工具与外部接入资料  /  1 个完整产品页',22,'white')
text(82,1205,'已验证：主要浏览与选择流程。接入资料不等于运行验证；框架、设备与组合场景未穷举。',20,'white')
text(82,1242,'边界：技能不会新增动画引擎能力；开发效率、性能和业务收益尚未做对照评测。',20,'white')
text(56,1306,'原库 github.com/greensock/gsap-skills · 独立研究架构示意，非运行截图 · 2026-09-15',18,'muted')
parts.append('</svg>')
svg='\n'.join(parts)
for relative in ('assets/capability-guide.svg','app/assets/capability-guide.svg'):
    dest=ROOT/relative
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(svg,encoding='utf-8')
print('Guide updated: README asset and browser asset')
