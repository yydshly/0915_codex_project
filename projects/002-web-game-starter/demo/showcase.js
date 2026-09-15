const base = window.DEMO_RUNTIME_BASE || 'http://127.0.0.1:5174';
document.querySelector('#courtyard-link').href = `${base}/courtyard`;
document.querySelector('#mika-link').href = `${base}/dance-studio`;
const upstream = 'https://github.com/vibegameengine/web-starter-kit/blob/d5f62cb074b506697fb035c420415026bafbe792/';
const experiments = [
  { id: 'world', name: '完整 3D 场景', sub: '角色 · 灯光 · 音乐 · 特效', category: '场景与特效', route: '/', code: 'src/features/world/ui/GameScreen.tsx',
    hint: '拖动旋转视角 · 滚轮缩放 · 点击 Burst 触发动画与特效',
    try: '先转动视角观察场景，再点画面中的 Burst：角色舞蹈、音乐和粒子特效会一起启动。再次点击 Stop burst 停止。',
    value: '接入并展示已有模型、动作、声音与特效。人物是否精致、舞蹈是否自然，核心仍取决于另外制作或取得的资产；灯光与渲染调校也会影响结果。',
    mechanism: 'Three.js 绘制场景，React 组织组件；动画与音频响应操作，特效通过独立的渲染层与场景合成。' },
  { id: 'character', name: '角色与骨骼动画', sub: '姿态切换 · 动画播放', category: '角色动画', route: '/labs/character-debug-lab', code: 'src/features/character/ui/CharacterDebugScreen.tsx',
    hint: '在原版面板选择 Default pose / Idle / Macarena / Greeting',
    try: '依次点击默认姿态、待机、舞蹈与问候，观察同一角色如何切换动作。拖动视角，从侧面检查动作。',
    value: '让已有的三维人物播放已有动作。实际模型与舞蹈数据仍需自己制作或取得并适配；这里没有人物生成器或舞蹈创作编辑器。',
    mechanism: '角色模型带有骨骼，Mixamo 动画驱动这些骨骼。FBX 动画在构建时转成浏览器可加载的 GLB。' },
  { id: 'physics', name: '物理布娃娃', sub: '拖拽 · 抛掷 · 碰撞', category: '物理模拟', route: '/labs/ragdoll-lab', code: 'src/features/ragdoll/ui/RagdollLabScreen.tsx',
    hint: '使用场景内控制面板开始模拟 · R 重置 · H 显示或隐藏面板',
    try: '开启物理模拟，拖拽身体再松手。用原版面板切换地面、起始姿态与重力，观察受力和碰撞后的变化。',
    value: '身体倒地与碰撞不必逐帧制作动画。可用于受击、跌落、物理玩具和互动实验。',
    mechanism: 'Rapier 物理引擎计算每段肢体的刚体和关节约束；固定步长推进模拟，再将结果写回角色骨骼。' },
  { id: 'ground', name: '地面去重复', sub: '大面积纹理 · 远近观察', category: '材质实验', route: '/labs/anti-tiling-ground', code: 'src/features/anti-tiling-ground/ui/AntiTilingGroundLabScreen.tsx',
    hint: '拖动与缩放视角 · 观察远近地面的重复纹理和细节',
    try: '绕到地面远端，再拉近观察纹理。当前页面展示固定参数效果，没有专用的材质对比开关；低对比度素材的部分变化较细微。',
    value: '用一张较小的贴图覆盖大面积地面，同时减轻明显的“瓷砖式重复”，避免依赖一张巨大的背景图。',
    mechanism: '着色器组合坐标扰动、宏观色调变化、旋转叠层和随机采样；实际观感受贴图内容与参数影响。' },
  { id: 'terrain', name: '多层地形材质', sub: '泥土 · 道路 · 石块', category: '地形渲染', route: '/labs/layered-terrain', code: 'src/features/terrain-layers/ui/LayeredTerrainLabScreen.tsx',
    hint: '调整地形图层与覆盖范围 · 切换遮罩查看混合区域',
    try: '在同一块地面上切换泥土、道路和石块图层，调整石块覆盖范围，观察不同材质交界的位置。',
    value: '在一张地面网格上组合多种材质，做出道路与自然地面的过渡，可用于户外关卡和场景展示。',
    mechanism: '结合高度信息混合材质，保留石块边缘；各图层复用去重复采样，减少简单透明叠加的模糊感。' },
  { id: 'ui', name: '游戏界面组件', sub: '按钮 · 菜单 · 音频设置', category: '界面与交互', route: '/ui-kit/starter-showcase', code: 'src/features/ui-kit/index.ts',
    hint: '从组件目录选择示例 · 尝试按钮、滑块与菜单',
    try: '浏览组件目录，试用按钮、设置面板与滑块。这些示例展示控件的外观和交互，不代表已接入一个完整游戏。',
    value: '复用已有的游戏界面组件，减少从零编写按钮、暂停菜单与设置页的重复工作。',
    mechanism: 'React 组件组织控件；九宫格切片拉伸边框素材，界面缩放工具根据可用空间调整显示尺寸。' },
];
const frame = document.querySelector('#demo-frame');
const loading = document.querySelector('#stage-loading');
const nav = document.querySelector('#experiments');
const buttons = new Map();
for (const [index, experiment] of experiments.entries()) {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'experiment-button';
  const number = document.createElement('span');
  number.className = 'experiment-number';
  number.textContent = String(index + 1).padStart(2, '0');
  const label = document.createElement('span');
  label.className = 'experiment-label';
  label.textContent = experiment.name;
  const sub = document.createElement('small');
  sub.textContent = experiment.sub;
  label.append(sub);
  const arrow = document.createElement('span');
  arrow.className = 'experiment-arrow';
  arrow.textContent = '↗';
  arrow.setAttribute('aria-hidden', 'true');
  button.append(number, label, arrow);
  button.addEventListener('click', () => { window.location.hash = experiment.id; });
  nav.append(button);
  buttons.set(experiment.id, button);
}
function selectExperiment() {
  const id = window.location.hash.slice(1);
  const selected = experiments.find(item => item.id === id) || experiments[0];
  const number = String(experiments.indexOf(selected) + 1).padStart(2, '0');
  for (const [key, button] of buttons) {
    if (key === selected.id) button.setAttribute('aria-current', 'page');
    else button.removeAttribute('aria-current');
  }
  document.querySelector('#experiment-title').textContent = selected.name;
  document.querySelector('#experiment-category').textContent = `${number} / ${selected.category}`;
  document.querySelector('#experiment-count').textContent = `${number} / 06`;
  document.querySelector('#interaction-hint').textContent = selected.hint;
  document.querySelector('#try-text').textContent = selected.try;
  document.querySelector('#value-text').textContent = selected.value;
  document.querySelector('#mechanism-text').textContent = selected.mechanism;
  document.querySelector('#code-link').href = upstream + selected.code;
  document.querySelector('#open-original').href = base + selected.route;
  document.title = `${selected.name} · 3D 游戏能力实验室`;
  frame.title = `${selected.name}交互演示`;
  loading.hidden = false;
  frame.src = base + selected.route;
}
frame.addEventListener('load', () => { loading.hidden = true; });
document.querySelector('#reload').addEventListener('click', () => { loading.hidden = false; frame.src = frame.src; });
const fullscreenButton = document.querySelector('#fullscreen');
if (!document.fullscreenEnabled) fullscreenButton.hidden = true;
fullscreenButton.addEventListener('click', async () => {
  try { await document.querySelector('#stage').requestFullscreen(); }
  catch { window.open(document.querySelector('#open-original').href, '_blank', 'noopener'); }
});
window.addEventListener('hashchange', selectExperiment);
selectExperiment();
