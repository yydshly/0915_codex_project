# 场景实战：MONO ONE 新品发布页

[打开在线场景](https://yydshly.github.io/0915_codex_project/009-gsap-skills/showcase/) · [能力全览](https://yydshly.github.io/0915_codex_project/009-gsap-skills/#overview)

[能力架构与研究汇总](understanding.md)：GSAP 与 gsap-skills 的差异、相关设计和特效工具的分工，以及完整引导图。

## 为什么这样展示

单个动画只回答“能怎样动”。本场景把它放入完整的浏览路径：第一眼看到产品 → 往下了解卖点 → 点击查看细节 → 选择搭配 → 生成试听计划。每个动效都对应一次内容解释或用户操作。

MONO 是本演示使用的虚构品牌，耳机为生成的概念视觉。页面没有真实销售、预约提交、个人信息收集或音频播放。

## 体验路径与实现

| 浏览动作 | 页面效果 | 使用的 GSAP 能力 | 产品用途 |
| --- | --- | --- | --- |
| 打开首页 | 标题、产品和入口按顺序出现 | Timeline、SplitText、核心补间 | 建立信息主次，突出产品 |
| 向下滚动 | 产品展示区固定，三段文案交替，图片靠近细节 | ScrollTrigger、pin、scrub、时间线 | 分步解释卖点，保持同一产品的连续性 |
| 点击安静模式 | 杂乱曲线逐步变平缓，背景线条收束 | MorphSVG、stagger、核心补间 | 让模式切换产生可理解的视觉反馈 |
| 选择设计细节 | 整机、耳罩、头梁的图片视野平滑移动 | scale、xPercent、yPercent | 引导注意力到当前描述的部分 |
| 选择随行组合 | 配件卡片从可选区移动到已选区，数量更新 | Flip、普通对象补间 | 看清选择带来的变化 |
| 预约试听 | 弹窗进入，选择偏好，生成本地完成状态 | 核心补间、原生 dialog | 操作闭环，明确反馈 |
| 页内导航与按钮 | 平滑定位、按钮轻微跟随 | ScrollToPlugin、quickTo | 衔接浏览，提供轻量反馈 |

顶部“动效说明”包含上述对应关系和直达入口。“动效：开启/关闭”可以对比同一网页；关闭后取消固定滚动，三段卖点改为普通连续阅读。系统开启减少动态效果时默认关闭动效。

## 运行与文件

复用原服务器，访问 /showcase/ 即可。所有脚本和图片都是本地相对路径；无 CDN 依赖。

- app/showcase/index.html：完整产品页、说明弹窗、试听流程。
- app/showcase/style.css：桌面与窄屏排版，静态阅读样式。
- app/showcase/app.js：滚动叙事、模式切换、局部展示、Flip 选择与弹窗。
- app/showcase/headphones.png：透明概念产品图。
- app/showcase/favicon.svg：独立页面图标。

产品图是二维透明 PNG。整体旋转和细节展示通过图片变换实现，并不等同于三维模型的自由视角。降噪区仅作视觉示意，不模拟实际音频性能。

## 已完成验证

在应用内浏览器中实际走通：

- 首屏产品加载与入场，页面导航定位。
- 向下滚动，第一段推进到第二段，再到第三段；产品保持固定展示。
- 关闭动效后，三段文案均可普通阅读；再次开启恢复滚动模式。
- 耳罩细节选择与缩放，安静模式状态切换。
- 随行组合切换后，配件移入已选区，数量变为 2。
- 试听计划携带当前组合；选择“30 分钟”“安静地听一张专辑”后生成正确本地摘要。
- 弹窗 Escape 关闭与焦点返回。
- 控制台没有错误或警告；桌面首屏、固定滚动区与细节区已截图查看。

窄屏布局已实现，未将当前浏览器验证表述为所有真实移动设备的兼容性测试。

## 素材记录

生成方式：内置 image_gen，由单个素材子任务生成；仅一次生成，无变体和重试。父任务检查后复制到项目。

最终素材路径：F:/codex_project/0915_codex_project/projects/009-gsap-skills/app/showcase/headphones.png

规格：1254 × 1254 PNG，透明 alpha。网页重复引用同一个本地素材。

最终提示词：

```text
Use case: product-mockup
Asset type: standalone transparent product image for a premium headphone launch website, not a website mockup.
Primary request: Create one photorealistic premium over-ear wireless headphone, matte black and brushed aluminum, with simple elegant industrial design.
Scene/backdrop: genuinely transparent alpha background. Isolated floating object, no floor and no shadow outside the object.
Composition/framing: Square image. Single complete headphone with both earcups and the entire headband visible. Three-quarter front view, slight diagonal tilt, floating centered, product fills about 85% of the frame with modest clear margins.
Style/medium: high-end crisp studio product photography.
Lighting/mood: sophisticated studio rim lighting, enough highlight and contrast to show black material details when placed on a pale ice gray webpage.
Materials/textures: rich matte black earcups and padded headband, tasteful brushed aluminum structural details, realistic cushions and precision construction.
Constraints: one product only. Preserve genuine alpha transparency, including the open space inside the headband. No props, words, logos, labels, watermarks, floor, scene, or external cast shadows.
```
