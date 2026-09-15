(() => {
 'use strict';
 const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
 const systemMotion = matchMedia('(prefers-reduced-motion: reduce)');
 let motion = !systemMotion.matches, motionContext, media, intro, storyTimeline;
 let quiet = false, travel = false, lastBookTrigger;
 const dynamic = new Set(), magnetControllers = new Map();
 const originalWave = $('#sound-path').getAttribute('d');
 const calmWave = 'M0 95C30 95 30 78 60 78S90 112 120 112S150 78 180 78S210 112 240 112S270 78 300 78S330 112 360 112S390 78 420 78S450 112 480 112S510 78 540 78S570 95 600 95';
 const gsapReady = [window.gsap,window.ScrollTrigger,window.SplitText,window.Flip,window.ScrollToPlugin,window.MorphSVGPlugin].every(Boolean);
 if(gsapReady) gsap.registerPlugin(ScrollTrigger,SplitText,Flip,ScrollToPlugin,MorphSVGPlugin); else motion = false;
 const d = seconds => motion ? seconds : 0;
 function track(tween) {
   dynamic.add(tween);
   const complete=tween.eventCallback('onComplete');
   tween.eventCallback('onComplete',()=>{dynamic.delete(tween);complete?.();});
   if(tween.progress()===1) dynamic.delete(tween);
   return tween;
 }
 function animate(target, vars) {
   if(!gsapReady) return null;
   return track(gsap.to(target,{overwrite:'auto',...vars,duration:d(vars.duration??.5)}));
 }
 function popIn(target) {
   if(motion) track(gsap.fromTo(target,{opacity:0,y:20},{opacity:1,y:0,duration:.4,ease:'power3.out',clearProps:'opacity,transform'}));
 }
 function updateMotionButton() {
   $('#motion-toggle').textContent = '动效：'+(motion?'开启':'关闭');
   $('#motion-toggle').setAttribute('aria-pressed',String(motion));
 }
 function setupMotion(entrance = false) {
   media?.revert(); media = null;
   motionContext?.revert(); motionContext = null;
   magnetControllers.forEach(({x,y})=>{x.tween.kill();y.tween.kill();});
   magnetControllers.clear();
   $$('.magnetic').forEach(el=>{el.style.transform='';});
   document.body.classList.toggle('has-motion',motion);
   document.body.classList.toggle('static-reading',!motion);
   updateMotionButton();
   if(!gsapReady || !motion) return;
   motionContext = gsap.context(()=>{
     const split=SplitText.create('#hero-title',{type:'chars,words',aria:'auto'});
     intro=gsap.timeline({defaults:{ease:'power3.out'}})
       .from('.hero .kicker',{opacity:0,y:10,duration:.6},0)
       .from(split.chars,{autoAlpha:0,y:35,rotation:3,stagger:.025,duration:.85},.15)
       .from('#hero-product',{autoAlpha:0,y:80,rotation:-13,scale:.88,duration:1.5},.3)
       .from('.hero-description, .hero .round-link, .hero-bottom',{autoAlpha:0,y:18,duration:.75,stagger:.1},.85);
     if(!entrance) intro.progress(1);
     gsap.fromTo('.hero-visual .model-type',{y:0},{y:65,ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:true}});
     $$('.reveal').forEach(el=>gsap.from(el,{y:38,autoAlpha:0,duration:.9,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 92%',once:true}}));
     gsap.from('.detail-choice',{x:24,opacity:0,duration:.7,stagger:.15,scrollTrigger:{trigger:'.detail-choices',start:'top 90%',once:true}});
   },document.querySelector('main'));
   media=gsap.matchMedia();
   media.add({desktop:'(min-width:701px)',mobile:'(max-width:700px)'},ctx=>{
     const mobile=ctx.conditions.mobile,steps=$$('.story-step'),product=$('.story-product img');
     gsap.set(steps,{autoAlpha:0,y:25});gsap.set(steps[0],{autoAlpha:1,y:0});
     storyTimeline=gsap.timeline({scrollTrigger:{id:'product-story',trigger:'.story-frame',start:()=>`top ${$('.demo-bar').offsetHeight}px`,end:()=>'+='+Math.round(innerHeight*(mobile?2:2.7)),pin:true,scrub:.6,invalidateOnRefresh:true},onUpdate(){
       const time=this.time(),chapter=time>=2.35?2:time>=1.05?1:0;
       $('#chapter-count').textContent='0'+(chapter+1)+' / 03';
       $('#part-label').textContent=['柔软耳罩','贴合质感','金属连接'][chapter];
     }});
     storyTimeline.to(product,{scale:1.02,rotation:0,duration:.65,ease:'none'},0)
       .to(steps[0],{autoAlpha:0,y:-22,duration:.28},.8)
       .fromTo(steps[1],{autoAlpha:0,y:25},{autoAlpha:1,y:0,duration:.42},1.02)
       .to(product,{scale:mobile?1.26:1.32,xPercent:-8,yPercent:-10,rotation:-6,duration:1,ease:'power2.inOut'},.85)
       .to(steps[1],{autoAlpha:0,y:-22,duration:.28},2.08)
       .fromTo(steps[2],{autoAlpha:0,y:25},{autoAlpha:1,y:0,duration:.42},2.33)
       .to(product,{scale:1.08,xPercent:4,yPercent:6,rotation:8,duration:1,ease:'power2.inOut'},2.15)
       .to('.chapter-track>i',{scaleX:3,duration:3.6,ease:'none'},0)
       .to({}, {duration:.25},3.35);
   });
   $$('.magnetic').forEach(el=>magnetControllers.set(el,{x:gsap.quickTo(el,'x',{duration:.3,ease:'power3.out'}),y:gsap.quickTo(el,'y',{duration:.3,ease:'power3.out'})}));
   ScrollTrigger.refresh();
 }
 $$('.magnetic').forEach(el=>{
   el.addEventListener('pointermove',event=>{
     if(!motion||event.pointerType==='touch')return;
     const r=el.getBoundingClientRect(),control=magnetControllers.get(el);
     control?.x((event.clientX-r.left-r.width/2)*.06);control?.y((event.clientY-r.top-r.height/2)*.09);
   });
   el.addEventListener('pointerleave',()=>{const control=magnetControllers.get(el);control?.x(0);control?.y(0);});
 });
 function toggleMotion(enabled) {
   const anchor=$$('main>section').find(el=>{const r=el.getBoundingClientRect();return r.top<=innerHeight/2&&r.bottom>=innerHeight/2;});
   const position=anchor?.getBoundingClientRect().top;
   dynamic.forEach(tween=>{tween.progress(1);tween.kill();});dynamic.clear();
   motion=enabled&&gsapReady;setupMotion(false);
   if(anchor) window.scrollBy(0,anchor.getBoundingClientRect().top-position);
 }
 $('#motion-toggle').onclick=()=>toggleMotion(!motion);
 systemMotion.addEventListener('change',()=>toggleMotion(!systemMotion.matches));
 function goTo(id) {
   const target=document.getElementById(id);if(!target)return;
   const top=$('.demo-bar').offsetHeight+12;
   if(gsapReady)animate(window,{scrollTo:{y:target,offsetY:top,autoKill:true},duration:.9,ease:'power2.inOut'});
   else window.scrollTo(0,target.getBoundingClientRect().top+scrollY-top);
   history.replaceState(null,'','#'+id);
 }
 $$('a[href^="#"]').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();closeAllDialogs();goTo(link.getAttribute('href').slice(1));}));
 $('.noise-bars').innerHTML=Array.from({length:48},(_,i)=>`<i style="height:${24+(Math.sin(i*2.3)+1)*35}%"></i>`).join('');
 $('#quiet-toggle').onclick=()=>{
   quiet=!quiet;$('#quiet-toggle').setAttribute('aria-pressed',String(quiet));
   $('#quiet-toggle').innerHTML=(quiet?'回到环境模式':'体验安静模式')+' <span>↗</span>';
   $('#sound-state').textContent=quiet?'FOCUS / 留给自己的声音':'AMBIENT / 外界的声音';
   $('#sound-indicator').textContent=quiet?'安静模式':'环境模式';
   $('#sound-caption').textContent=quiet?'把这一刻，还给自己。':'让外界的声音，慢慢退到身后。';
   if(gsapReady){animate('#sound-path',{morphSVG:quiet?calmWave:originalWave,duration:1.1,ease:'power2.inOut'});animate('.noise-bars i',{scaleY:quiet?.09:1,opacity:quiet?.3:1,duration:.8,stagger:motion?.008:0,ease:'power2.inOut'});}
   else $('#sound-path').setAttribute('d',quiet?calmWave:originalWave);
 };
 const views={whole:{scale:1,xPercent:0,yPercent:0,caption:'01 / 整体轮廓'},ear:{scale:1.9,xPercent:-20,yPercent:-27,caption:'02 / 耳罩与包覆质感'},band:{scale:1.85,xPercent:10,yPercent:40,caption:'03 / 头梁与金属连接'}};
 $$('.detail-choice').forEach(button=>button.onclick=()=>{
   const view=views[button.dataset.view];
   $$('.detail-choice').forEach(el=>{el.classList.toggle('active',el===button);el.setAttribute('aria-pressed',String(el===button));});
   $('#zoom-caption').textContent=view.caption;
   if(gsapReady)animate('#zoom-product',{scale:view.scale,xPercent:view.xPercent,yPercent:view.yPercent,duration:.9,ease:'power3.inOut'});
   else $('#zoom-product').style.transform=`translate(${view.xPercent}%,${view.yPercent}%) scale(${view.scale})`;
 });
 let flipTween,countTween;const count={value:1};
 function chooseBundle(value){
   if(travel===value)return;
   flipTween?.progress(1).kill();countTween?.progress(1).kill();
   const state=gsapReady?Flip.getState('#case-card, .headphone-card'):null;
   travel=value;(travel?$('#chosen-items'):$('#available-items')).append($('#case-card'));
   $('#case-status').textContent=travel?'已选':'可加入';
   $('#solo').classList.toggle('selected',!travel);$('#solo').setAttribute('aria-pressed',String(!travel));
   $('#travel').classList.toggle('selected',travel);$('#travel').setAttribute('aria-pressed',String(travel));
   $('#bundle-description').textContent=travel?'耳机与收纳包一起，陪你去更远的地方。':'一副耳机，留给自己的轻装时刻。';
   if(gsapReady){flipTween=track(Flip.from(state,{duration:d(.75),absolute:true,ease:'power3.inOut',onComplete:()=>ScrollTrigger.refresh()}));countTween=animate(count,{value:travel?2:1,duration:.45,ease:'power2.out',onUpdate:()=>$('#item-count').textContent=Math.round(count.value)});}
   else $('#item-count').textContent=travel?'2':'1';
 }
 $('#solo').onclick=()=>chooseBundle(false);$('#travel').onclick=()=>chooseBundle(true);
 const dialogs=$$('dialog');
 function lockPage(){document.documentElement.style.overflow=dialogs.some(el=>el.open)?'hidden':'';}
 function closeAllDialogs(){dialogs.forEach(el=>{if(el.open)el.close();});lockPage();}
 dialogs.forEach(dialog=>{
   dialog.addEventListener('close',lockPage);
   dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();});
   dialog.querySelectorAll('[data-close]').forEach(button=>button.onclick=()=>dialog.close());
 });
 function openBook(trigger){
   closeAllDialogs();lastBookTrigger=trigger;$('#booking-form').hidden=false;$('#booking-success').hidden=true;
   $('#plan-bundle').textContent=travel?'ONE + 收纳包 · 随行组合':'ONE · 轻装出发';
   $('#booking-dialog').showModal();lockPage();popIn($('#booking-dialog'));
 }
 $$('[data-book]').forEach(button=>button.onclick=()=>openBook(button));
 $('#booking-dialog').addEventListener('close',()=>{if(lastBookTrigger&&!lastBookTrigger.closest('dialog'))lastBookTrigger.focus({preventScroll:true});});
 $('#booking-form').addEventListener('submit',event=>{
   event.preventDefault();$('#plan-summary').textContent=`${$('#listening-time').value}，${$('#listening-style').value}。你的搭配：${travel?'ONE 耳机与随行收纳包':'ONE 耳机'}。`;
   $('#booking-form').hidden=true;$('#booking-success').hidden=false;$('#booking-success').focus({preventScroll:true});popIn($('#booking-success'));
 });
 $('#explain-open').onclick=()=>{closeAllDialogs();$('#explain-dialog').showModal();lockPage();popIn($('#explain-dialog'));};
 setupMotion(true);
 document.fonts.ready.then(()=>{if(gsapReady)ScrollTrigger.refresh();});
 window.addEventListener('load',()=>{if(gsapReady)ScrollTrigger.refresh();});
 window.addEventListener('pagehide',()=>{media?.revert();motionContext?.revert();dynamic.forEach(tween=>tween.kill());magnetControllers.forEach(({x,y})=>{x.tween.kill();y.tween.kill();});});
 window.addEventListener('pageshow',event=>{if(event.persisted)setupMotion(false);});
})();
