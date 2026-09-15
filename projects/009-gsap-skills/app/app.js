(() => {
  'use strict';
  const $ = (selector) => document.querySelector(selector);
  const stage = $('#stage');
  if (![window.gsap, window.ScrollTrigger, window.SplitText, window.MotionPathPlugin, window.DrawSVGPlugin, window.Flip, window.Draggable, window.InertiaPlugin].every(Boolean)) {
    $('#error').hidden = false;
    return;
  }
  gsap.registerPlugin(ScrollTrigger, SplitText, MotionPathPlugin, DrawSVGPlugin, Flip, Draggable, InertiaPlugin);
  $('#version').textContent = gsap.version;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0, context, timeline, cleanup = () => {}, draggingSlider = false, resizeTimer, activeView = 'overview';
  const demos = [
    { name: '时间线编排', engine: 'Timeline', skill: 'gsap-timeline',
      description: '圆、方块和圆环依次入场，再一起转动。多个动作被放在同一条时间线上，像剪视频一样安排先后与重叠。',
      use: '首屏入场、产品发布、分步骤引导', note: '用时间线和位置参数编排动作；重播、暂停、倒放都控制同一个实例。',
      hint: '试试暂停、倒放，或拖动进度条。你可以控制整个动画的任意一刻。',
      code: 'const tl = gsap.timeline();\ntl.from(shapes, {\n  y: 90, scale: 0.3,\n  autoAlpha: 0, stagger: 0.18\n});\ntl.to(shapes, { rotation: 360 });',
      build() {
        stage.innerHTML = '<span class="stage-label">CHOREOGRAPHY / 01</span><div class="composition"><div class="shape circle">g</div><div class="shape square">s</div><div class="shape outline">ap</div></div><div class="timeline-caption">THREE SHAPES. ONE TIMELINE.</div>';
        return gsap.timeline({ paused: true, defaults: { duration: 1, ease: 'power3.out' } })
          .from('.shape', { y: 90, scale: .3, autoAlpha: 0, rotation: -60, stagger: .18 })
          .to('.shape', { rotation: 360, y: -20, stagger: .1, ease: 'back.inOut(1.4)' }, '+=.25')
          .to('.shape', { y: 0, scale: 1.12, stagger: .12, duration: .6 })
          .to('.shape', { scale: 1, duration: .5 });
      }
    },
    { name: '缓动对比', engine: 'Easing', skill: 'gsap-core',
      description: '同样的距离和时长，速度的变化会带来不同的感觉：匀速、轻轻停下、弹簧回弹、落地反弹。',
      use: '按钮反馈、弹窗出现、物体落下', note: '使用真实存在的缓动名称；优先用 x、y 等变换属性移动元素，减少布局计算。',
      hint: '四个方块同时出发。把速度改成 0.5×，更容易看出它们的区别。',
      code: 'gsap.to(box, {\n  x: distance, duration: 2.5,\n  ease: "elastic.out(1, 0.4)"\n});',
      build() {
        const eases = ['none', 'power3.out', 'elastic.out(1, 0.4)', 'bounce.out'];
        stage.innerHTML = '<span class="stage-label">SAME DISTANCE / DIFFERENT FEEL</span><div class="races">' + ['匀速 · linear', '减速 · ease out', '弹簧 · elastic', '弹跳 · bounce'].map(label => `<div class="race"><span>${label}</span><div class="track"><div class="racer"></div></div></div>`).join('') + '</div>';
        const tl = gsap.timeline({ paused: true });
        stage.querySelectorAll('.racer').forEach((el, i) => tl.to(el, { x: () => el.parentElement.clientWidth - 35, duration: 2.8, ease: eases[i] }, 0));
        return tl;
      }
    },
    { name: '滚动联动', engine: 'ScrollTrigger', skill: 'gsap-scrolltrigger',
      description: '在预览框里上下滚动，方块就随之转动、变形，文字逐渐出现。滚动位置就是动画的进度。',
      use: '滚动叙事、产品细节展示、视差页面', note: '将 ScrollTrigger 挂在主时间线上。固定外层容器，动画作用于内部元素；布局改变后刷新位置。',
      hint: '在预览框内滚动或滑动；也可以用下面的按钮与进度条体验。',
      code: 'gsap.timeline({ scrollTrigger: {\n  scroller: viewport,\n  trigger: panel, pin: true,\n  scrub: true, end: "+=650"\n}}).to(box, { rotation: 360 });',
      build() {
        stage.innerHTML = '<div class="scroll-viewport" tabindex="0" role="region" aria-label="滚动动画预览，使用滚轮或上下方向键"><div class="scroll-meter"><div></div></div><div class="scroll-content"><div class="scroll-pin"><div class="scroll-orbit">g.</div><div class="scroll-copy">往下滚动，让动画继续。</div></div><p class="scroll-end">向上滚动，动画也会倒放 ↑</p></div></div>';
        const viewport = $('.scroll-viewport');
        const tl = gsap.timeline({ scrollTrigger: { id: 'lab-scroll', scroller: viewport, trigger: '.scroll-pin', start: 'top top', end: '+=650', pin: true, scrub: true, onUpdate: self => {
          $('#progress').value = Math.round(self.progress * 1000);
          $('#progress-label').textContent = Math.round(self.progress * 100) + '%';
          gsap.set('.scroll-meter>div', { scaleX: self.progress });
        } } });
        tl.to('.scroll-orbit', { rotation: 180, borderRadius: '50%', scale: 1.25, duration: 1, ease: 'none' })
          .to('.scroll-orbit', { rotation: 360, backgroundColor: '#b7a3ed', scale: .8, duration: 1, ease: 'none' })
          .fromTo('.scroll-copy', { opacity: .25, y: 15 }, { opacity: 1, y: 0, duration: 2, ease: 'none' }, 0);
        $('#special-controls').innerHTML = '<button id="scroll-next">向下滚一段 ↓</button><button id="scroll-top">回到顶部 ↑</button>';
        $('#scroll-next').onclick = () => viewport.scrollBy({ top: 180, behavior: reduced.matches ? 'instant' : 'smooth' });
        $('#scroll-top').onclick = () => viewport.scrollTo({ top: 0, behavior: reduced.matches ? 'instant' : 'smooth' });
        cleanup = () => tl.scrollTrigger?.kill();
        return tl;
      }
    },
    { name: '文字拆分', engine: 'SplitText', skill: 'gsap-plugins',
      description: '一句文字被拆成单个字符，每个字符都可以独立移动和旋转，随后以短暂的时间差依次出现。',
      use: '品牌标题、章节切换、重点文字揭示', note: '只拆分需要动画的部分；保留无障碍文本，在结束使用时恢复原始结构。',
      hint: '文字使用真正的 SplitText 插件拆分。重播或倒放，观察字符的错峰变化。',
      code: 'const split = SplitText.create(title, {\n  type: "chars,words", aria: "auto"\n});\ngsap.from(split.chars, {\n  y: 70, rotation: 12,\n  opacity: 0, stagger: 0.09\n});',
      build() {
        stage.innerHTML = '<span class="stage-label">EVERY LETTER HAS A MOMENT</span><div class="text-demo"><div class="split-heading">Make it move.</div><p>让每一个字，都有自己的节奏。</p></div>';
        const split = SplitText.create('.split-heading', { type: 'chars,words', aria: 'auto' });
        cleanup = () => split.revert();
        return gsap.timeline({ paused: true }).from(split.chars, { y: 70, rotation: 12, opacity: 0, stagger: .09, duration: .9, ease: 'back.out(1.6)' }).from('.text-demo p', { y: 12, opacity: 0, duration: .7 }, '-=.3');
      }
    },
    { name: '沿路径运动', engine: 'MotionPath + DrawSVG', skill: 'gsap-plugins',
      description: '小圆点沿着一条弯曲的 SVG 路径移动，线条也同步被画出来。你可以自由倒放或停在任意位置。',
      use: '路线展示、流程引导、图形描边', note: '注册所用插件；MotionPath 负责沿路径移动，DrawSVG 负责显示线条的可见部分。',
      hint: '拖动进度条，观察圆点与线条是否同步。路径缩放后仍保持对齐。',
      code: 'tl.fromTo(path, { drawSVG: 0 },\n  { drawSVG: "100%", duration: 4 });\ntl.to(dot, { duration: 4, ease: "none",\n  motionPath: { path, align: path,\n    alignOrigin: [0.5, 0.5] }\n}, 0);',
      build() {
        stage.innerHTML = '<span class="stage-label">FOLLOW YOUR OWN PATH</span><svg class="path-svg" viewBox="0 0 560 280" role="img" aria-label="圆点沿 S 形曲线运动"><path d="M45 195 C70 25 195 15 215 135 S355 270 385 130 S500 50 515 140" fill="none" stroke="#c9d1bd" stroke-width="3" stroke-dasharray="5 7"/><path id="motion-path" d="M45 195 C70 25 195 15 215 135 S355 270 385 130 S500 50 515 140" fill="none" stroke="#779a43" stroke-width="4"/><circle id="path-dot" cx="0" cy="0" r="13" fill="#b7a3ed" stroke="#293422" stroke-width="2"/></svg>';
        return gsap.timeline({ paused: true }).fromTo('#motion-path', { drawSVG: 0 }, { drawSVG: '100%', duration: 4, ease: 'none' }, 0).to('#path-dot', { duration: 4, ease: 'none', motionPath: { path: '#motion-path', align: '#motion-path', alignOrigin: [.5, .5] } }, 0);
      }
    },
    { name: '布局变换', engine: 'Flip', skill: 'gsap-plugins',
      description: '点击按钮，卡片从三列切换为两列，或交换顺序。每张卡片平滑移动到新位置，帮助你看清布局变化。',
      use: '相册切换、卡片排序、列表与网格切换', note: '先记录元素的位置，再改变页面布局，最后用 Flip.from() 补出过渡动画。',
      hint: '连续切换也可以；数字代表同一张卡片，方便你跟踪它去了哪里。',
      code: 'const state = Flip.getState(cards);\ngrid.classList.toggle("list");\nFlip.from(state, {\n  duration: 0.8, ease: "power2.inOut",\n  absolute: true\n});',
      build() {
        stage.innerHTML = '<span class="stage-label">NEW LAYOUT / SAME ELEMENTS</span><div class="flip-grid">' + ['01', '02', '03', '04', '05', '06'].map(n => `<div class="tile">${n}</div>`).join('') + '</div>';
        $('#special-controls').innerHTML = '<button id="layout" class="primary">切换为两列</button><button id="shuffle">交换卡片顺序</button>';
        let flipTween;
        const change = (reorder) => {
          if (flipTween) flipTween.progress(1).kill();
          const cards = stage.querySelectorAll('.tile'), grid = $('.flip-grid');
          const state = Flip.getState(cards);
          if (reorder) grid.append(grid.firstElementChild);
          else grid.classList.toggle('list');
          $('#layout').textContent = grid.classList.contains('list') ? '切换为三列' : '切换为两列';
          flipTween = Flip.from(state, { duration: reduced.matches ? 0 : .85, absolute: true, ease: 'power2.inOut', stagger: .025 });
        };
        $('#layout').onclick = () => change(false);
        $('#shuffle').onclick = () => change(true);
        cleanup = () => flipTween?.kill();
        return null;
      }
    },
    { name: '拖拽与惯性', engine: 'Draggable + Inertia', skill: 'gsap-plugins',
      description: '按住方块拖动，松手后它会沿着你的方向继续滑行，然后慢慢停下。虚线框限制了它的活动范围。',
      use: '自由画布、拖拽交互、可移动面板', note: '用 Draggable 处理拖拽，InertiaPlugin 处理松手后的惯性，并设置活动边界。',
      hint: '拖住方块快速甩一下。也支持键盘：聚焦方块后按方向键，Home 回到起点。',
      code: 'Draggable.create(box, {\n  type: "x,y", bounds: container,\n  inertia: true, edgeResistance: 0.8\n});',
      build() {
        stage.innerHTML = '<span class="stage-label">GRAB / THROW / RELEASE</span><div class="drag-boundary"><button class="drag-object" aria-label="可拖动方块，方向键移动，Home 复位">✣</button><span class="drag-help">拖我一下</span></div>';
        const box = $('.drag-object'), bounds = $('.drag-boundary');
        const drag = Draggable.create(box, { type: 'x,y', bounds, inertia: !reduced.matches, edgeResistance: .8, overshootTolerance: 0 })[0];
        box.addEventListener('keydown', event => {
          const moves = { ArrowLeft: [-25, 0], ArrowRight: [25, 0], ArrowUp: [0, -25], ArrowDown: [0, 25] };
          if (!moves[event.key] && event.key !== 'Home') return;
          event.preventDefault();
          drag.tween?.kill();
          const move = moves[event.key] || [0, 0];
          const x = event.key === 'Home' ? 0 : gsap.utils.clamp(drag.minX, drag.maxX, Number(gsap.getProperty(box, 'x')) + move[0]);
          const y = event.key === 'Home' ? 0 : gsap.utils.clamp(drag.minY, drag.maxY, Number(gsap.getProperty(box, 'y')) + move[1]);
          gsap.set(box, { x, y }); drag.update();
        });
        $('#special-controls').innerHTML = '<button id="drag-reset">回到起点</button>';
        $('#drag-reset').onclick = () => { drag.tween?.kill(); gsap.set(box, { x: 0, y: 0 }); drag.update(); };
        cleanup = () => { drag.tween?.kill(); drag.kill(); };
        return null;
      }
    }
  ];
  demos.push(...window.createExtraDemos({stage, $, reduced, setCleanup: fn => { cleanup = fn; }}));
  window.renderCapabilityCatalog(demos);
  function dispose() {
    cleanup(); cleanup = () => {};
    gsap.killTweensOf(stage.querySelectorAll('*'));
    context?.revert(); context = null; timeline = null;
    stage.innerHTML = '';
  }
  function showView(view, index = current, autoPlay = true) {
    activeView = view;
    $('#overview').hidden = view !== 'overview';
    $('#guides').hidden = view !== 'guides';
    $('.workspace').hidden = view !== 'lab';
    for (const name of ['overview','lab','guides']) {
      $('#show-'+name).classList.toggle('active', name === view);
      $('#show-'+name).setAttribute('aria-pressed', String(name === view));
    }
    if (view === 'lab') select(index, autoPlay); else dispose();
    const hash = view === 'lab' ? '#demo-' + (index + 1) : '#' + view;
    history.replaceState(null, '', hash);
  }
  function updateTransport() {
    if (!timeline || current === 2) return;
    if (!draggingSlider) $('#progress').value = Math.round(timeline.progress() * 1000);
    $('#progress-label').textContent = Math.round(timeline.progress() * 100) + '%';
    $('#play').textContent = timeline.isActive() ? 'Ⅱ 暂停' : '▶ 播放';
  }
  function select(index, autoPlay = true) {
    dispose();
    current = index;
    const demo = demos[index];
    $('#demo-count').textContent = (index + 1) + ' / ' + demos.length;
    $('#prev-demo').disabled = index === 0;
    $('#next-demo').disabled = index === demos.length - 1;
    $('#special-controls').innerHTML = '';
    $('#experiment-number').textContent = 'EXPERIMENT ' + String(index + 1).padStart(2, '0');
    $('#experiment-title').textContent = demo.name;
    $('#engine').textContent = demo.engine;
    $('#description').textContent = demo.description;
    $('#use-case').textContent = demo.use;
    $('#skill-note').textContent = demo.note;
    $('#hint').textContent = demo.hint + (reduced.matches ? ' 已遵循系统偏好，关闭自动播放。' : '');
    $('#code').textContent = demo.code;
    $('#skill-link').href = 'https://github.com/greensock/gsap-skills/blob/main/skills/' + demo.skill + '/SKILL.md';
    document.querySelectorAll('.experiment').forEach((button, i) => button.setAttribute('aria-current', i === index ? 'true' : 'false'));
    $('#progress').value = 0; $('#progress-label').textContent = '0%';
    context = gsap.context(() => { timeline = demo.build(); }, stage);
    history.replaceState(null, '', '#demo-' + (index + 1));
    $('.transport').hidden = !timeline || index === 2;
    $('.transport').style.display = !timeline || index === 2 ? 'none' : 'flex';
    $('#scrub-wrap').style.display = timeline ? 'flex' : 'none';
    if (timeline && index !== 2) {
      timeline.eventCallback('onUpdate', updateTransport);
      timeline.eventCallback('onComplete', updateTransport);
      timeline.eventCallback('onReverseComplete', updateTransport);
      timeline.timeScale(Number($('#speed').value));
      timeline.progress(1).pause();
      if (autoPlay && !reduced.matches) timeline.restart();
      updateTransport();
    }
    ScrollTrigger.refresh();
  }
  $('#experiment-list').innerHTML = window.labGroups.map(group => '<p class="rail-group">'+group.name+'</p>'+group.indices.map(i => `<button class="experiment" data-index="${i}" type="button" aria-current="${i === 0}"><span class="num">${String(i + 1).padStart(2,'0')}</span><span class="name">${demos[i].name}</span></button>`).join('')).join('');
  $('#experiment-list').addEventListener('click', event => { const button = event.target.closest('button'); if (button) select(Number(button.dataset.index)); });
  $('#show-overview').onclick = () => showView('overview');
  $('#show-lab').onclick = () => showView('lab');
  $('#show-guides').onclick = () => showView('guides');
  document.querySelector('main').addEventListener('click', event => {
    const target = event.target.closest('[data-open-demo]');
    if(target) {showView('lab',Number(target.dataset.openDemo));$('.view-nav').scrollIntoView({block:'start'});}
    if(event.target.closest('[data-open-guides]')) {showView('guides');$('.view-nav').scrollIntoView({block:'start'});}
  });
  $('#prev-demo').onclick=()=>select(Math.max(0,current-1));
  $('#next-demo').onclick=()=>select(Math.min(demos.length-1,current+1));
  $('#play').onclick = () => {
    if (!timeline || current === 2) return;
    if (timeline.isActive()) timeline.pause();
    else if (timeline.progress() >= .999) timeline.restart();
    else timeline.play();
    updateTransport();
  };
  $('#restart').onclick = () => { timeline?.restart(); updateTransport(); };
  $('#reverse').onclick = () => { if (timeline?.progress() === 0) timeline.progress(1); timeline?.reverse(); updateTransport(); };
  $('#speed').onchange = () => timeline?.timeScale(Number($('#speed').value));
  $('#progress').addEventListener('input', event => {
    const progress = Number(event.target.value) / 1000;
    if (current === 2) { const st = timeline.scrollTrigger; $('.scroll-viewport').scrollTop = st.start + progress * (st.end - st.start); ScrollTrigger.update(); }
    else { draggingSlider = true; timeline?.pause().progress(progress); draggingSlider = false; updateTransport(); }
  });
  let width = stage.clientWidth;
  const observer = new ResizeObserver(() => {
    if (stage.clientWidth === width) return;
    width = stage.clientWidth;
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { if(activeView === 'lab') select(current, false); }, 180);
  });
  observer.observe(stage);
  reduced.addEventListener('change', () => { if(activeView === 'lab') select(current, false); });
  window.addEventListener('pagehide', () => { clearTimeout(resizeTimer); observer.disconnect(); dispose(); });
  window.addEventListener('pageshow',event=>{if(event.persisted){observer.observe(stage);showView(activeView,current,false);}});
  function restoreLocation() {
    const initial=/^#demo-(\d+)$/.exec(location.hash);
    if(initial && Number(initial[1])>=1 && Number(initial[1])<=demos.length) showView('lab',Number(initial[1])-1);
    else showView(location.hash==='#guides'?'guides':'overview');
  }
  window.addEventListener('hashchange', restoreLocation);
  restoreLocation();
})();
