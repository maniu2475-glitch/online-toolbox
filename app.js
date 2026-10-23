/* ===== 在线工具箱 app.js ===== */
"use strict";

/* ---------- 导航与面板切换 ---------- */
function initNav() {
  const toggle = document.getElementById('menuToggle');
  const nav = document.getElementById('mainNav');
  toggle.addEventListener('click', () => nav.classList.toggle('open'));

  nav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => nav.classList.remove('open'));
  });

  window.addEventListener('hashchange', showPanel);
  showPanel();
}

function showPanel() {
  let id = location.hash.replace('#', '') || 'home';
  const panels = document.querySelectorAll('.tool-panel');
  const target = document.getElementById('tool-' + id);
  if (!target) id = 'home';
  panels.forEach(p => p.classList.toggle('active', p.id === 'tool-' + id));
  // 高亮导航
  document.querySelectorAll('.main-nav a').forEach(a =>
    a.classList.toggle('active', a.dataset.tool === id));
  // 预填时间戳
  if (id === 'timestamp') startClock();
  window.scrollTo(0, 0);
}

/* ---------- JSON ---------- */
function getJsonInput() { return document.getElementById('json-input').value; }
function setJsonOutput(text) { document.getElementById('json-output').textContent = text; }

function jsonFormat() {
  try {
    const obj = JSON.parse(getJsonInput());
    setJsonOutput(JSON.stringify(obj, null, 2));
  } catch (e) { setJsonOutput('❌ JSON 校验错误：' + e.message); }
}
function jsonMinify() {
  try {
    const obj = JSON.parse(getJsonInput());
    setJsonOutput(JSON.stringify(obj));
  } catch (e) { setJsonOutput('❌ JSON 校验错误：' + e.message); }
}
function jsonValidate() {
  try {
    JSON.parse(getJsonInput());
    setJsonOutput('✅ JSON 格式正确');
  } catch (e) { setJsonOutput('❌ JSON 校验错误：' + e.message); }
}
function jsonCopy() {
  const text = document.getElementById('json-output').textContent;
  navigator.clipboard.writeText(text).then(() => alert('已复制到剪贴板'));
}

/* ---------- Base64 / URL ---------- */
function utf8ToB64(str) { return btoa(unescape(encodeURIComponent(str))); }
function b64ToUtf8(b64) { return decodeURIComponent(escape(atob(b64))); }
function b64Encode() {
  try { document.getElementById('b64-output').value = utf8ToB64(document.getElementById('b64-input').value); }
  catch (e) { document.getElementById('b64-output').value = '❌ 编码失败：' + e.message; }
}
function b64Decode() {
  try { document.getElementById('b64-output').value = b64ToUtf8(document.getElementById('b64-input').value.trim()); }
  catch (e) { document.getElementById('b64-output').value = '❌ 解码失败：输入不是有效的 Base64'; }
}
function urlEncode() { document.getElementById('url-output').value = encodeURIComponent(document.getElementById('url-input').value); }
function urlDecode() {
  try { document.getElementById('url-output').value = decodeURIComponent(document.getElementById('url-input').value); }
  catch (e) { document.getElementById('url-output').value = '❌ 解码失败：' + e.message; }
}
function swapText(aId, bId) {
  const a = document.getElementById(aId), b = document.getElementById(bId);
  [a.value, b.value] = [b.value, a.value];
}

/* ---------- 二维码 ---------- */
let qrSize = 200;
document.addEventListener('DOMContentLoaded', () => {
  const sizeEl = document.getElementById('qr-size');
  if (sizeEl) {
    sizeEl.addEventListener('input', () => {
      qrSize = +sizeEl.value;
      document.getElementById('qr-size-val').textContent = qrSize;
    });
  }
});
function qrGenerate() {
  const text = document.getElementById('qr-input').value.trim();
  const box = document.getElementById('qr-output');
  box.innerHTML = '';
  if (!text) { box.innerHTML = '<p style="color:#9aa1ad">请输入内容后再生成</p>'; return; }
  if (typeof QRCode === 'undefined') { box.innerHTML = '<p style="color:#d93025">二维码库加载失败，请检查网络</p>'; return; }
  new QRCode(box, { text, width: qrSize, height: qrSize, correctLevel: QRCode.CorrectLevel.M });
}
function qrDownload() {
  const img = document.querySelector('#qr-output img');
  if (!img) { alert('请先生成二维码'); return; }
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = qrSize;
  canvas.getContext('2d').drawImage(img, 0, 0, qrSize, qrSize);
  const a = document.createElement('a');
  a.href = canvas.toDataURL('image/png');
  a.download = 'qrcode.png';
  a.click();
}

/* ---------- 密码生成 ---------- */
function pwdGenerate() {
  const len = +document.getElementById('pwd-length').value;
  let chars = '';
  if (document.getElementById('pwd-upper').checked) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  if (document.getElementById('pwd-lower').checked) chars += 'abcdefghijklmnopqrstuvwxyz';
  if (document.getElementById('pwd-digit').checked) chars += '0123456789';
  if (document.getElementById('pwd-symbol').checked) chars += '!@#$%^&*()-_=+[]{};:,.<>?';
  if (!chars) { document.getElementById('pwd-output').textContent = '请至少选择一种字符类型'; return; }
  const noDup = document.getElementById('pwd-nodup').checked;
  let pwd = '';
  const rand = new Uint32Array(len * 4);
  crypto.getRandomValues(rand);
  for (let i = 0; i < rand.length && pwd.length < len; i++) {
    const c = chars[rand[i] % chars.length];
    if (noDup && pwd.includes(c)) continue;
    pwd += c;
  }
  if (noDup && pwd.length < len && chars.length < len) {
    document.getElementById('pwd-output').textContent = '⚠️ 字符集过小，无法生成不重复的 ' + len + ' 位密码';
    return;
  }
  document.getElementById('pwd-output').textContent = pwd;
  updateStrength(pwd, chars.length);
}
function pwdCopy() {
  navigator.clipboard.writeText(document.getElementById('pwd-output').textContent)
    .then(() => alert('已复制到剪贴板'));
}
function updateStrength(pwd, pool) {
  const bits = pwd.length * Math.log2(pool || 2);
  const bar = document.getElementById('pwd-strength');
  const txt = document.getElementById('pwd-strength-text');
  let pct, label, color;
  if (bits < 40) { pct = 25; label = '弱'; color = '#d93025'; }
  else if (bits < 60) { pct = 50; label = '中等'; color = '#f9ab00'; }
  else if (bits < 100) { pct = 75; label = '强'; color = '#1e8e3e'; }
  else { pct = 100; label = '极强'; color = '#0d652d'; }
  bar.style.width = pct + '%';
  bar.style.background = color;
  txt.textContent = '强度评估：' + label + '（约 ' + Math.round(bits) + ' 位熵）';
}

/* ---------- 时间戳 ---------- */
let clockTimer = null;
function startClock() {
  if (clockTimer) return;
  const tick = () => {
    const now = Date.now();
    const el = document.getElementById('ts-now');
    if (el) el.textContent = Math.floor(now / 1000) + ' s / ' + now + ' ms';
  };
  tick();
  clockTimer = setInterval(tick, 1000);
}
function tsToDate() {
  let ts = document.getElementById('ts-input').value.trim();
  const out = document.getElementById('ts-date-out');
  if (!/^\d{10,13}$/.test(ts)) { out.textContent = '❌ 请输入 10 位（秒）或 13 位（毫秒）数字时间戳'; return; }
  if (ts.length === 10) ts = +ts * 1000;
  const d = new Date(+ts);
  out.textContent = '本地时间：' + d.toLocaleString('zh-CN', { hour12: false })
    + '\nUTC：' + d.toISOString();
  out.style.whiteSpace = 'pre-wrap';
}
function dateToTs() {
  const v = document.getElementById('date-input').value;
  const out = document.getElementById('ts-out2');
  if (!v) { out.textContent = '❌ 请选择日期时间'; return; }
  const d = new Date(v);
  out.textContent = '秒级：' + Math.floor(d.getTime() / 1000)
    + '\n毫秒级：' + d.getTime()
    + '\nISO：' + d.toISOString();
  out.style.whiteSpace = 'pre-wrap';
}

/* ---------- 颜色 ---------- */
function hexToRgb(hex) {
  hex = hex.replace('#', '');
  if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
  if (!/^[0-9a-fA-F]{6}$/.test(hex)) return null;
  return [parseInt(hex.slice(0,2),16), parseInt(hex.slice(2,4),16), parseInt(hex.slice(4,6),16)];
}
function rgbToHsl(r, g, b) {
  r/=255; g/=255; b/=255;
  const max = Math.max(r,g,b), min = Math.min(r,g,b);
  let h=0, s=0, l=(max+min)/2;
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d/(2-max-min) : d/(max+min);
    if (max===r) h = ((g-b)/d + (g<b?6:0));
    else if (max===g) h = ((b-r)/d + 2);
    else h = ((r-g)/d + 4);
    h /= 6;
  }
  return [Math.round(h*360), Math.round(s*100), Math.round(l*100)];
}
function hslToHex(h, s, l) {
  s/=100; l/=100;
  const f = n => {
    const k = (n + h/30) % 12;
    const a = s * Math.min(l, 1-l);
    const c = l - a * Math.min(-1, Math.min(k-3, Math.min(9-k, 1)));
    return Math.round(255*c).toString(16).padStart(2,'0');
  };
  return '#' + f(0)+f(8)+f(4);
}
function colorUpdate(fromHex) {
  const hex = document.getElementById('color-hex').value.trim();
  const rgb = hexToRgb(hex);
  if (!rgb) return;
  document.getElementById('color-picker').value = '#' + hex.replace('#','').toLowerCase();
  renderColor(rgb, hex.startsWith('#') ? hex.toLowerCase() : ('#' + hex.toLowerCase()));
}
function colorFromHex() { colorUpdate(); }
function renderColor(rgb, hex) {
  const [h, s, l] = rgbToHsl(...rgb);
  document.getElementById('color-info').textContent =
    'HEX: ' + hex + '   RGB: rgb(' + rgb.join(', ') + ')   HSL: hsl(' + h + ', ' + s + '%, ' + l + '%)';
  // 配色方案
  const schemes = {
    '互补色': [hslToHex((h+180)%360, s, l)],
    '类似色': [hslToHex((h+30)%360, s, l), hslToHex((h-30+360)%360, s, l)],
    '三角': [hslToHex((h+120)%360, s, l), hslToHex((h+240)%360, s, l)],
    '明暗': [hslToHex(h, s, Math.min(l+20,95)), hslToHex(h, s, Math.max(l-20,5))],
  };
  const out = document.getElementById('palette-out');
  out.innerHTML = '';
  const items = [['主色', hex]].concat(Object.entries(schemes).flatMap(([k, arr]) => arr.map(c => [k, c])));
  items.forEach(([name, c]) => {
    const div = document.createElement('div');
    div.className = 'palette-item';
    div.innerHTML = '<div class="palette-swatch" style="background:' + c + '"></div><div class="palette-label">' + name + '<br>' + c + '</div>';
    div.title = '点击复制 ' + c;
    div.style.cursor = 'pointer';
    div.onclick = () => navigator.clipboard.writeText(c).then(() => div.title = '已复制!');
    out.appendChild(div);
  });
}
// 取色器变化
document.addEventListener('DOMContentLoaded', () => {
  const picker = document.getElementById('color-picker');
  if (picker) picker.addEventListener('input', () => {
    document.getElementById('color-hex').value = picker.value.toUpperCase();
    colorUpdate();
  });
  colorUpdate();
});

/* ---------- Markdown ---------- */
function mdRender() {
  const input = document.getElementById('md-input');
  const out = document.getElementById('md-output');
  if (!input || !out || typeof marked === 'undefined') return;
  marked.setOptions({ breaks: true, gfm: true });
  out.innerHTML = marked.parse(input.value);
}
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('md-input');
  if (input) {
    input.addEventListener('input', mdRender);
    mdRender();
  }
  startClock();
});

/* ---------- 字数统计 ---------- */
function countText() {
  const text = document.getElementById('count-input').value;
  const chars = text.length;
  const charsNoSpace = text.replace(/\s/g, '').length;
  const cjk = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const words = (text.replace(/[\u4e00-\u9fa5]/g, ' ').match(/[A-Za-z0-9_'-]+/g) || []).length;
  const lines = text ? text.split('\n').length : 0;
  const paragraphs = text.trim() ? text.trim().split(/\n\s*\n/).length : 0;
  const bytes = new Blob([text]).size;
  const stats = [
    [chars, '总字符数'], [charsNoSpace, '不含空格'], [cjk, '中文字数'],
    [words, '英文单词数'], [lines, '行数'], [paragraphs, '段落数'], [bytes, '字节数'],
  ];
  document.getElementById('count-output').innerHTML = stats.map(([n, l]) =>
    '<div class="stat-item"><div class="stat-num">' + n + '</div><div class="stat-label">' + l + '</div></div>').join('');
}

/* ---------- 初始化 ---------- */
document.addEventListener('DOMContentLoaded', initNav);
