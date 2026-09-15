const scenes = {
  lamp: {
    world: "THE INVENTOR'S DESK", chapter: '一个还没完成的想法', title: ['这里的故事，','从一点好奇开始。'], description: '灯还没亮。桌上的笔记，记录着我如何把问题一步步变成作品。', action: '点亮台灯', object: '点击点亮', hint: '点亮台灯，揭示这间工作室的主人。', duration: 2200,
    revealChapter: '你好，欢迎来到我的工作台', revealTitle: ['我把好奇，','变成可以运行的作品。'], revealDescription: '从一个问题开始，查原理、做实验、记下结论。这就是我与世界打交道的方式。', revealHint: '光照亮的不只是桌面，还有这个人的做事方式。',
    memory: '一个亮起来的工作台，和喜欢动手的主人。', curiosity: '桌上还有什么？这个人做出了哪些东西？', audience: '研究者、开发者、设计师、动手创作者。', bridge: '灯光把你带到工作台前，接下来顺着桌上的物件认识这个人。',
    flow: [['人物','灯下的身份卡','先认识这里的主人与他关心的问题。'],['经历','抽屉里的旧物','每件物品，连接一个影响他的阶段。'],['文章','摊开的实验手册','阅读他的尝试、判断与反思。'],['产品','可启动的作品','亲眼看看，想法最后变成了什么。'],['联系','下一张任务卡','带着一个问题，开始新的合作。']]
  },
  letter: {
    world: 'A LETTER WAITING FOR YOU', chapter: '写给第一次来到这里的你', title: ['认识一个人，','可以从一封信开始。'], description: '有些经历，会改变我们看世界的方式。这封信里，藏着故事的起点。', action: '拆开这封信', object: '点击拆信', hint: '打开信件，看看这段自我介绍从哪里开始。', duration: 2300,
    revealChapter: '第一封信 · 关于一次转折', revealTitle: ['有些转折，','后来成了我的方向。'], revealDescription: '从那个让我停下来思考的问题开始，我想带你看看一路留下的选择、作品与答案。', revealHint: '信件建立亲近感，转折让人想继续了解。',
    memory: '一封像是专门写给自己的信。', curiosity: '是什么问题改变了这个人的方向？', audience: '有转折经历的创作者、写作者、独立工作者。', bridge: '把整站组织成几封连续的信，分别讲起点、选择、作品与未来。',
    flow: [['人物','第一封自我介绍','用自然的口吻，讲清楚你是谁。'],['经历','留下的几封旧信','每封信对应一个真实转折。'],['文章','寄出的观点','文章成为与世界持续交流的方式。'],['产品','随信附上的作品','把思考产生的实际结果交给访客。'],['联系','等待下一封回信','告诉对方可以为什么事联系你。']]
  },
  stars: {
    world: 'THE PERSONAL OBSERVATORY', chapter: '每一次探索，都有自己的坐标', title: ['看似无关的经历，','也能连成一片星空。'], description: '先点亮一个起点。看看好奇如何经过拆解与验证，最后变成创造。', action: '点亮第一颗星', object: '从这里出发', hint: '点亮起点，让四段探索逐渐连成一条路线。', duration: 3100,
    revealChapter: '好奇 · 拆解 · 验证 · 创造', revealTitle: ['每一次探索，','都是下一次的起点。'], revealDescription: '这些连接，构成了我理解问题的方式。接下来，可以沿着每个坐标走进具体的经历与作品。', revealHint: '路径有了形状，零散的经历也有了共同方向。',
    memory: '几颗星连成一条属于这个人的探索路线。', curiosity: '每个坐标后面，发生过什么？', audience: '跨领域研究者、持续学习者、探索型创作者。', bridge: '用星图呈现探索方向，以节点进入经历与成果，同时保留清楚的文字目录。',
    flow: [['人物','观测站的主人','介绍持续关注的问题与方向。'],['经历','沿途的坐标','每个节点是一段经历与改变。'],['文章','观测日志','记录一次发现，以及得出判断的过程。'],['产品','探索带回的成果','展示研究产生的工具、作品与方法。'],['联系','下一次共同探索','邀请访客带着问题与你连接。']]
  }
};
const stage = document.getElementById('experience');
const tabs = [...document.querySelectorAll('[data-scene]')];
const play = document.getElementById('play');
const objectTrigger = document.getElementById('object-trigger');
const replay = document.getElementById('replay');
const skip = document.getElementById('skip-motion');
const continueLink = document.getElementById('continue');
const copy = document.querySelector('.scene-copy');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let current = 'lamp';
let timer;
let runId = 0;
function setText(id, text) { document.getElementById(id).textContent = text; }
function setTitle(lines) {
  const title = document.getElementById('scene-title');
  title.replaceChildren(document.createTextNode(lines[0]), document.createElement('br'), document.createTextNode(lines[1]));
}
function actionLabel(text) {
  play.replaceChildren(document.createTextNode(text + ' '));
  const arrow = document.createElement('span'); arrow.textContent = '↗'; play.append(arrow);
}
function reset() {
  clearTimeout(timer); runId++;
  const s = scenes[current];
  stage.dataset.state = 'idle'; copy.classList.remove('content-change');
  setText('chapter', s.chapter); setTitle(s.title); setText('scene-description', s.description);
  setText('stage-hint', s.hint); setText('state-label', '等待你的第一步');
  actionLabel(s.action); play.disabled = false; play.hidden = false;
  objectTrigger.hidden = false; objectTrigger.disabled = false;
  objectTrigger.setAttribute('aria-label', s.action); setText('object-label', s.object);
  replay.hidden = true; skip.hidden = false; continueLink.hidden = true;
  document.querySelector('.letter-paper').setAttribute('aria-hidden','true');
  setText('announcement','');
}
function complete(token = runId) {
  if (token !== runId) return;
  clearTimeout(timer);
  const s = scenes[current];
  const hadTriggerFocus = document.activeElement === play || document.activeElement === objectTrigger || document.activeElement === skip;
  stage.dataset.state = 'revealed';
  setText('chapter',s.revealChapter); setTitle(s.revealTitle); setText('scene-description',s.revealDescription);
  setText('stage-hint',s.revealHint); setText('state-label','开场完成');
  copy.classList.add('content-change');
  play.hidden = true; objectTrigger.hidden = true; skip.hidden = true;
  replay.hidden = false; continueLink.hidden = false;
  document.querySelector('.letter-paper').setAttribute('aria-hidden',String(current !== 'letter'));
  setText('announcement',s.revealTitle.join('') + ' 可以重播，或继续查看后续故事。');
  if (hadTriggerFocus) continueLink.focus({preventScroll:true});
}
function start() {
  if (stage.dataset.state !== 'idle') return;
  const token = ++runId;
  if (reducedMotion.matches) { complete(token); return; }
  stage.dataset.state = 'running';
  stage.style.setProperty('--duration', scenes[current].duration+'ms');
  play.disabled = true; objectTrigger.disabled = true;
  setText('state-label','故事正在展开'); setText('announcement','故事正在展开。');
  timer = setTimeout(() => complete(token), scenes[current].duration);
}
function select(name, moveFocus = false) {
  if (!scenes[name]) return;
  current = name;
  stage.className = 'stage theme-' + name;
  stage.setAttribute('aria-labelledby','tab-'+name);
  for (const tab of tabs) {
    const selected = tab.dataset.scene === name;
    tab.setAttribute('aria-selected',String(selected)); tab.tabIndex = selected ? 0 : -1;
  }
  const s=scenes[name];
  document.getElementById('scene-image').src='assets/opening-'+name+'.png';
  setText('world-label',s.world);
  for(const key of ['memory','curiosity','audience','bridge']) setText(key,s[key]);
  const flow=document.getElementById('story-flow'); flow.replaceChildren();
  s.flow.forEach(([type,title,body],i)=>{
    const li=document.createElement('li');
    const label=document.createElement('span'); label.textContent=String(i+1).padStart(2,'0')+' / '+type;
    const heading=document.createElement('h3'); heading.textContent=title;
    const p=document.createElement('p'); p.textContent=body;
    li.append(label,heading,p); flow.append(li);
  });
  reset();
  if(moveFocus) document.getElementById('tab-'+name).focus();
}
play.addEventListener('click',start); objectTrigger.addEventListener('click',start);
skip.addEventListener('click',()=>complete()); replay.addEventListener('click',()=>{reset();play.focus({preventScroll:true});});
tabs.forEach((tab,index)=>{
  tab.addEventListener('click',()=>select(tab.dataset.scene));
  tab.addEventListener('keydown',event=>{
    let next;
    if(event.key==='ArrowRight')next=(index+1)%tabs.length;
    if(event.key==='ArrowLeft')next=(index+tabs.length-1)%tabs.length;
    if(event.key==='Home')next=0;
    if(event.key==='End')next=tabs.length-1;
    if(next!==undefined){event.preventDefault();select(tabs[next].dataset.scene,true);}
  });
});
document.querySelectorAll('[data-jump]').forEach(button=>button.addEventListener('click',()=>{
  select(button.dataset.jump,true);
  document.querySelector('.selector').scrollIntoView({behavior:reducedMotion.matches?'auto':'smooth',block:'start'});
}));
reducedMotion.addEventListener('change',event=>{if(event.matches&&stage.dataset.state==='running')complete();});
select('lamp');
