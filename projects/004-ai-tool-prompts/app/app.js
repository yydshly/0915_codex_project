'use strict';
const repoBase='https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/blob/1e4203a7d88873c1b37ab2d1c07074fea498c274/';
const original=(path,lines='')=>repoBase+path.split('/').map(encodeURIComponent).join('/')+lines;
const intents={
 flow:['优先看 x1xhlol 的产品流程案例','从 Manus 的执行循环、Kiro 的阶段产物和 Cursor 的工具选择入手；再用 asgeirtj 的同类材料补充。两个来源可以一起用。'],
 version:['优先看 asgeirtj 的版本与功能档案','对照同一产品不同模式、功能和历史版本的指令。版本标签是仓库标注，不能单凭标签判断真实性或完整性。'],
 build:['两个仓库都需要实际运行环境','资料可以提供规则和接口参考。要运行助手，还要准备模型、工具实现和连接它们的程序；不能把文件夹当成可直接使用的产品合集。']
};
const cases={
 manus:{task:'整理一个开源项目的能力，交付中文研究页',source:original('Manus Agent Tools & Prompt/Agent loop.txt','#L27-L33'),steps:[
 ['读取当前状态','根据用户任务和已有执行结果，确定还缺少什么信息。','任务：整理能力、原理和使用边界\n已有：仓库链接\n缺少：说明文档、目录、代表性样本','先弄清当前状态，避免一开始就凭印象写结论。'],
 ['选择一个工具','依据当前状态和任务计划选择下一次工具调用。','下一步：读取仓库说明与目录\n输入：仓库地址\n希望得到：能力描述与证据位置','工具选择服务于眼前的信息缺口。'],
 ['读取执行反馈','工具由运行环境执行，结果成为下一轮判断的依据。','示意反馈：一份 tools.json 解析失败\n已取得：文本内容\n尚未取得：可直接导入的工具结构','失败信息也属于有用结果，不能当作任务已经完成。'],
 ['调整后继续','根据新的观察继续选择行动，重复循环直到任务完成。','调整：按文本阅读，并标注格式问题\n保留：原始文件位置与版本\n结论：有接口说明，仍需整理后适配','具体失败情节是教学设定；它解释原文中的反馈与迭代。'],
 ['交付结果','完成任务后交付成果及相关文件，并等待后续任务。','中文研究页：能力、原理、案例、边界\n证据清单：固定版本与样本链接\n说明：未运行原产品，未验证效果提升','交付的是能查看的成果，以及清楚的验证范围。']
 ]},
 kiro:{task:'设计一个能收藏和筛选研究资料的小工具',source:original('Kiro/Spec_Prompt.txt','#L198-L210'),steps:[
 ['写清需求','先把想法转换为需求与验收标准，再与用户完善。','requirements.md（教学片段）\n用户可以保存资料标题、链接与标签。\n验收：选择一个标签，只显示匹配资料。','先明确“做出来以后怎样算满足需求”。'],
 ['形成设计','在需求基础上编写设计，说明结构、数据与处理方式。','design.md（教学片段）\n资料字段：标题、链接、标签列表\n页面区域：添加表单、标签选择、资料列表\n筛选方式：按标签匹配资料','设计解释怎样满足需求；它仍不是已经运行的程序。'],
 ['拆成任务','把已明确的需求与设计转成可执行的任务清单。','tasks.md（教学片段）\n□ 定义资料结构\n□ 实现添加资料\n□ 实现按标签筛选\n□ 检查空列表与多标签情况','给后续实现提供明确的工作单位与检查方向。'],
 ['按阶段推进','样本中的阶段确认用于让需求、设计和任务保持一致。','当前产物：需求 + 设计 + 任务\n下一步：确认后进入实现阶段\n没有发生：真实编码、存储或上线','文件名与阶段来自样本；这里的收藏工具内容由研究者编写。']
 ]},
 cursor:{task:'找到并理解项目中的登录逻辑',source:original('Cursor Prompts/Agent Prompt 2.0.txt','#L12-L27'),steps:[
 ['按含义找入口','在不熟悉代码库、寻找行为位置时，使用语义搜索。','问题：登录成功后，页面跳转在哪里处理？\n选择：按含义搜索代码\n目标：定位负责该行为的模块','不知道函数名时，先按问题含义寻找线索。'],
 ['按精确名称查找','已知符号或确切文本时，用精确搜索定位引用。','已知线索：handleLogin\n选择：精确搜索 handleLogin\n目标：找到定义和调用位置','已经知道名字，就不需要再次做宽泛的语义检索。'],
 ['读取已知文件','已知文件位置时，直接读取对应文件。','已知文件：src/auth/login.ts（虚构示例）\n选择：读取文件\n目标：核对参数、分支和跳转条件','工具不同，解决的问题不同；先建立事实再判断。'],
 ['形成可解释结论','把查到的位置与读到的逻辑整理成研究结果。','输出：登录流程说明 + 文件位置\n支持结论：来源是实际读取到的代码\n后续修改：仍需执行与验证','这一结论步骤是教学延伸；引用原文直接支持前三步的工具选择规则。']
 ]}
};
let selected='manus',step=0;
const byId=id=>document.getElementById(id);
function selectIntent(key){const [title,body]=intents[key];const box=byId('intent-result');box.replaceChildren();const h=document.createElement('strong');h.textContent=title;const p=document.createElement('p');p.textContent=body;box.append(h,p);document.querySelectorAll('[data-intent]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.intent===key)));}
function render(){const c=cases[selected],s=c.steps[step];byId('case-task').textContent=c.task;byId('case-source').href=c.source;byId('step-index').textContent=`步骤 ${step+1} / ${c.steps.length}`;byId('step-title').textContent=s[0];byId('step-rule').textContent=s[1];byId('step-output').textContent=s[2];byId('step-meaning').textContent=s[3];byId('progress-label').textContent=`${step+1} / ${c.steps.length}`;byId('prev').disabled=step===0;byId('next').disabled=step===c.steps.length-1;byId('next').textContent=step===c.steps.length-1?'已到最后一步':'下一步 →';byId('steps').replaceChildren();c.steps.forEach((s,i)=>{const li=document.createElement('li'),b=document.createElement('button'),n=document.createElement('span');b.type='button';n.textContent=String(i+1).padStart(2,'0');b.append(n,document.createTextNode(s[0]));b.setAttribute('aria-current',i===step?'step':'false');b.addEventListener('click',()=>{step=i;render();byId('steps').children[i].firstElementChild.focus({preventScroll:true});});li.append(b);byId('steps').append(li);});document.querySelectorAll('[data-case]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.case===selected)));}
document.querySelectorAll('[data-intent]').forEach(b=>b.addEventListener('click',()=>selectIntent(b.dataset.intent)));
document.querySelectorAll('[data-case]').forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.case;step=0;render();}));
byId('prev').addEventListener('click',()=>{step=Math.max(0,step-1);render();});byId('next').addEventListener('click',()=>{step=Math.min(cases[selected].steps.length-1,step+1);render();});byId('reset').addEventListener('click',()=>{step=0;render();});
const links=[['x1xhlol · 本次研究版本','https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/tree/1e4203a7d88873c1b37ab2d1c07074fea498c274','1e4203a7 · 111 个跟踪文件'],['asgeirtj · 对照版本','https://github.com/asgeirtj/system_prompts_leaks/tree/b55f7e37b71f076eb3228faa836954b6610046fe','b55f7e37 · 492 个跟踪文件'],['Manus · 执行循环',cases.manus.source,'循环原文 L27–33'],['Kiro · 需求、设计与任务',cases.kiro.source,'需求 L208 · 设计 L265 · 任务 L303'],['Cursor · 搜索与读取的选择',cases.cursor.source,'工具选择说明 L12–27']];
links.forEach(([title,url,detail])=>{const a=document.createElement('a'),small=document.createElement('small');a.href=url;a.target='_blank';a.rel='noopener';a.textContent=title+' ↗';small.textContent=detail;a.append(small);byId('sources').append(a);});selectIntent('flow');render();
