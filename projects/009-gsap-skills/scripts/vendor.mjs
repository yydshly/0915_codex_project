import { mkdir, copyFile } from 'node:fs/promises';
const root = new URL('../', import.meta.url);
await mkdir(new URL('app/vendor/', root), { recursive: true });
for (const file of ['gsap.min.js', 'ScrollTrigger.min.js', 'SplitText.min.js', 'MotionPathPlugin.min.js', 'DrawSVGPlugin.min.js', 'Flip.min.js', 'Draggable.min.js', 'InertiaPlugin.min.js', 'ScrollToPlugin.min.js', 'ScrollSmoother.min.js', 'ScrambleTextPlugin.min.js', 'MorphSVGPlugin.min.js', 'Observer.min.js', 'Physics2DPlugin.min.js', 'PhysicsPropsPlugin.min.js', 'CustomEase.min.js', 'CustomWiggle.min.js', 'CustomBounce.min.js', 'EasePack.min.js', 'TextPlugin.min.js']) {
  await copyFile(new URL('node_modules/gsap/dist/' + file, root), new URL('app/vendor/' + file, root));
}
await copyFile(new URL('node_modules/gsap/README.md', root), new URL('app/vendor/GSAP-README.md', root));
console.log('Vendored GSAP 3.15.0 and the capability gallery plugins.');
