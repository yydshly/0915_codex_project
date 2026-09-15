const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1080}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('console',m=>{if(['error','warning'].includes(m.type()))errors.push(m.text());});
 page.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url());});
 await page.goto('http://127.0.0.1:8099/');
 await page.waitForSelector('.capability-card');
 assert.equal(await page.locator('.capability-card').count(),27);
 assert.equal(await page.locator('.skill-card').count(),8);
 await page.locator('#show-guides').click();
 assert.equal(await page.locator('#guides').isVisible(),true);
 assert.equal(await page.locator('.external-grid article').count(),6);
 await page.locator('#show-overview').click();
 await page.screenshot({path:path.join(__dirname,'../assets/catalog.png'),fullPage:true});
 for(let i=0;i<27;i++){
  await page.goto('http://127.0.0.1:8099/#demo-'+(i+1));
  // Hash-only navigation does not reload: explicitly load the selected experiment.
  await page.reload();
  await page.waitForSelector('#stage > *');
  assert.ok(await page.locator('#experiment-title').textContent());
  if(await page.locator('#scrub-wrap').isVisible()){
   await page.locator('#progress').fill('500');
   await page.waitForTimeout(40);
  }
  console.log('Rendered '+(i+1)+' '+await page.locator('#experiment-title').textContent());
 }
 async function demo(index){await page.locator(`[data-index="${index}"]`).click();}
 await demo(10);await page.locator('#progress').fill('1000');assert.equal(await page.locator('#scramble').textContent(),'MAKE IT MOVE');
 await demo(11);const start=await page.locator('#morph-shape').getAttribute('d');await page.locator('#progress').fill('200');assert.notEqual(await page.locator('#morph-shape').getAttribute('d'),start);
 await demo(12);await page.locator('#go-C').click();await page.waitForTimeout(1200);assert.ok(await page.locator('#jump-viewport').evaluate(el=>el.scrollTop)>500);
 await demo(13);const frame=page.frameLocator('.smooth-frame');await frame.locator('#smooth-down').click();await page.waitForTimeout(1400);
 assert.ok(await frame.locator('body').evaluate(()=>scrollY)>100);
 assert.ok(await frame.locator('#smooth-content').evaluate(el=>el.style.transform.length)>0);
 await demo(14);await page.locator('#gesture-next').click();assert.equal(await page.locator('.gesture-card').textContent(),'感知');
 await page.locator('.gesture-area').focus();await page.keyboard.press('ArrowLeft');assert.equal(await page.locator('.gesture-card').textContent(),'移动');
 await demo(21);await page.locator('#utils-input').fill('83');assert.equal(await page.locator('#value-snap').textContent(),'吸附 80');assert.equal(await page.locator('#value-angle').textContent(),'角度 299°');
 await demo(22);await page.locator('#follow-move').click();await page.waitForTimeout(550);const follow=await page.locator('.follow-dot').evaluate(el=>Number(gsap.getProperty(el,'x')));assert.ok(follow>20);
 await demo(24);await page.locator('#mount').click();assert.equal(await page.locator('#live-count').textContent(),'组件动画数：1');await page.locator('#unmount').click();assert.equal(await page.locator('#live-count').textContent(),'组件动画数：0');
 assert.equal(await page.locator('.local-box').evaluate(el=>Number(gsap.getProperty(el,'x'))),0);
 await demo(25);await page.locator('#progress').fill('500');assert.equal(await page.locator('#lab-canvas').getAttribute('aria-label'),'圆环进度 50%');
 await demo(26);await page.locator('#progress').fill('1000');assert.equal(await page.locator('#typed-text').textContent(),'Make it yours.');
 for(let i=0;i<27;i++)await demo(i);
 await page.locator('#show-overview').click();
 assert.equal(await page.evaluate(()=>ScrollTrigger.getAll().length),0);
 assert.equal(await page.evaluate(()=>Observer.getAll().length),0);
 await page.setViewportSize({width:390,height:844});
 for(let i=0;i<27;i++){
  await page.locator('#show-lab').click();await demo(i);await page.waitForTimeout(30);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'mobile overflow '+i);
 }
 await demo(11);await page.locator('#progress').fill('350');await page.screenshot({path:path.join(__dirname,'../assets/mobile-expanded.png'),fullPage:true});
 await page.locator('#show-overview').click();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.locator('#show-guides').click();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.emulateMedia({reducedMotion:'reduce'});await page.locator('#show-lab').click();await demo(23);assert.ok((await page.locator('#media-status').textContent()).includes('减少动态效果'));
 assert.deepEqual(errors,[]);
 console.log('PASS: 27 demos, 8 skills, 6 reference entries, plugin behaviors, scoped cleanup, 390px layout, reduced-motion adaptation.');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
