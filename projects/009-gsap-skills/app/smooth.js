(() => {
 if(!window.gsap||!window.ScrollTrigger||!window.ScrollSmoother){document.querySelector('#smooth-error').hidden=false;return;}
 gsap.registerPlugin(ScrollTrigger,ScrollSmoother);
 const reduced=matchMedia('(prefers-reduced-motion:reduce)').matches;
 const smoother=ScrollSmoother.create({wrapper:'#smooth-wrapper',content:'#smooth-content',smooth:reduced?0:1,effects:!reduced,smoothTouch:0});
 document.querySelector('#smooth-down').onclick=()=>smoother.scrollTo(Math.min(document.documentElement.scrollHeight-innerHeight,scrollY+260),!reduced);
 document.querySelector('#smooth-up').onclick=()=>smoother.scrollTo(0,!reduced);
 window.addEventListener('pagehide',()=>smoother.kill());
})();
