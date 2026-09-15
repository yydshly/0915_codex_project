# 有记忆的开场：创意与动态演示

[项目入口](../README.md) · [演示页面](../app/openings.html)

## 本轮结果

做了三种可点击、可重播的开场，页面同时列出六个方向。

| 方向 | 开头的动作 | 故事连接 | 完成情况 |
| --- | --- | --- | --- |
| 点亮工作台 | 点灯，场景从暗到明，揭示人物文案 | 身份卡、旧物抽屉、实验手册、作品、任务卡 | 已制作动态演示 |
| 拆开一封信 | 背景信封退后，信纸向上展开 | 自我介绍、旧信、观点、随信作品、回信 | 已制作动态演示 |
| 连接探索星图 | 点亮起点，逐段连接好奇、拆解、验证与创造 | 主人、坐标、日志、成果、共同探索 | 已制作动态演示 |
| 翻开旧物箱 | 选择一件旧物引出经历 | 由物及人 | 创意储备 |
| 启动一个作品 | 先展示实际成果再解释过程 | 倒叙呈现问题与方法 | 创意储备 |
| 印出第一期刊物 | 印出姓名、观点与作品 | 按目录进入个人故事 | 创意储备 |

开场图与第一人称文案均为原创创意示例，不描述用户真实经历。信封演示采用背景退后与信纸上移，不是实体信封的三维翻盖仿真。星图为叙事示意，不表示真实天文坐标。

页面提供直接查看结果、重播、切换与故事路线；尊重系统减少动态效果偏好，不播放声音，不保存用户数据。后三项没有标为已实现。

## 文件

- `app/openings.html`：三场景展台、六类开头对照、后续故事。
- `app/openings.css`：灯光揭示、纸张入场、星图连线及自适应布局。
- `app/openings.js`：切换、计时、重播、跳过和焦点管理。
- [台灯素材](../app/assets/opening-lamp.png)
- [信封素材](../app/assets/opening-letter.png)
- [星空素材](../app/assets/opening-stars.png)

素材通过内置 image_gen 生成，未使用 CLI；原图保留于生成目录，消费副本已保存到本项目。以下为最终提示词。

### 台灯提示词

```text
Create a single polished cinematic website background asset, 1536x1024 landscape, no UI, no lettering, no logo, no watermark. Scene: a curious inventor's real work desk at night, photographed like an exceptionally crafted miniature set with realistic tactile paper, graphite metal and warm amber lighting. Composition: angled articulated brass-and-black desk lamp occupying the right third, lamp on shining down onto a small open notebook with faint unlabeled sketches, pencil and compact mechanical prototype on the lower right. Left 52 percent is empty very dark charcoal-blue negative space for later HTML text overlay, no objects there. Desk surface spans bottom quarter. Lamp shade near x75% y28%, pool of warm light centered x70% y65%. No humans. Mood: invitation, curiosity, a quiet mind at work, restrained visual depth, rich shadows but clearly discernible lamp silhouette. Photoreal 3D diorama quality. One image only, not a collage.
```

### 信封提示词

```text
Create a single cinematic premium editorial website background asset, 1536x1024 landscape. No UI, no words, no letters, no logos, no watermark. Scene: one beautiful closed ivory cotton-paper envelope, small deep oxblood wax seal with an abstract simple non-letter relief, on a dark burgundy archival desk. It should feel like a personal letter preserved for years, intimate and intriguing. Composition: envelope is fully visible in the RIGHT 45 percent, centered x73% y52%, gently angled clockwise 8 degrees, macro tactile folded paper edges and authentic wax material, a subtle corner of another old blank note beneath it. LEFT 50 percent is calm dark burgundy near-black negative space for later HTML copy, with no objects. Soft dramatic light from upper right, premium quiet photographic still life, nuanced paper fibers, sophisticated balanced contrast. Large enough envelope to be the obvious interactive object. One image only, no collage.
```

### 星图提示词

```text
Create a single cinematic website background asset, 1536x1024 landscape, no text, no UI, no logos, no watermark. Theme: a personal observatory, mapping curiosity and discovery. Minimalist astronomical photographic art with deep midnight navy almost black space, restrained cyan-green haze on the RIGHT half, tiny white star points concentrated on right, one refined brass circular astrolabe-like ring / celestial navigation instrument on lower right, almost abstract physically crafted instrument. Left 55 percent must be very dark quiet negative space for later HTML typography. Do NOT draw any connecting constellation lines, labels, coordinate grids or axes; these will be overlaid interactively in code. Keep the center-right sky open for four animated story nodes. Elegant scientific instrument meets cinematic space, no planets, no bright nebula poster, no people, no rocket. One image, no collage.
```

## 验证范围

JavaScript 语法、站点本地链接、锚点、图片与描述检查通过。已在浏览器完成台灯、信纸与星图三个开场，确认台灯重播恢复初始状态、切换时后续故事同步更新，星图依次显示四个故事节点与连线。实际效果截图保存在项目 assets 目录。移动端、键盘操作与减少动态效果偏好尚未单独进行浏览器验证。

素材以图片呈现，动态效果由浏览器执行；不代表已经建成完整个人主页。当前仅本地展示，未部署本次更新。
