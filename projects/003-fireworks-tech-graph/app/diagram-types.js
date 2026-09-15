'use strict';
const get=id=>document.getElementById(id);let entries=[],chosen='sequence',requestId=0;
function anchor(url,label,download=false){const a=document.createElement('a');a.href=url;a.textContent=label;if(download)a.download='';return a;}
async function choose(key,scroll=false){
 const item=entries.find(x=>x.key===key);if(!item)return;chosen=key;const current=++requestId;
 get('type-title').textContent=item.title;get('type-question').textContent=item.question;get('type-badge').textContent=item.support;get('type-note').textContent=item.note;get('type-origin').textContent=item.origin;
 get('type-image').src=`types/${key}.svg`;get('type-image').alt=`${item.title}：${item.question}`;
 get('type-check').textContent=item.allChecksPassed?'上游五项通用 SVG 检查均通过；不等于完整图型语义认证。':'通用检查的结果或适配限制已保留在记录中，未将失败改写为通过。';
 get('type-downloads').replaceChildren(anchor(`types/${key}.html`,'原生交互查看器 ↗'),anchor(`types/${key}.png`,'下载 PNG',true),anchor(`types/${key}.svg`,'下载 SVG',true),anchor(`types/${key}.${item.input}`,item.input==='json'?'输入 JSON':'AI 编写的 SVG'),anchor(`types/${key}.checks.json`,'实际检查记录'));
 document.querySelectorAll('#type-list button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.key===key)));
 history.replaceState(null,'',`#${key}`);
 if(scroll)get('type-view').scrollIntoView({block:'start',behavior:'instant'});
 try{const r=await fetch(`types/${key}.${item.input}`);if(!r.ok)throw new Error();const data=await r.text();if(current===requestId)get('type-input').textContent=data;}catch{if(current===requestId)get('type-input').textContent='输入未能载入，请打开上方文件链接。';}
}
function filter(){
 const category=get('type-category').value,support=get('type-support').value;const visible=entries.filter(x=>(category==='all'||x.category===category)&&(support==='all'||x.support===support));
 get('type-count').textContent=`${visible.length} / ${entries.length} 个展示条目`;get('type-list').replaceChildren();
 for(const item of visible){const b=document.createElement('button');b.dataset.key=item.key;b.setAttribute('aria-pressed',String(item.key===chosen));const title=document.createElement('strong');title.textContent=item.title;const sub=document.createElement('small');sub.textContent=item.support+' · '+item.category;b.append(title,sub);b.addEventListener('click',()=>choose(item.key));get('type-list').append(b);}
 if(!visible.length){const p=document.createElement('p');p.textContent='这个组合没有条目，请调整类别或支持层级。';get('type-list').append(p);}else if(!visible.some(x=>x.key===chosen))choose(visible[0].key);
}
for(const id of ['type-category','type-support'])get(id).addEventListener('change',filter);
fetch('types/catalog.json').then(r=>{if(!r.ok)throw new Error('图型目录未能载入');return r.json();}).then(data=>{
 entries=data.items;const key=location.hash.slice(1);if(entries.some(x=>x.key===key))chosen=key;
 const order=['通用表达','系统与工程','数据与结构','UML 与行为','AI 与领域模式'];entries.sort((a,b)=>order.indexOf(a.category)-order.indexOf(b.category));
 for(const item of entries){const tr=document.createElement('tr');const td=document.createElement('td');const b=document.createElement('button');b.textContent=item.title;b.addEventListener('click',()=>{get('type-category').value='all';get('type-support').value='all';filter();choose(item.key,true);});const preview=document.createElement('img');preview.src=`types/${item.key}.svg`;preview.alt=`${item.title}预览，点击放大`;preview.loading='lazy';preview.style.cssText='display:block;width:220px;height:135px;object-fit:contain;margin-bottom:8px;border:1px solid #e0e7f1;background:white';b.prepend(preview);td.append(b);tr.append(td);for(const value of [item.question,item.support]){const cell=document.createElement('td');cell.textContent=value;tr.append(cell);}get('type-table').append(tr);}
 filter();choose(chosen);
}).catch(e=>get('type-status').textContent=e.message);
