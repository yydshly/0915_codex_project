'use strict';
const $=id=>document.getElementById(id);
let manifest, selected=1, format='svg';
const artifact=(key,ext)=>`artifacts/${key}.${ext}`;
function link(href,label,download=false){const a=document.createElement('a');a.href=href;a.textContent=label;if(download)a.download='';return a;}
function setScene(id){
 if(!manifest)return;
 selected=id;const s=manifest.gallery.find(x=>x.id===id);
 document.querySelectorAll('.scene').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.id===id)));
 $('scene-number').textContent=`STYLE ${String(id).padStart(2,'0')} / ${s.theme}`;$('scene-title').textContent=s.title;
 $('scene-image').src=artifact(s.key,format==='gif'?'reference.gif':'svg');$('scene-image').alt=`${s.theme} 风格的${s.title}${format==='gif'?'动画':''}`;
 $('scene-caption').textContent=format==='gif'?'上游 1.2.0 发布样片 · 非本次编码 · 点击「本次 SVG」停止播放':s.generated?'本次使用原库 JSON 样例重新生成 · 5 项程序检查通过':'上游 AI 编写 SVG 原样保留 · 本次 5 项程序检查通过';
 $('scene-summary').textContent=s.summary;
 $('show-svg').textContent=s.generated?'本次 SVG':'上游 SVG';
 $('show-svg').setAttribute('aria-pressed',String(format==='svg'));$('show-gif').setAttribute('aria-pressed',String(format==='gif'));
 $('scene-links').replaceChildren(link(artifact(s.key,'html'),'打开原生交互图 ↗'),link(artifact(s.key,'svg'),'下载 SVG',true),link(artifact(s.key,'png'),'下载本次 PNG',true),link(artifact(s.key,'checks.json'),'校验记录'));
 if(s.generated)$('scene-links').append(link(artifact(s.key,'json'),'输入 JSON'));
 history.replaceState(null,'',`#gallery-${id}`);
}
function activate(panel){
 if(!manifest)return;
 document.querySelectorAll('.panel').forEach(p=>p.hidden=p.id!==panel);
 document.querySelectorAll('[data-panel]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.panel===panel)));
 if(panel!=='gallery'){format='svg';$('scene-image').src=artifact(manifest.gallery.find(x=>x.id===selected).key,'svg');history.replaceState(null,'',`#${panel}`);}
 else setScene(selected);
}
document.querySelectorAll('[data-panel]').forEach(b=>b.addEventListener('click',()=>activate(b.dataset.panel)));
$('show-svg').addEventListener('click',()=>{format='svg';setScene(selected)});
$('show-gif').addEventListener('click',()=>{format='gif';setScene(selected)});
async function init(){
 try{
  const response=await fetch('data.json');if(!response.ok)throw new Error('资料暂时无法载入');manifest=await response.json();
  for(const s of manifest.gallery){const b=document.createElement('button');b.className='scene';b.dataset.id=s.id;b.innerHTML=`<span class="num">${String(s.id).padStart(2,'0')}</span><span><b>${s.title}</b><small>${s.theme}</small></span>`;b.addEventListener('click',()=>setScene(s.id));$('scene-list').append(b);}
  renderChinese();renderMechanism();renderComparison();
  const hash=location.hash.slice(1);if(/^gallery-\d+$/.test(hash)){selected=+hash.split('-')[1];if(!manifest.gallery.some(s=>s.id===selected))selected=1;}
  setScene(selected);if(['chinese','mechanism','compare'].includes(hash))activate(hash);
 }catch(e){$('load-status').textContent=`${e.message}。请使用本地网页服务打开本页。`;}
}
function renderChinese(){
 $('chinese').innerHTML=`<div class="section-intro"><h2>一张中文架构，七种表达。</h2><p>用一个研究助手演示请求、规划、记忆、工具与评估。七张图保持 6 个节点、7 条关系及坐标一致，观察风格如何影响阅读。</p></div><div class="paper"><span class="pill">本次真实生成 · 中文严格文字模式</span><div id="theme-picker" class="theme-picker" aria-label="中文图风格"></div><img id="custom-image" class="custom-image" src="artifacts/chinese-style1.svg" alt="研究助手中文架构图"><p class="notice">这是用于解释分工的教学架构，由本次研究编写规格；不表示已部署或已测量的真实系统。</p><div id="custom-links" class="links"></div><details><summary>查看这张图的结构化输入</summary><pre id="custom-json" class="result"></pre></details></div><div class="two-col"><article class="paper"><h3>这次实际验证了什么？</h3><p>中文节点与连线标签、相同结构下的七种风格、严格文字完整性，以及 XML、箭头引用、碰撞、几何和构图五类检查。</p></article><article class="paper"><h3>从描述到图，还需要谁？</h3><p>宿主 AI 负责理解需求、整理事实与位置；本库接收 JSON 并绘制。本页切换已生成结果，不会在浏览器里调用大模型。</p></article></div>`;
 let version=0;
 async function choose(id){const request=++version;const s=manifest.custom.find(x=>x.id===id);$('custom-image').src=artifact(s.key,'svg');document.querySelectorAll('#theme-picker button').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.id===id)));$('custom-links').replaceChildren(link(artifact(s.key,'html'),'打开原生交互图 ↗'),link(artifact(s.key,'svg'),'下载 SVG',true),link(artifact(s.key,'png'),'下载 PNG',true),link(artifact(s.key,'checks.json'),'检查记录'));try{const r=await fetch(artifact(s.key,'json'));if(!r.ok)throw new Error();const text=await r.text();if(request===version)$('custom-json').textContent=text;}catch{if(request===version)$('custom-json').textContent='输入文件未能载入，请通过原始文件查看。';}}
 for(const s of manifest.custom){const b=document.createElement('button');b.dataset.id=s.id;b.textContent=s.theme;b.addEventListener('click',()=>choose(s.id));$('theme-picker').append(b);}choose(1);
}
function renderMechanism(){
 $('mechanism').innerHTML=`<div class="section-intro"><h2>AI 组织内容，程序约束结果。</h2><p>生成一张图只是开始。核心价值来自图数据、路由、结构检查和实际图像检查之间的协作。</p></div><div class="pipeline"><div><span>01 / 理解</span><h3>系统描述</h3><p>AI 读取需求与资料，选择节点、关系、分组和风格。事实需要来源。</p></div><div><span>02 / 规范</span><h3>图数据</h3><p>JSON 规范化为版本化内部结构，检查 ID、引用、坐标与工程规则。</p></div><div><span>03 / 布局</span><h3>连线路由</h3><p>在给定位置间选择正交路线，按距离、转弯、交叉、重叠计算代价。</p></div><div><span>04 / 验证</span><h3>SVG 与检查</h3><p>生成语义 SVG，检查越界、碰撞、标签和构图。失败后定点修复。</p></div><div><span>05 / 交付</span><h3>图像与查看器</h3><p>导出 PNG、离线 HTML；受支持语义场景可进一步生成 GIF。</p></div></div><div class="two-col"><article class="paper"><h3>真正的自动化在哪里？</h3><p>确定性连线路由使用障碍物可见性网格与最短路径搜索。节点位置通常由输入或 AI 给出，不能推导为任意大图都有自动最优布局。</p><p>Style 9–12 检查 C4 层级、云归属、事件拓扑、观测指标等领域规则；规则一致不等于现实事实正确。</p></article><article class="paper"><h3>本次验证范围</h3><p><b>18 张重新生成 SVG + 1 张上游手绘 SVG</b>，共 19 张图通过五项程序检查，并导出原生离线 HTML 和 PNG。</p><p>GIF 展示使用上游发布文件。本次没有重新编码 GIF；也没有宣称所有图型或任意拓扑均已验证。</p><a href="artifacts/provenance.json">查看完整生成凭证 ↗</a></article></div><article class="paper"><h3>故意输入错误，原库会怎样？</h3><p>以下为实际执行原库得到的拒绝记录。切换查看失败原因与原始输入。</p><div class="experiment-buttons" id="negative-picker"></div><pre id="negative-result" class="result"></pre><div id="negative-links" class="links"></div></article><article class="paper"><h3>可交付，也可复查</h3><p>SVG 保留可编辑矢量；PNG 适合文档；单文件 HTML 支持平移、缩放、主题和下载。程序检查无法完全替代视觉判断：中文字体替换、实际可读性和复杂图仍需看渲染结果。</p><p>生成核心：<a href="https://github.com/yizhiyanhua-ai/fireworks-tech-graph/blob/${manifest.commit}/scripts/generate-from-template.py">生成器与路由</a> · <a href="https://github.com/yizhiyanhua-ai/fireworks-tech-graph/blob/${manifest.commit}/scripts/semantic_contracts.py">工程语义检查</a> · <a href="https://github.com/yizhiyanhua-ai/fireworks-tech-graph/blob/${manifest.commit}/scripts/validate_svg.py">SVG 校验</a></p></article>`;
 function select(index){const c=manifest.negativeCases[index];$('negative-result').textContent=JSON.stringify(c.result,null,2);document.querySelectorAll('#negative-picker button').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));$('negative-links').replaceChildren(link(artifact('invalid-'+c.key,'json'),'错误输入'),link(artifact('invalid-'+c.key,'result.json'),'原始拒绝记录'));}
 manifest.negativeCases.forEach((c,i)=>{const b=document.createElement('button');b.textContent=c.label;b.addEventListener('click',()=>select(i));$('negative-picker').append(b)});select(0);
}
function renderComparison(){
 $('compare').innerHTML=`<div class="section-intro"><h2>最相近的是 Archify。Graphify 位于上游。</h2><p>已经核对 9 月 9 日的 Archify 实战与 9 月 11 日研究库的 Graphify 记录。以下按当时固定研究版本比较，不把历史结果写成各项目的最新状态。</p></div><div class="table-wrap" tabindex="0" role="region" aria-label="三个项目的能力对比"><table><thead><tr><th>比较维度</th><th>Fireworks</th><th>Archify · 以前研究过</th><th>Graphify · 以前研究过</th></tr></thead><tbody><tr><td>主要问题</td><td>怎样把技术关系画得清晰、风格统一？</td><td>怎样交互阅读系统，并讲解或比较设计？</td><td>代码和资料里有哪些实体与关系？</td></tr><tr><td>主要输入</td><td>AI / 作者整理的 JSON 或 SVG</td><td>作者 / Agent 编写的类型化 JSON 设计规格</td><td>源码、文档及其他受支持资料</td></tr><tr><td>核心机制</td><td>风格规则、正交路由、语义与几何校验</td><td>专用布局与渲染、产物检查、HTML 查看器</td><td>AST / 语义提取、建图、图分析与查询</td></tr><tr><td>视觉与交付</td><td>12 种风格；SVG、PNG、离线 HTML、受约束 GIF</td><td>五类技术图与架构差异；交互 HTML、多格式导出</td><td>网络、树、调用流程、报告、Wiki 与图数据</td></tr><tr><td>交互重点</td><td>离线查看器的平移、缩放、主题与下载</td><td>搜索、上下游追踪、有向路径、章节讲解</td><td>Query / Explain / Path / Affected、CLI 与 MCP</td></tr><tr><td>源码与变更</td><td>本次未见内置源码提取或架构模型差异功能</td><td>可关联固定提交源码；比较两个已编写的模型</td><td>从代码提取关系，支持增量更新；静态图并非运行轨迹</td></tr><tr><td>已有证据</td><td>19 张 SVG 程序检查、中文换肤、3 种错误拒绝</td><td>自身五类中文图、源码引用、真实模型差异与导出</td><td>FastAPI 48 文件 → 747 节点 / 1,971 关系</td></tr><tr><td>研究版本</td><td>1.2.0 + 未发布升级<br><code>31fea36</code></td><td>2.17.0-dev.1<br><code>1072200</code></td><td>0.9.57<br><code>3f82bf7</code></td></tr></tbody></table></div><div class="comparison-cards"><article class="paper"><h3>Archify：我们已经做过的中文实战</h3><figure><img loading="lazy" src="comparison/archify.png" alt="以前由 Archify 原生生成的自身中文架构图"><figcaption>复用 0909 研究项目的实际预览。源码事实由 Agent 阅读整理，Archify 负责渲染与交互。</figcaption></figure><p><a href="https://yydshly.github.io/0909_codex_project/projects/003-archify/">打开以前的完整展厅 ↗</a></p></article><article class="paper"><h3>Graphify：从资料中提取关系</h3><figure><img loading="lazy" src="comparison/graphify.svg" alt="以前 Graphify 根据 FastAPI 核心包生成的完整关系网络"><figcaption>复用已有全量图谱。747 节点、1,971 关系是特定 48 文件范围的结果，并非整个 FastAPI。</figcaption></figure><p><a href="https://yydshly.github.io/0911_codex_project/009-graphify/">打开以前的原生演示 ↗</a></p></article></div><div class="two-col"><article class="paper"><h3>Fireworks 的新增价值</h3><ol class="value-list"><li><b>统一研究配图。</b>为 README、技术说明和演示稿建立视觉一致的架构与流程图。</li><li><b>减少重复排版。</b>复用风格、形状与连线约定，并用机器检查筛出常见错误。</li><li><b>增强工程表达。</b>C4、云、事件和观测视图的规则帮助发现缺失字段与关系。</li><li><b>保留可复现交付。</b>让输入、SVG、图片与检查记录一起留在研究项目中。</li></ol></article><article class="paper"><h3>按问题选择工具</h3><ul class="value-list"><li><b>陌生项目，先找关系：</b>Graphify。</li><li><b>评审设计，追踪路径与看改造：</b>Archify。</li><li><b>文章、README 与演示图：</b>Fireworks。</li><li><b>组合方向：</b>Graphify 提取证据 → Agent 筛选和核实 → Fireworks 出图或 Archify 交互讲解。</li></ul><p class="notice">组合链路是建议，尚未接通。效率提升、成本节省与付费价值需要同题对照实验，当前没有量化结论。</p></article></div><article class="paper"><h3>需要避免的重复建设</h3><p>Archify 已经提供可复现绘图与交付，Fireworks 的新增价值主要在风格体系和工程图表达。若只需要交互追踪和架构差异，继续使用已有 Archify 更直接；若研究重点是数据趋势与统计报告，可沿用此前的 Lieflat Charts 路线。不同任务不必统一成一个工具。</p><div class="links"><a href="https://github.com/tt-a1i/archify/tree/10722002bb8777ecb639d93c49586fae4adf3ae4">Archify 固定源码</a><a href="https://github.com/Graphify-Labs/graphify/tree/3f82bf7f837a07fb0f7668fbdbd5662801906942">Graphify 固定源码</a><a href="comparison/history.json">历史研究来源</a></div></article>`;
}
init();
