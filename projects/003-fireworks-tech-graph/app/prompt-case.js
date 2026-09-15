'use strict';
const byId=id=>document.getElementById(id);
const descriptions={
 overview:{label:'仓库事实',caption:'实际扫描固定提交的文件清单。箭头表示资料分类关系，不表示服务调用。',alt:'提示词仓库的资料分类与实际文件统计',explanation:'83 个 TXT 是提示词和规则等文本资料；17 个 JSON 后缀文件主要收录工具说明；两个 YAML 位于 Amp 目录，含模型名称和调试输入。另有 README、许可、图片和维护文件等 9 个文件。'},
 'agent-loop':{label:'依据文本归纳',caption:'依据 Manus Agent loop.txt 第 27–33 行整理；展示文中描述的循环，没有在本次运行该产品。',alt:'从分析事件到选择工具、执行、观察和交付的 Manus 文字流程',explanation:'提示词描述的是行为规则：读取事件、选择工具、等待实际执行结果，再决定继续还是交付。资料中的工具定义描述接口；真正执行动作，需要模型和外部运行环境。'},
 'your-workflow':{label:'建议使用流程',caption:'结合你的开源项目研究工作提出的方案。它是本次分析建议，不是目标仓库自带的自动化。',alt:'把参考资料经过筛选、改写、任务测试，沉淀为研究助手规则的流程',explanation:'例如，把 Cursor 的检索选择、Kiro 的需求设计任务拆分、Manus 的执行反馈循环，转化成你自己的研究助手规则。只写实际可用的工具，并以实际任务测试效果。'}
};
let revision=0;
async function selectDiagram(key){
 if(!descriptions[key])key='overview';const current=++revision;const d=descriptions[key];
 byId('case-image').src=`prompt-case/${key}.svg`;byId('case-image').alt=d.alt;
 byId('case-label').textContent=d.label;byId('case-caption').textContent=d.caption;byId('case-explanation').textContent=d.explanation;
 document.querySelectorAll('[data-diagram]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.diagram===key)));
 byId('case-downloads').replaceChildren(...[['html','打开原生交互图 ↗'],['png','下载 PNG'],['svg','下载 SVG'],['json','输入图纸 JSON'],['checks.json','检查记录']].map(([ext,label])=>{const a=document.createElement('a');a.href=`prompt-case/${key}.${ext}`;a.textContent=label;if(['png','svg'].includes(ext))a.download='';return a;}));
 history.replaceState(null,'',`#${key}`);
 try{const r=await fetch(`prompt-case/${key}.json`);if(!r.ok)throw new Error();const text=await r.text();if(current===revision)byId('raw-input').textContent=text;}catch{if(current===revision)byId('raw-input').textContent='无法载入，请通过输入图纸链接打开文件。';}
}
document.querySelectorAll('[data-diagram]').forEach(b=>b.addEventListener('click',()=>selectDiagram(b.dataset.diagram)));
selectDiagram(location.hash.slice(1));
fetch('prompt-case/research.json').then(r=>{if(!r.ok)throw new Error('来源记录未能载入');return r.json();}).then(data=>{
 for(const source of data.evidence){const a=document.createElement('a');a.href=source.url;a.textContent=`${source.file} · ${source.meaning} ↗`;byId('source-links').append(a);}
 for(const entry of data.jsonChecks.filter(x=>!x.parsed)){const li=document.createElement('li');li.textContent=`${entry.file}：第 ${entry.line} 行，${entry.reason}`;byId('json-errors').append(li);}
 for(const name of data.collectionDirectories){const li=document.createElement('li');li.textContent=name;byId('directory-list').append(li);}
}).catch(error=>byId('case-status').textContent=error.message);
