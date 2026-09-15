# 验证记录

日期：2026-09-15。环境：Windows、本地 HTTP、Playwright Chromium。

## 已验证

- 七个模块加载与反复切换，控制台无错误或警告。
- 时间线播放、暂停、倒放和 50% 进度定位。
- 缓动、文字与路径实验的进度定位。
- ScrollTrigger 75% 进度对应旋转角度大于 180°，回顶部可归零。
- Flip 两列切换、卡片换序后元素顺序正确。
- 拖拽方块的鼠标拖动、惯性运行、键盘方向键和复位。
- 切走滚动实验后 ScrollTrigger 实例数归零。
- 390px 手机视口逐一切换模块，无页面横向溢出。
- 减少动态效果偏好生效：文字实验不自动播放，内容完整显示。
- 实际桌面与手机截图已人工查看。

## 验证脚本

`scripts/verify.cjs` 使用运行环境提供的 Playwright，不属于网页生产依赖。先启动 8099 端口的本地演示，再在可解析 Playwright 的环境中执行 `node scripts/verify.cjs`。

截图为本地 Chromium 验证；未宣称在所有浏览器、真实手机设备或公开部署环境上完成测试。

## 能力全览扩展验证

- 27 个真实实验分别加载，控制台与本地资源请求无错误或警告。
- 检查全览为 27 张卡片、技能说明为 8 项、外部工具为 6 项。
- 检查 ScrambleText 最终文本、MorphSVG 路径变化、TextPlugin 文字替换。
- ScrollTo 可定位 C 章节；iframe 内真实 ScrollSmoother 移动原生滚动位置并更新内容变换。
- Observer 手势区域的按钮与键盘操作可切换内容。
- utils 输入 83 时角度为 299°、吸附为 80；quickTo 更新跟随对象。
- 组件挂载后动画数为 1，卸载后为 0，作用域外同名元素没有位移。
- Canvas 50% 时间位置对应 50% 圆环进度。
- 全部实验连续切换后回到全览，ScrollTrigger 和 Observer 实例数均为 0。
- 390px 视口下逐项检查 27 个实验，全览与接入页均无页面横向溢出。
- 真实窄屏媒体条件和减少动态效果偏好生效。
- 桌面全览、手机实验截图已查看；并非跨设备或性能跑分结论。

扩展验证脚本：scripts/verify-catalog.cjs。全览截图：assets/catalog.png；窄屏截图：assets/mobile-expanded.png。
