"""Draw our reasoning journey from general guidance to domain-specific decisions."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[1]
out=['''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1530" viewBox="0 0 1500 1530" role="img" aria-labelledby="title desc">
<title id="title">从通用 Skill 到具体领域：我们的理解过程</title>
<desc id="desc">从区分 GSAP 与技能说明，到理解条件规则与效果决策，再由大模型结合领域目标筛选规则、选择方案和调整参数，最后通过运行验证沉淀经验。产品页、后台、阅读页说明同一原则可以有不同实现。</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10" fill="#407665"/></marker></defs>
<rect width="1500" height="1530" fill="#f5f4ed"/>
<style>text{font-family:'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif;fill:#203b35}.muted{fill:#526d65}.white{fill:white}.green{fill:#27705b}.orange{fill:#9d542d}</style>''']
def t(x,y,s,size=22,cls='',weight=400):
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" class="{cls}">{escape(s)}</text>')
def box(x,y,w,h,fill='#fff',stroke='#d7dfd5'):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{fill}" stroke="{stroke}"/>')
def arrow(d,dash=False):
    out.append(f'<path d="{d}" fill="none" stroke="#407665" stroke-width="2.5" marker-end="url(#arrow)"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')

t(52,48,'009 / 从“它能做什么”到“它如何指导 AI”',19,'green',600)
t(52,105,'通用规则，如何落到具体领域？',44,weight=700)
t(52,150,'大模型结合场景解释与应用规则，提出领域方案；方案是否合适，需要验证。',25)
t(52,209,'01  我们逐步厘清的四件事',25,weight=700)
journey=[('工具与指南','GSAP 执行动画','Skill 指导 AI 写代码'),('指导的方式','用条件、规则和示例','影响 AI 的实现选择'),('规则的对象','按技术问题组织规则','不预先写死每一种网页'),('领域化的角色','大模型结合用户任务','选择、组合并调整方案')]
for i,(title,a,b) in enumerate(journey):
    x=52+i*354
    box(x,229,332,119)
    t(x+18,264,f'{i+1}. {title}',23,weight=600)
    t(x+18,298,a,20)
    t(x+18,329,b,20,'muted')
    if i<3:arrow(f'M{x+334} 290H{x+352}')

t(52,405,'02  真正的连接：通用知识 + 具体情境 → 大模型判断',25,weight=700)
box(52,429,672,133,'#e0eee4')
t(76,464,'输入 A / 通用指导',24,'green',600)
t(76,502,'Skill：条件规则、API 用法、范例、适配与清理',22)
t(76,537,'例如：高频更新复用动画；退出时清理资源。',21,'muted')
box(766,429,682,133,'#fff0de','#e5d3ba')
t(790,464,'输入 B / 领域与项目情境',24,'orange',600)
t(790,502,'用户任务、页面内容、品牌风格、设备与现有技术栈',22)
t(790,537,'来自用户和项目资料；关键事实缺失时需要澄清。',21,'muted')
arrow('M388 562V591H650V616')
arrow('M1107 562V591H850V616')
box(205,620,1090,170,'#203b35','#203b35')
t(231,659,'大模型 / 将通用规则转成当前任务的实现方案',28,'white',600)
t(231,703,'识别用户任务 → 判断是否需要动效 → 筛选适用规则 → 组合工具 → 调整参数',23,'white')
t(231,740,'产品决策：为什么动、哪里动？      技术决策：如何实现、适配与清理？',22,'white')
t(231,772,'gsap-skills 主要指导 GSAP 技术实现；领域设计与跨工具选型需要额外判断。',20,'white')
arrow('M750 790V822H278V853')
arrow('M750 790V853')
arrow('M750 822H1222V853')

t(52,836,'',20)
domains=[
('产品介绍页 / 耳机案例','用户任务：了解卖点与细节','效果选择：分段讲解、局部放大','实现选择：GSAP / ScrollTrigger','参数适配：距离随内容和屏幕调整'),
('数据后台 / 应用示意','用户任务：快速操作与确认结果','效果选择：简短反馈、少干扰','实现选择：CSS；复杂重排考虑 Flip','参数适配：不阻碍连续操作'),
('内容阅读页 / 应用示意','用户任务：稳定、连续地阅读','效果选择：正文保持稳定','实现选择：静态页面或轻量 CSS','参数适配：避免强制滚动与持续运动')]
for i,(title,*lines) in enumerate(domains):
    x=52+i*472
    box(x,858,452,205)
    t(x+20,895,title,24,weight=600)
    for j,line in enumerate(lines):t(x+20,936+j*34,line,20,'muted' if j==3 else '')
t(52,1136,'同一原则：让变化帮助用户完成任务。具体领域可以得到不同效果，也可以决定不加动画。',23,'green',600)

arrow('M278 1064V1090H750V1106')
arrow('M750 1064V1106')
arrow('M1222 1064V1090H750')
box(205,1160,1090,88,'#e0eee4')
t(231,1196,'03  生成代码并运行验证',25,weight=600)
t(231,1230,'检查功能、可读性、减少动效、设备适配和性能；与目标或同条件基线对比。',22)
arrow('M750 1248V1284')
box(205,1289,1090,92,'#fff0de','#e5d3ba')
t(231,1325,'04  通过后交付；将反复验证的经验写回领域 Skill',25,weight=600)
t(231,1360,'沉淀格式：适用条件 → 决策原则 → 可调参数 → 验收方法；不把单次偏好变成通用禁令。',21)
arrow('M205 1335H25V494H50',True)
box(52,1420,1396,60,'#203b35','#203b35')
t(76,1458,'核心理解：Skill 提供可复用原则；大模型负责情境判断；代码实现方案；测试提供结果依据。',24,'white',600)
t(52,1510,'这是我们的理解与建议工作流，非上游自带的自动领域分类器；不会自动训练模型或自动改写 Skill。',20,'muted')
out.append('</svg>')
for name in ('assets/understanding-journey.svg','app/assets/understanding-journey.svg'):
    p=ROOT/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text('\n'.join(out),encoding='utf-8')
print('Understanding journey map generated')
