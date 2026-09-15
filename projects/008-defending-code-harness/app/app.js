"use strict";

const commit = "d3bea6b5793b5f3d59a75ebe69a58efa88383145";
const upstream = `https://github.com/anthropics/defending-code-reference-harness/blob/${commit}/`;
const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[char]);
const steps = [
  {label:"THREAT MODEL / 明确范围", title:"先问：谁能把什么数据送进来？", text:"模型结合源码、文档和使用者提供的部署信息，识别外部输入、受保护资源和权限边界。这决定哪些路径值得检查，也帮助排除只在测试工具里成立的问题。", input:"源码、部署方式、接口权限、已有安全约束。", action:"列出可控制字段，追踪它们能调用哪些生产入口。", output:"威胁模型：资产、入口、信任边界与优先威胁。", example:"例如：未登录用户能上传音频，服务会把文件交给某个解码器。攻击者控制的是文件字节，不是服务器启动参数。", source:"docs/threat-model.md"},
  {label:"RECON / 搜索分区", title:"把大仓库拆成可探索的输入路径。", text:"Recon 读取源码结构，提出多个搜索区域，交给不同 Find 任务。区域通常是一个解析器、入口函数或状态处理子系统，减少所有智能体反复找到同一个问题。", input:"源码目录、目标信息；已有 focus_areas 或可供参考的威胁模型。", action:"定位入口和模块关系，将不同解析路径分配给独立任务。", output:"focus_areas：每轮的搜索起点，可手写也可由 --auto-focus 生成。", example:"例如：一个任务检查文件头长度，另一个检查元数据块，第三个检查解码循环。分区是搜索策略，不是覆盖率证明。", source:"docs/pipeline.md"},
  {label:"FIND / 提出假设", title:"沿着输入走，找约束失效的地方。", text:"模型寻找从输入到危险操作的链路：长度是否被校验？分配大小与复制长度是否一致？释放后的对象是否还会被使用？它根据代码语义提出一个可以实验的假设。", input:"分配到的源码区域、可调用入口、已有问题清单。", action:"追踪数据与控制条件，找出可能破坏的安全约束。", output:"可检验假设，以及需要满足哪些条件才能触发。", example:"例如：数量字段先乘以每项大小，再存入更窄的类型；后续循环却仍按原数量写入。假设是“分配大小可能小于写入量”。", source:"harness/prompts/find_prompt.py"},
  {label:"FIND / 实验反馈", title:"写出输入，用程序输出修正判断。", text:"模型生成边界值、截断结构或相互矛盾的字段，调用带 ASAN 的目标。未触发时回看源码、调整输入，必要时换路径。它可以写辅助生成脚本，但框架本身并未提供完整的覆盖率引导模糊测试引擎。", input:"漏洞假设、输入格式、可运行的目标程序。", action:"写输入 → 运行 → 读退出码与诊断 → 调整假设和输入。", output:"实验反馈：正常拒绝、资源问题、断言或内存错误。", example:"例如：长度很大只导致内存耗尽，不满足当前高质量发现标准；改变字段关系后是否出现真正越界，仍需继续验证。", source:"harness/prompts/find_prompt.py"},
  {label:"PoC / 提交产物", title:"保留能复现问题的最小证据。", text:"有效输入要实际写入文件，不能只在回答中声称存在。模型尝试去掉无关字节并重复运行，再提交输入路径、复现命令、崩溃类型、诊断和去重说明。", input:"能触发问题的文件和运行记录。", action:"最小化输入、尝试 3/3 复现、对照已有问题解释差异。", output:"PoC 文件与结构化字段，随后交给独立 Grade。", example:"同一根因可能在不同输入下表现为不同崩溃。新增一条堆栈不一定是新漏洞，需要比较函数、调用路径与根因。", source:"harness/find.py"}
];
function renderStep(index) {
  const step = steps[index];
  document.querySelectorAll("[data-step]").forEach(button => {
    const selected = Number(button.dataset.step) === index;
    button.classList.toggle("active", selected);
    button.setAttribute("aria-pressed", String(selected));
  });
  document.getElementById("step-detail").innerHTML = `<span class="kicker">${step.label}</span><h3>${step.title}</h3><p>${step.text}</p><dl><div><dt>输入</dt><dd>${step.input}</dd></div><div><dt>动作</dt><dd>${step.action}</dd></div><div><dt>产物</dt><dd>${step.output}</dd></div></dl><p class="step-example">${step.example}</p><a class="source-link" href="${upstream + step.source}" target="_blank" rel="noreferrer">这一阶段的源码依据 ↗</a>`;
}
document.querySelectorAll("[data-step]").forEach(button => button.addEventListener("click", () => renderStep(Number(button.dataset.step))));
renderStep(0);

function updateLab() {
  const count = Number(document.getElementById("item-count").value);
  const guard = document.getElementById("guard").checked;
  const needed = count * 4;
  const recorded = needed % 256;
  const rejected = guard && count > 63;
  document.getElementById("count-output").textContent = `${count} 项`;
  document.getElementById("needed-value").textContent = needed;
  document.getElementById("allocated-value").textContent = rejected ? "未分配" : recorded;
  document.getElementById("needed-bar").style.width = `${needed / 360 * 100}%`;
  document.getElementById("allocated-bar").style.width = rejected ? "0%" : `${recorded / 360 * 100}%`;
  document.getElementById("toy-code").textContent = `// 教学伪代码：故意用 8 位长度演示回绕\n数量 = ${count}\n${guard ? "若 数量 > 63：拒绝输入\n" : ""}记录长度 = (数量 × 4) mod 256\n分配(记录长度)\n写入(数量 × 4 字节)`;
  const verdict = document.getElementById("lab-verdict");
  verdict.classList.toggle("warning", !rejected && needed > recorded);
  if (rejected) {
    verdict.innerHTML = "<b>示意修复：先拒绝，再停止处理</b><p>此输入不进入分配与写入。在教学模型中约束成立；真实修复应根据实际类型范围、格式规范和调用路径设计。</p>";
  } else if (needed > recorded) {
    verdict.innerHTML = `<b>假设可检验：需要 ${needed}，却只记录 ${recorded}</b><p>相差 ${needed - recorded} 字节。若真实程序按这个分配量接收全部写入，就可能发生越界；本页没有执行程序，尚未形成真实漏洞证据。</p>`;
  } else {
    verdict.innerHTML = "<b>这个输入没有出现长度回绕</b><p>需要写入的字节与记录长度相等。这只说明当前教学输入没有触发该条件，不能说明其他路径安全。</p>";
  }
}
document.getElementById("item-count").addEventListener("input", updateLab);
document.getElementById("guard").addEventListener("change", updateLab);
document.querySelectorAll("[data-count]").forEach(button => button.addEventListener("click", () => {
  document.getElementById("item-count").value = button.dataset.count;
  updateLab();
}));
updateLab();

const scenarios = {
  parser: {
    title:"新 C/C++ 解析器：保持检测机制，替换目标", status:"原框架约定 · 接入后仍需实测", intro:"当目标可以封装成“程序 + 输入文件”时，优先从目标目录适配开始。",
    contract:[
      ["目标与边界","用户上传文件进入生产解析入口。明确支持的格式、大小限制与调用者权限。"],
      ["输入形式","单个文件，入口封装接收文件路径，再调用真实解析函数。"],
      ["问题信号","ASAN 报告内存错误并指向项目代码；排除单纯内存耗尽、超时与正常拒绝。"],
      ["独立复现","从同一原始镜像创建新容器，复制文件，运行复现命令并记录多次结果。"],
      ["去重与报告","结合崩溃类别、项目堆栈和根因判断；报告说明入口可达性与影响前提。"],
      ["修复验收","重新编译，原输入无 ASAN 报错，已有测试通过，再尝试邻近输入变体。"]
    ],
    changes:["新增 targets/<name>/Dockerfile：构建带 ASAN 的程序和研究工具。","新增 config.yaml：固定版本、容器路径、构建和测试命令。","新增薄入口封装 entry.c 或等效入口，确认覆盖真实解析路径。"],
    preserved:["保持现有 Find → Grade → Judge → Report → Patch 流程。","遵循当前产物和运行约定时，通常无需修改 Python 调度层。","检查检测器生效，正常输入通过，再开始模型搜索。"],
    brief:"请将一个新的 C/C++ 解析器接入当前漏洞发现流水线。\n目标仓库与固定版本：[填写]\n生产入口与攻击者可控输入：[填写]\n环境：可重复构建的容器，入口接收单个文件，启用 ASAN。\n检测标准：项目代码中的内存错误，排除单纯 OOM、超时与正常错误处理。\n请先核对 Dockerfile、入口封装、config.yaml、已有测试与目标约定，再列出具体改动。\n验证：一个正常输入、一个已知错误、独立容器复现；补丁需编译、原输入和回归测试通过。\n本说明是适配任务草稿，不表示目标已经接入或验证。"
  },
  access: {
    title:"Web 越权：从“崩溃”切换到“权限被突破”", status:"迁移建议 · 原框架未直接实现", intro:"不以报错或响应码猜测漏洞，用独立身份和资源归属验证访问结果。",
    contract:[
      ["目标与边界","两个普通用户 A、B，各自拥有私有资源；规范明确彼此不可访问。"],
      ["输入形式","认证会话、请求序列、资源 ID 与初始数据。需要保存完整复现步骤。"],
      ["问题信号","A 的会话实际读到或修改了 B 的私有资源。单独 HTTP 200 或 500 都不够。"],
      ["独立复现","新环境重置数据，重新创建会话和资源，重放请求并检查资源内容或状态。"],
      ["去重与报告","按缺失的授权检查和根因聚合，而不只按 URL；记录身份前提与数据暴露范围。"],
      ["修复验收","跨用户访问被正确拒绝，资源所有者仍可正常访问，相关业务测试通过。"]
    ],
    changes:["目标环境与产物：HTTP 服务、身份种子、请求重放器和状态恢复。","Find / Grade / Judge / Report / Patch 提示词：替换内存错误假设。","artifacts.py、配置和签名解析：保存请求链、身份条件与授权根因。","patch_grade.py：把 ASAN 检查替换为资源访问断言，并适配再次验证。"],
    preserved:["沿用发现与独立验证分离、证据留存、预算与重试思路。","容器与调度代码可部分复用；新状态和输入格式仍需逐处核对。","先用预埋越权问题和正确权限路径校准，不能只替换扫描提示词。"],
    brief:"请提出将当前框架迁移到 Web 资源越权检测的具体方案。\n目标与环境：[填写服务、版本和隔离测试地址]\n权限规范：用户 A 与 B 的私有资源不能相互访问；请核实此规则与业务一致。\n输入：身份会话、请求序列、资源归属与初始测试数据。\n检测：验证 A 是否实际读取或修改 B 的私有资源，不能只看响应状态码。\n复现：使用全新数据和会话独立重放，并保留请求、响应及状态变化证据。\n适配范围：目标运行器、产物结构、发现/验证/报告/补丁提示、去重、补丁验收与环境重置。\n修复验收：跨用户访问被拒绝，所有者访问仍正常，现有测试通过。\n请先列出文件改动与一个有已知答案的校准实验。本方案尚未实现。"
  },
  coupon: {
    title:"优惠券重复核销：先有业务规范，再生成测试", status:"业务测试迁移建议 · 尚未实现", intro:"核心是独立于现有代码的业务断言，以及可重复建立的账户、订单和优惠券状态。",
    contract:[
      ["目标与边界","一次性优惠券对同一用户最多成功核销一次。先核实重试与订单取消规则。"],
      ["输入形式","重复或并发的结算请求，携带测试账号、优惠券、订单和请求标识。"],
      ["问题信号","数据库或权威流水显示成功核销超过一次。重复响应不一定代表重复扣减。"],
      ["独立复现","重新种入未使用优惠券与账户，控制并发时序，多次重放并读取最终状态。"],
      ["去重与报告","按错误状态转换或根因聚合；报告包括前置条件、请求序列和权威状态证据。"],
      ["修复验收","一次性约束成立，合法首单正常，重试、失败与取消行为符合需求；保留回归用例。"]
    ],
    changes:["新增业务规范与断言检查器：不能从现有代码自我推导正确行为。","新增数据种子、并发或重复请求运行器、数据库状态读回与清理。","适配输入产物、发现与验证提示、状态签名和影响报告。","将补丁原输入验收改为业务断言，增加正常路径和持久化回归测试。"],
    preserved:["保留假设 → 实验 → 独立复现 → 修复验收的方法。","异常状态可以不伴随进程崩溃，ASAN 对这类业务规则没有判定能力。","成功核销次数要读权威状态；并发实验未重现只能说明这次未观察到。"],
    brief:"请设计针对一次性优惠券重复核销的自动测试适配方案。\n需求来源与确认人：[填写]\n业务规则：同一用户对同一张一次性优惠券最多成功核销一次；请补充取消、失败和重试语义。\n输入：独立测试账号、未使用优惠券、订单、重复或并发请求。\n检测：以数据库或权威核销流水的成功次数为准，不以重复响应推断重复核销。\n复现：重置初始数据、控制请求时序、保留请求与状态变化，多次独立重放。\n修复验收：一次性约束成立，正常首单、重试和取消流程正确，并保留长期回归测试。\n需要新增运行器、业务断言、状态恢复、结果结构与相应提示词。\n这是业务测试迁移草稿，不是当前仓库内置功能。"
  }
};
let selectedScenario = "parser";
const savedBriefs = Object.fromEntries(Object.entries(scenarios).map(([key, value]) => [key, value.brief]));
function renderScenario(key) {
  selectedScenario = key;
  const scene = scenarios[key];
  document.querySelectorAll("[data-scenario]").forEach(button => {
    const selected = button.dataset.scenario === key;
    button.classList.toggle("active", selected);
    button.setAttribute("aria-pressed", String(selected));
  });
  document.getElementById("scenario-panel").innerHTML = `<div class="scenario-head"><div><h3>${scene.title}</h3><p>${scene.intro}</p></div><span class="pill">${scene.status}</span></div><div class="contract-grid">${scene.contract.map(([title, content], index) => `<article><small>0${index + 1}</small><h4>${title}</h4><p>${content}</p></article>`).join("")}</div><div class="adapt-map"><article><h4>需要改动或准备</h4><ul>${scene.changes.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul></article><article><h4>可复用思路与验证重点</h4><ul>${scene.preserved.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul></article></div><div class="brief-box"><div class="brief-top"><h4><label for="custom-brief">带走一份定制任务说明</label></h4><button id="copy-brief" type="button">复制说明</button></div><textarea id="custom-brief" spellcheck="false">${escapeHtml(savedBriefs[key])}</textarea><p class="copy-status" id="copy-status" role="status">可直接编辑；修改仅保留在当前页面，刷新后重置。</p></div>`;
  document.getElementById("custom-brief").addEventListener("input", event => { savedBriefs[selectedScenario] = event.target.value; });
  document.getElementById("copy-brief").addEventListener("click", async () => {
    const area = document.getElementById("custom-brief");
    const status = document.getElementById("copy-status");
    const text = area.value;
    try {
      if (!navigator.clipboard?.writeText) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(text);
      status.textContent = "已复制当前说明，可粘贴给代码智能体或项目同事。";
    } catch {
      area.focus();
      area.select();
      status.textContent = "浏览器未允许自动复制，已选中全文，请使用 Ctrl+C 或系统复制操作。";
    }
  });
}
document.querySelectorAll("[data-scenario]").forEach(button => button.addEventListener("click", () => renderScenario(button.dataset.scenario)));
renderScenario("parser");

const sources = [
  ["README.md", "能力与默认范围", "交互技能、自动流水线及维护声明"],
  ["harness/prompts/find_prompt.py", "发现问题的指令", "假设、构造输入、价值分级与排除项"],
  ["harness/grade.py", "独立复现", "新容器、PoC 和元数据传递"],
  ["harness/prompts/grade_prompt.py", "验证的五项标准", "重复运行、项目位置与一致性"],
  ["harness/patch_grade.py", "补丁验收", "构建、原输入、测试与再次攻击"],
  [".claude/skills/customize/SKILL.md", "定制技能", "需求澄清、改动映射与校准流程"],
  ["docs/customizing.md", "定制说明", "新检测信号与交互技能参数"],
  ["targets/README.md", "目标接入要求", "Dockerfile、配置和入口封装"],
  ["harness/config.py", "配置字段", "目标路径、构建、测试、搜索区域"],
  ["harness/agent.py", "Claude 调用层", "CLI、工具、消息与会话恢复"],
  ["harness/sandbox.py", "执行隔离", "gVisor、容器和网络出口"],
  ["docs/pipeline.md", "阶段与运行方式", "可选步骤、结果、重试与恢复"],
  ["docs/patching.md", "补丁的证据边界", "验证层级、缺失测试与人工审查"],
  ["docs/threat-model.md", "威胁模型", "资产、入口与信任边界"],
  ["docs/triage.md", "跨轮次分诊", "核实、去重、严重性与归属"]
];
document.getElementById("source-grid").innerHTML = sources.map(([path, title, detail]) => `<a href="${upstream + path}" target="_blank" rel="noreferrer">${title} ↗<span>${detail}</span><code>${path}</code></a>`).join("");
document.querySelectorAll("[data-source]").forEach(link => {
  link.href = upstream + link.dataset.source;
  link.target = "_blank";
  link.rel = "noreferrer";
});

const navLinks = [...document.querySelectorAll(".sidebar nav a")];
function updateNavigation() {
  let current = navLinks[0];
  for (const link of navLinks) {
    const section = document.querySelector(link.getAttribute("href"));
    if (section.getBoundingClientRect().top <= 165) current = link;
  }
  navLinks.forEach(link => {
    const active = link === current;
    link.classList.toggle("active", active);
    if (active) link.setAttribute("aria-current", "location"); else link.removeAttribute("aria-current");
  });
}
let navScheduled = false;
window.addEventListener("scroll", () => {
  if (navScheduled) return;
  navScheduled = true;
  requestAnimationFrame(() => { updateNavigation(); navScheduled = false; });
}, {passive:true});
updateNavigation();
