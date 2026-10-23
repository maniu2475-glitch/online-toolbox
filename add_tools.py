# -*- coding: utf-8 -*-
# 向 index.html / app.js 注入 9 个新工具
import io, re

idx = io.open('index.html', encoding='utf-8').read()

# ---------- 新导航链接 ----------
new_nav = '''      <a href="#tool-hash" data-tool="hash">哈希</a>
      <a href="#tool-ip" data-tool="ip">IP查询</a>
      <a href="#tool-radix" data-tool="radix">进制转换</a>
      <a href="#tool-unit" data-tool="unit">单位换算</a>
      <a href="#tool-case" data-tool="case">大小写</a>
      <a href="#tool-textsort" data-tool="textsort">文本处理</a>
      <a href="#tool-csv" data-tool="csv">CSV转JSON</a>
      <a href="#tool-uuid" data-tool="uuid">UUID</a>
      <a href="#tool-jwt" data-tool="jwt">JWT解码</a>
    </nav>'''
idx = idx.replace('''      <a href="#tool-counter" data-tool="counter">字数</a>
    </nav>''', '''      <a href="#tool-counter" data-tool="counter">字数</a>
''' + new_nav, 1)

# ---------- 首页卡片 ----------
new_cards = '''        <a class="home-card" href="#tool-hash"><div class="hc-icon">#️⃣</div><div class="hc-title">MD5/SHA 哈希</div><div class="hc-desc">MD5、SHA1、SHA256 全支持</div></a>
        <a class="home-card" href="#tool-ip"><div class="hc-icon">🌐</div><div class="hc-title">IP 查询</div><div class="hc-desc">查看您的 IP 与归属地信息</div></a>
        <a class="home-card" href="#tool-radix"><div class="hc-icon">🔢</div><div class="hc-title">进制转换</div><div class="hc-desc">二进制/八进制/十进制/十六进制</div></a>
        <a class="home-card" href="#tool-unit"><div class="hc-icon">📏</div><div class="hc-title">单位换算</div><div class="hc-desc">温度、长度、重量、面积</div></a>
        <a class="home-card" href="#tool-case"><div class="hc-icon">🔤</div><div class="hc-title">大小写转换</div><div class="hc-desc">全大写/小写/首字母/驼峰</div></a>
        <a class="home-card" href="#tool-textsort"><div class="hc-icon">📋</div><div class="hc-title">文本去重/排序</div><div class="hc-desc">去重、排序、去空行、提取</div></a>
        <a class="home-card" href="#tool-csv"><div class="hc-icon">📄</div><div class="hc-title">CSV 转 JSON</div><div class="hc-desc">支持自定义分隔符</div></a>
        <a class="home-card" href="#tool-uuid"><div class="hc-icon">🆔</div><div class="hc-title">UUID 生成器</div><div class="hc-desc">批量生成 UUID v4</div></a>
        <a class="home-card" href="#tool-jwt"><div class="hc-icon">🔑</div><div class="hc-title">JWT 解码</div><div class="hc-desc">解码 Header/Payload，本地运行</div></a>
      </div>'''
idx = re.sub(r'(        <a class="home-card" href="#tool-counter".*?</a>\n)(      </div>)', r'\1' + new_cards.replace('      </div>',''), idx, flags=re.S)
# 上面替换后 home-card 区块结尾的 </div> 需要保留 —— 用更稳妥方式检查
if '#tool-hash"><div class="hc-icon">#️⃣' not in idx:
    raise SystemExit('home card insert failed')

# ---------- 工具面板（插在 </main> 之前） ----------
panels = '''
    <!-- ===== 哈希 ===== -->
    <section class="tool-panel" id="tool-hash">
      <h2>MD5 / SHA 哈希计算</h2>
      <p class="tool-desc">在浏览器本地计算文本的 MD5、SHA-1、SHA-256、SHA-512 哈希值。</p>
      <textarea id="hash-input" rows="4" placeholder="输入要计算哈希的文本"></textarea>
      <div class="btn-group"><button class="btn" onclick="hashCompute()">计算哈希</button></div>
      <div class="result-box" id="hash-out"></div>
    </section>

    <!-- ===== IP 查询 ===== -->
    <section class="tool-panel" id="tool-ip">
      <h2>IP 查询</h2>
      <p class="tool-desc">点击按钮查询您的公网 IP 与归属地信息（调用公开 API，仅查询时发送请求）。</p>
      <div class="btn-group"><button class="btn" onclick="ipLookup()">查询我的 IP</button></div>
      <div class="result-box" id="ip-out">点击按钮开始查询</div>
    </section>

    <!-- ===== 进制转换 ===== -->
    <section class="tool-panel" id="tool-radix">
      <h2>进制转换</h2>
      <p class="tool-desc">输入任意进制数字，同时显示二/八/十/十六进制结果。</p>
      <div class="form-row">
        <select id="radix-from">
          <option value="2">二进制 (2)</option>
          <option value="8">八进制 (8)</option>
          <option value="10" selected>十进制 (10)</option>
          <option value="16">十六进制 (16)</option>
        </select>
        <input type="text" id="radix-input" placeholder="输入数字" oninput="radixConvert()">
      </div>
      <div class="result-box" id="radix-out"></div>
    </section>

    <!-- ===== 单位换算 ===== -->
    <section class="tool-panel" id="tool-unit">
      <h2>单位换算</h2>
      <p class="tool-desc">温度、长度、重量、面积常用单位换算。</p>
      <div class="form-row">
        <select id="unit-cat" onchange="unitChangeCat()">
          <option value="temp">温度</option>
          <option value="length">长度</option>
          <option value="weight">重量</option>
          <option value="area">面积</option>
        </select>
        <input type="number" id="unit-val" value="1" oninput="unitConvert()">
        <select id="unit-from" onchange="unitConvert()"></select>
        <span>→</span>
        <select id="unit-to" onchange="unitConvert()"></select>
      </div>
      <div class="result-box" id="unit-out"></div>
    </section>

    <!-- ===== 大小写 ===== -->
    <section class="tool-panel" id="tool-case">
      <h2>大小写转换</h2>
      <p class="tool-desc">全大写、全小写、首字母大写、驼峰、下划线等多种转换。</p>
      <textarea id="case-input" rows="5" placeholder="输入文本"></textarea>
      <div class="btn-group">
        <button class="btn" onclick="caseDo('upper')">全大写</button>
        <button class="btn" onclick="caseDo('lower')">全小写</button>
        <button class="btn" onclick="caseDo('cap')">首字母大写</button>
        <button class="btn" onclick="caseDo('camel')">驼峰</button>
        <button class="btn" onclick="caseDo('snake')">下划线</button>
      </div>
      <textarea id="case-output" rows="5" class="output-text" readonly placeholder="结果"></textarea>
    </section>

    <!-- ===== 文本处理 ===== -->
    <section class="tool-panel" id="tool-textsort">
      <h2>文本去重 / 排序</h2>
      <p class="tool-desc">按行去重、排序（升/降/长度）、去空行、添加行号、反转。</p>
      <textarea id="tsort-input" rows="8" placeholder="每行一个条目"></textarea>
      <div class="btn-group">
        <button class="btn" onclick="tsort('dedup')">去重</button>
        <button class="btn" onclick="tsort('asc')">升序</button>
        <button class="btn" onclick="tsort('desc')">降序</button>
        <button class="btn" onclick="tsort('len')">按长度</button>
        <button class="btn" onclick="tsort('trim')">去空行</button>
        <button class="btn" onclick="tsort('num')">加行号</button>
        <button class="btn" onclick="tsort('rev')">反转</button>
      </div>
      <textarea id="tsort-output" rows="8" class="output-text" readonly placeholder="结果"></textarea>
    </section>

    <!-- ===== CSV → JSON ===== -->
    <section class="tool-panel" id="tool-csv">
      <h2>CSV 转 JSON</h2>
      <p class="tool-desc">首行为表头，支持逗号/制表符/分号分隔，自动去引号。</p>
      <textarea id="csv-input" rows="8" placeholder="name,age&#10;Tom,18&#10;Jerry,22"></textarea>
      <div class="form-row">
        <select id="csv-sep">
          <option value=",">逗号 ,</option>
          <option value="&#9;">制表符 Tab</option>
          <option value=";">分号 ;</option>
        </select>
      </div>
      <div class="btn-group">
        <button class="btn" onclick="csvToJson()">转换为 JSON</button>
        <button class="btn btn-outline" onclick="csvCopy()">复制结果</button>
      </div>
      <pre id="csv-output" class="output"></pre>
    </section>

    <!-- ===== UUID ===== -->
    <section class="tool-panel" id="tool-uuid">
      <h2>UUID 生成器</h2>
      <p class="tool-desc">使用浏览器加密随机源批量生成 UUID v4。</p>
      <div class="form-row">
        <label>数量：<input type="number" id="uuid-count" min="1" max="100" value="5"></label>
        <label><input type="checkbox" id="uuid-upper"> 大写</label>
      </div>
      <div class="btn-group">
        <button class="btn" onclick="uuidGen()">生成 UUID</button>
        <button class="btn btn-outline" onclick="uuidCopy()">复制</button>
      </div>
      <pre id="uuid-output" class="output"></pre>
    </section>

    <!-- ===== JWT ===== -->
    <section class="tool-panel" id="tool-jwt">
      <h2>JWT 解码</h2>
      <p class="tool-desc">解码 JWT 的 Header 和 Payload（不验证签名，纯本地解码）。</p>
      <textarea id="jwt-input" rows="4" placeholder="粘贴 JWT，形如 eyJhbGciOi..."></textarea>
      <div class="btn-group"><button class="btn" onclick="jwtDecode()">解码</button></div>
      <pre id="jwt-output" class="output"></pre>
    </section>

  </main>'''
idx = idx.replace('\n  </main>', panels, 1)

# ---------- 侧边栏列表 ----------
new_list = '''        <li><a href="#tool-hash">MD5/SHA 哈希</a></li>
        <li><a href="#tool-ip">IP 查询</a></li>
        <li><a href="#tool-radix">进制转换</a></li>
        <li><a href="#tool-unit">单位换算</a></li>
        <li><a href="#tool-case">大小写转换</a></li>
        <li><a href="#tool-textsort">文本去重/排序</a></li>
        <li><a href="#tool-csv">CSV 转 JSON</a></li>
        <li><a href="#tool-uuid">UUID 生成</a></li>
        <li><a href="#tool-jwt">JWT 解码</a></li>
      </ul>'''
idx = idx.replace('''        <li><a href="#tool-counter">字数统计</a></li>
      </ul>''', '''        <li><a href="#tool-counter">字数统计</a></li>
''' + new_list, 1)

# ---------- 更新 SEO 描述 ----------
idx = idx.replace('9 款常用在线小工具', '18 款常用在线小工具')
idx = idx.replace('等9款免费在线工具', '等18款免费在线工具')
idx = idx.replace('Markdown预览、字数统计。纯前端', 'Markdown预览、字数统计、MD5哈希、IP查询、进制转换、单位换算、JWT解码。纯前端')

io.open('index.html', 'w', encoding='utf-8').write(idx)
print('index.html updated')

# ---------- app.js 追加逻辑 ----------
js_extra = u'''
/* ===== v2 新增工具 ===== */

/* 哈希 */
async function hashCompute() {
  const text = document.getElementById('hash-input').value;
  const out = document.getElementById('hash-out');
  if (!text) { out.textContent = '请输入文本'; return; }
  const enc = new TextEncoder().encode(text);
  const results = [];
  results.push('MD5     : ' + (window.md5 ? md5(text) : '需加载库'));
  for (const alg of ['SHA-1', 'SHA-256', 'SHA-512']) {
    const buf = await crypto.subtle.digest(alg, enc);
    const hex = [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
    results.push(alg.padEnd(8, ' ') + ': ' + hex);
  }
  out.textContent = results.join('\\n');
  out.style.whiteSpace = 'pre-wrap';
}

/* IP 查询 */
async function ipLookup() {
  const out = document.getElementById('ip-out');
  out.textContent = '查询中…';
  try {
    const r = await fetch('https://ipapi.co/json/');
    const d = await r.json();
    out.textContent = '您的 IP：' + d.ip + '\\n归属地：' + (d.country_name || '') + ' ' + (d.region || '') + ' ' + (d.city || '') +
      '\\n运营商/组织：' + (d.org || '未知') + '\\n时区：' + (d.timezone || '未知');
  } catch (e) {
    try {
      const r2 = await fetch('https://ip.useragentinfo.com/json');
      const d2 = await r2.json();
      out.textContent = '您的 IP：' + d2.ip + '\\n归属地：' + d2.province + ' ' + d2.city + ' ' + (d2.isp || '');
    } catch (e2) { out.textContent = '❌ 查询失败，请稍后重试'; }
  }
  out.style.whiteSpace = 'pre-wrap';
}

/* 进制转换 */
function radixConvert() {
  const from = +document.getElementById('radix-from').value;
  const val = document.getElementById('radix-input').value.trim();
  const out = document.getElementById('radix-out');
  if (!val) { out.textContent = ''; return; }
  const num = parseInt(val, from);
  if (isNaN(num)) { out.textContent = '❌ 输入不是有效的' + from + '进制数字'; return; }
  out.textContent = '二进制 : ' + num.toString(2) + '\\n八进制 : ' + num.toString(8) +
    '\\n十进制 : ' + num.toString(10) + '\\n十六进制: ' + num.toString(16).toUpperCase();
  out.style.whiteSpace = 'pre-wrap';
}

/* 单位换算 */
const UNITS = {
  temp: [['摄氏度 (°C)', 1, 0], ['华氏度 (°F)', 5/9, -32], ['开尔文 (K)', 1, -273.15]],
  length: [['毫米 (mm)', 1], ['厘米 (cm)', 10], ['米 (m)', 1000], ['千米 (km)', 1e6], ['英寸 (in)', 25.4], ['英尺 (ft)', 304.8], ['英里 (mi)', 1.609e6]],
  weight: [['毫克 (mg)', 1], ['克 (g)', 1000], ['千克 (kg)', 1e6], ['吨 (t)', 1e9], ['盎司 (oz)', 28349.5], ['磅 (lb)', 453592]],
  area: [['平方厘米 (cm²)', 1], ['平方米 (m²)', 1e4], ['平方千米 (km²)', 1e10], ['公顷 (ha)', 1e8], ['英亩 (acre)', 4.047e7]]
};
function unitChangeCat() {
  const cat = document.getElementById('unit-cat').value;
  const list = UNITS[cat];
  const from = document.getElementById('unit-from');
  const to = document.getElementById('unit-to');
  from.innerHTML = list.map((u, i) => '<option value="' + i + '">' + u[0] + '</option>').join('');
  to.innerHTML = from.innerHTML;
  from.selectedIndex = 0; to.selectedIndex = Math.min(1, list.length - 1);
  unitConvert();
}
function unitConvert() {
  const cat = document.getElementById('unit-cat').value;
  const list = UNITS[cat];
  const v = parseFloat(document.getElementById('unit-val').value);
  const out = document.getElementById('unit-out');
  if (isNaN(v)) { out.textContent = ''; return; }
  const f = list[+document.getElementById('unit-from').value];
  const t = list[+document.getElementById('unit-to').value];
  if (cat === 'temp') {
    // 先换算回摄氏度再转到目标
    let c = f[2] === 0 ? v : (v + f[2]) * f[1];
    let result = t[2] === 0 ? c : c / t[1] - t[2];
    out.textContent = v + ' ' + f[0] + ' = ' + +result.toFixed(4) + ' ' + t[0];
  } else {
    const base = v * f[1];
    out.textContent = v + ' ' + f[0] + ' = ' + +(base / t[1]).toPrecision(8) + ' ' + t[0];
  }
}
document.addEventListener('DOMContentLoaded', unitChangeCat);

/* 大小写 */
function caseDo(mode) {
  const text = document.getElementById('case-input').value;
  let r = text;
  if (mode === 'upper') r = text.toUpperCase();
  else if (mode === 'lower') r = text.toLowerCase();
  else if (mode === 'cap') r = text.toLowerCase().replace(/(^|\\s+)([a-z])/g, (m, a, b) => a + b.toUpperCase());
  else if (mode === 'camel') r = text.toLowerCase().replace(/[^a-zA-Z0-9]+(.)?/g, (m, c) => c ? c.toUpperCase() : '');
  else if (mode === 'snake') r = text.replace(/([a-z])([A-Z])/g, '$1_$2').replace(/[\\s-]+/g, '_').toLowerCase();
  document.getElementById('case-output').value = r;
}

/* 文本排序 */
function tsort(mode) {
  const raw = document.getElementById('tsort-input').value;
  let lines = raw.split('\\n');
  if (mode === 'dedup') lines = [...new Set(lines)];
  else if (mode === 'asc') lines.sort((a, b) => a.localeCompare(b, 'zh'));
  else if (mode === 'desc') lines.sort((a, b) => b.localeCompare(a, 'zh'));
  else if (mode === 'len') lines.sort((a, b) => a.length - b.length);
  else if (mode === 'trim') lines = lines.filter(l => l.trim());
  else if (mode === 'num') lines = lines.map((l, i) => (i + 1) + '. ' + l);
  else if (mode === 'rev') lines.reverse();
  document.getElementById('tsort-output').value = lines.join('\\n');
}

/* CSV → JSON */
function csvToJson() {
  const text = document.getElementById('csv-input').value.trim();
  const sep = document.getElementById('csv-sep').value;
  const out = document.getElementById('csv-output');
  if (!text) { out.textContent = '请输入 CSV 内容'; return; }
  const lines = text.split(/\\r?\\n/).filter(l => l.trim());
  const parseLine = l => {
    const cells = [];
    let cur = '', inQ = false;
    for (const ch of l) {
      if (ch === '"' && (inQ || cur === '' || true)) { inQ = !inQ; continue; }
      if (ch === sep && !inQ) { cells.push(cur); cur = ''; } else cur += ch;
    }
    cells.push(cur);
    return cells.map(c => c.trim());
  };
  const header = parseLine(lines[0]);
  const data = lines.slice(1).map(l => {
    const cells = parseLine(l);
    const obj = {};
    header.forEach((h, i) => obj[h] = isNaN(+cells[i]) || cells[i] === '' ? cells[i] : +cells[i]);
    return obj;
  });
  out.textContent = JSON.stringify(data, null, 2);
}
function csvCopy() {
  navigator.clipboard.writeText(document.getElementById('csv-output').textContent).then(() => alert('已复制'));
}

/* UUID */
function uuidGen() {
  const n = Math.min(100, Math.max(1, +document.getElementById('uuid-count').value || 5));
  const upper = document.getElementById('uuid-upper').checked;
  const list = [];
  for (let i = 0; i < n; i++) {
    if (crypto.randomUUID) { list.push(crypto.randomUUID()); }
    else {
      const b = crypto.getRandomValues(new Uint8Array(16));
      b[6] = (b[6] & 15) | 64; b[8] = (b[8] & 63) | 128;
      const h = [...b].map(x => x.toString(16).padStart(2, '0')).join('');
      list.push(h.slice(0,8) + '-' + h.slice(8,12) + '-' + h.slice(12,16) + '-' + h.slice(16,20) + '-' + h.slice(20));
    }
  }
  document.getElementById('uuid-output').textContent = (upper ? list.map(u => u.toUpperCase()) : list).join('\\n');
}
function uuidCopy() {
  navigator.clipboard.writeText(document.getElementById('uuid-output').textContent).then(() => alert('已复制'));
}

/* JWT 解码 */
function jwtDecode() {
  const token = document.getElementById('jwt-input').value.trim();
  const out = document.getElementById('jwt-output');
  const parts = token.split('.');
  if (parts.length < 2) { out.textContent = '❌ 不是有效的 JWT（需要 header.payload.signature 三段）'; return; }
  const dec = s => {
    s = s.replace(/-/g, '+').replace(/_/g, '/');
    while (s.length % 4) s += '=';
    try { return JSON.parse(decodeURIComponent(escape(atob(s)))); } catch (e) { return '❌ 解码失败'; }
  };
  const header = dec(parts[0]), payload = dec(parts[1]);
  let html = 'Header:\\n' + JSON.stringify(header, null, 2) + '\\n\\nPayload:\\n' + JSON.stringify(payload, null, 2);
  if (payload && typeof payload.exp === 'number') {
    const exp = new Date(payload.exp * 1000);
    html += '\\n\\n过期时间：' + exp.toLocaleString('zh-CN', { hour12: false }) + (exp < new Date() ? '（已过期 ⚠️）' : '（有效 ✅）');
  }
  out.textContent = html;
}
'''
app = io.open('app.js', encoding='utf-8').read()
if 'v2 新增工具' not in app:
    io.open('app.js', 'a', encoding='utf-8').write(js_extra)
print('app.js updated')
