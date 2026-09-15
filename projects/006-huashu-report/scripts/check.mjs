import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const html=fs.readFileSync(path.join(root,'app/index.html'),'utf8');
const nodes=new Map([...html.matchAll(/id="([^"]+)"/g)].map(m=>[m[1],{innerHTML:'',extra:'',insertAdjacentHTML(_,s){this.extra+=s;}}]));
const buttons=Array.from({length:6},(_,i)=>({dataset:{template:String(i)},attrs:{},events:{},setAttribute(k,v){this.attrs[k]=String(v)},addEventListener(k,fn){this.events[k]=fn}}));
const context=vm.createContext({document:{querySelector(selector){const node=nodes.get(selector.slice(1));assert.ok(node,`Missing container ${selector}`);return node;},querySelectorAll(selector){assert.equal(selector,'[data-template]');return buttons;}}});
vm.runInContext(fs.readFileSync(path.join(root,'app/app.js'),'utf8'),context);
assert.equal((nodes.get('template-grid').innerHTML.match(/class="template-card"/g)||[]).length,6);
assert.equal((nodes.get('visual-grid').innerHTML.match(/class="visual-card"/g)||[]).length,9);
assert.equal((nodes.get('chart-grid').innerHTML.match(/class="chart-card"/g)||[]).length,8);
for(let i=0;i<6;i++){
 buttons[i].events.click();
 assert.equal(buttons.filter(b=>b.attrs['aria-pressed']==='true').length,1);
 assert.equal(buttons[i].attrs['aria-pressed'],'true');
 const title=vm.runInContext(`templates[${i}].name`,context);
 assert.ok(nodes.get('template-detail').innerHTML.includes(`<h3>${title}</h3>`));
}
for(const id of ['evidence-metrics','rule-examples','visual-grid','chart-grid','detail-examples','detail-grid','pipeline-content','source-content'])assert.ok(nodes.get(id).innerHTML.length>100,`Empty ${id}`);
const fragments=[...nodes.values()].map(n=>n.innerHTML+n.extra).join('\n');
assert.ok(!/NaN|undefined/.test(fragments),'Invalid generated value');
assert.ok(!/(?:width|height)="-/.test(fragments),'Negative SVG dimension');
for(const m of fragments.matchAll(/href="([^"]+)"/g)){
 const url=new URL(m[1]);assert.equal(url.protocol,'https:');
 if(url.hostname==='github.com')assert.ok(url.pathname.includes('/bdc08bee5077462e1300431408c5237438a22d00/'));
}
console.log('PASS: 6 template selections, 9 directions, 8 chart diagrams, populated sections, pinned sources, finite SVG dimensions.');
