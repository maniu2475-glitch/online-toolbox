# -*- coding: utf-8 -*-
# 生成英文工具站（复用工具逻辑，翻译 UI，替换 CSS 变量主题色）
import io, re, os

os.makedirs('en-site', exist_ok=True)
h = io.open('index.html', encoding='utf-8').read()
css = io.open('style.css', encoding='utf-8').read()
js = io.open('app.js', encoding='utf-8').read()

# ---- index.html ----
h = h.replace('lang="zh-CN"', 'lang="en"')
h = h.replace('在线工具箱 - JSON格式化、Base64、二维码、密码生成等免费在线小工具',
  'Free Online Tools - JSON Formatter, Base64, QR Code, Hash, UUID & More')
h = h.replace('免费在线工具箱：JSON格式化校验、Base64编解码、URL编解码、二维码生成、密码生成器、时间戳转换、颜色转换配色、Markdown预览、字数统计、MD5哈希、IP查询、进制转换、单位换算、JWT解码。纯前端运行，数据不上传，安全快速。',
  'Free online toolbox: JSON formatter & validator, Base64, URL encode, QR code generator, password generator, timestamp converter, color palette, Markdown preview, word counter, MD5/SHA hash, IP lookup, radix converter, unit converter, JWT decoder. 100% browser-side, no data uploaded.')
h = h.replace('在线工具,JSON格式化,JSON校验,Base64编码,URL编码,二维码生成,密码生成器,时间戳转换,Unix时间戳,颜色转换,配色方案,Markdown预览,字数统计,免费工具',
  'online tools,json formatter,json validator,base64 encode,url encode,qr code generator,password generator,timestamp converter,unix timestamp,md5 hash generator,sha256,ip lookup,uuid generator,jwt decoder,unit converter,free tools')
h = h.replace('og:title" content="在线工具箱 - 免费在线小工具合集"', 'og:title" content="Free Online Toolbox - 18 Handy Web Tools"')
h = h.replace('og:description" content="JSON格式化、Base64、二维码、密码生成、时间戳转换等18款免费在线工具，纯前端运行，数据不上传。"',
  'og:description" content="18 free online tools: JSON formatter, Base64, QR code, hash generator, UUID, JWT decoder. All run locally in your browser."')
h = h.replace('og:locale" content="zh_CN"', 'og:locale" content="en_US"')
h = h.replace('🧰</span>\n      <span class="logo-text">在线工具箱', '🧰</span>\n      <span class="logo-text">ToolBox')

# nav labels
for zh, en in [('JSON','JSON'),('Base64','Base64'),('URL','URL'),('二维码','QR Code'),('密码','Password'),
               ('时间戳','Timestamp'),('颜色','Colors'),('Markdown','Markdown'),('字数','Word Count'),
               ('哈希','Hash'),('IP查询','IP Lookup'),('进制转换','Radix'),('单位换算','Units'),
               ('大小写','Case'),('文本处理','Text Tools'),('CSV转JSON','CSV→JSON'),('UUID','UUID'),('JWT解码','JWT')]:
    pass  # nav uses data-tool already; labels below

nav_map = {'JSON</a>':'JSON</a>','Base64</a>':'Base64</a>','URL</a>':'URL</a>','二维码</a>':'QR Code</a>',
  '密码</a>':'Password</a>','时间戳</a>':'Timestamp</a>','颜色</a>':'Colors</a>','Markdown</a>':'Markdown</a>',
  '字数</a>':'Word Count</a>','哈希</a>':'Hash</a>','IP查询</a>':'IP Lookup</a>','进制转换</a>':'Radix</a>',
  '单位换算</a>':'Units</a>','大小写</a>':'Case</a>','文本处理</a>':'Text</a>','CSV转JSON</a>':'CSV→JSON</a>',
  'UUID</a>':'UUID</a>','JWT解码</a>':'JWT</a>'}
for k, v in nav_map.items():
    h = h.replace('data-tool="' + k.rstrip('</a>') + '">' + k, 'data-tool="' + k.rstrip('</a>') + '">' + v.replace('→','&#8594;'))

h = h.replace('免费在线工具箱', 'Free Online Toolbox')
h = h.replace('18 款常用在线小工具，纯浏览器本地运行，<strong>数据不上传服务器</strong>，安全、快速、免费。',
  '18 handy online tools that run <strong>entirely in your browser</strong> — fast, private, and free. No data ever leaves your device.')

card_map = {
 'JSON 格式化/校验':'JSON Formatter / Validator','格式化、压缩、校验错误行号':'Beautify, minify, validate with error lines',
 'Base64 编解码':'Base64 Encode / Decode','支持中文与任意文本':'UTF-8 safe, any text',
 'URL 编解码':'URL Encode / Decode','encodeURIComponent / decodeURI':'encodeURIComponent / decodeURI',
 '二维码生成':'QR Code Generator','自定义尺寸，可下载 PNG':'Custom size, download PNG',
 '密码生成器':'Password Generator','可调长度与字符集，强度评估':'Adjustable length & charset, strength meter',
 '时间戳转换':'Unix Timestamp Converter','Unix 秒/毫秒与日期互转':'Unix sec/ms ↔ date, live clock',
 '颜色转换/配色':'Color Converter & Palettes','HEX/RGB/HSL 互转 + 配色方案':'HEX/RGB/HSL + color schemes',
 'Markdown 预览':'Markdown Preview','实时渲染，支持表格/代码块':'Live render, GFM tables & code',
 '字数统计':'Word Counter','字符/词/行/中英文分别统计':'Chars, words, lines, bytes',
 'MD5/SHA 哈希':'MD5 / SHA Hash','MD5、SHA1、SHA256 全支持':'MD5, SHA-1, SHA-256, SHA-512',
 'IP 查询':'IP Lookup','查看您的 IP 与归属地信息':'Your public IP & geolocation',
 '进制转换':'Radix / Base Converter','二进制/八进制/十进制/十六进制':'Binary, octal, decimal, hex',
 '单位换算':'Unit Converter','温度、长度、重量、面积':'Temperature, length, weight, area',
 '大小写转换':'Case Converter','全大写/小写/首字母/驼峰':'UPPER, lower, Title, camelCase, snake_case',
 '文本去重/排序':'Text Dedup & Sort','去重、排序、去空行、提取':'Dedupe, sort, trim, number, reverse',
 'CSV 转 JSON':'CSV to JSON','支持自定义分隔符':'Custom delimiter supported',
 'UUID 生成器':'UUID Generator','批量生成 UUID v4':'Batch generate UUID v4',
 'JWT 解码':'JWT Decoder','解码 Header/Payload，本地运行':'Decode header/payload locally',
}
for k, v in card_map.items():
    h = h.replace('<div class="hc-title">' + k + '</div>', '<div class="hc-title">' + v + '</div>')

# section headings & descs
sec_map = [
 ('<h2>JSON 格式化 / 校验</h2>','<h2>JSON Formatter / Validator</h2>'),
 ('粘贴 JSON 文本，支持格式化（美化）、压缩、错误定位校验。','Paste JSON text to beautify, minify, or validate with error location.'),
 ('<h2>Base64 编码 / 解码</h2>','<h2>Base64 Encode / Decode</h2>'),
 ('支持中文（UTF-8）的 Base64 编码与解码。','Base64 encode & decode, UTF-8 safe.'),
 ('<h2>URL 编码 / 解码</h2>','<h2>URL Encode / Decode</h2>'),
 ('对文本进行 URL 编码（encodeURIComponent）或解码。','URL-encode or decode text using encodeURIComponent.'),
 ('<h2>二维码生成器</h2>','<h2>QR Code Generator</h2>'),
 ('输入文本或网址，生成二维码，可右键保存或点击下载 PNG。','Enter text or a URL, generate a QR code, download as PNG.'),
 ('<h2>密码生成器</h2>','<h2>Password Generator</h2>'),
 ('使用浏览器加密随机源生成高强度密码。','Generate strong passwords using browser crypto randomness.'),
 ('点击下方按钮生成密码','Click the button to generate a password'),
 ('位</label>','</label>'),
 ('大写字母 A-Z','Uppercase A-Z'),('小写字母 a-z','Lowercase a-z'),('数字 0-9','Digits 0-9'),
 ('符号 !@#$%…','Symbols !@#$%…'),('不含重复字符','No duplicate chars'),
 ('<h2>Unix 时间戳转换</h2>','<h2>Unix Timestamp Converter</h2>'),
 ('当前时间：','Current time:'),('每秒自动刷新）','auto-refreshes every second)'),
 ('时间戳 → 日期','Timestamp → Date'),('日期 → 时间戳','Date → Timestamp'),
 ('取当前秒','Now (sec)'),('转换</button>','Convert</button>'),
 ('<h2>颜色转换 & 配色方案</h2>','<h2>Color Converter & Palettes</h2>'),
 ('选择颜色，查看 HEX / RGB / HSL 表示，并生成配色方案。','Pick a color to see HEX / RGB / HSL and generate schemes.'),
 ('配色方案','Color Schemes'),('<h2>Markdown 实时预览</h2>','<h2>Live Markdown Preview</h2>'),
 ('左侧输入 Markdown，右侧实时渲染（支持表格、代码块等 GFM 语法）。','Type Markdown on the left, see rendered output on the right (GFM).'),
 ('<h2>字数统计</h2>','<h2>Word Counter</h2>'),
 ('统计字符数、单词数、中文字数、行数、段落数，实时更新。','Live counts of characters, words, lines, paragraphs and bytes.'),
 ('在此粘贴或输入文本…','Paste or type text here…'),
 ('<h2>MD5 / SHA 哈希计算</h2>','<h2>MD5 / SHA Hash Calculator</h2>'),
 ('在浏览器本地计算文本的 MD5、SHA-1、SHA-256、SHA-512 哈希值。','Compute MD5, SHA-1, SHA-256 and SHA-512 hashes locally in your browser.'),
 ('输入要计算哈希的文本','Enter text to hash'),('计算哈希','Compute Hash'),
 ('<h2>IP 查询</h2>','<h2>IP Lookup</h2>'),
 ('点击按钮查询您的公网 IP 与归属地信息（调用公开 API，仅查询时发送请求）。','Click to look up your public IP and location (calls a public API only on demand).'),
 ('点击按钮开始查询','Click the button to start'),('查询我的 IP','Look up my IP'),
 ('<h2>进制转换</h2>','<h2>Radix / Base Converter</h2>'),
 ('输入任意进制数字，同时显示二/八/十/十六进制结果。','Enter a number in any base; see binary, octal, decimal and hex at once.'),
 ('二进制 (2)','Binary (2)'),('八进制 (8)','Octal (8)'),('十进制 (10)','Decimal (10)'),('十六进制 (16)','Hex (16)'),
 ('输入数字','Enter number'),
 ('<h2>单位换算</h2>','<h2>Unit Converter</h2>'),
 ('温度、长度、重量、面积常用单位换算。','Convert temperature, length, weight and area units.'),
 ('温度','Temperature'),('长度','Length'),('重量','Weight'),('面积','Area'),
 ('<h2>大小写转换</h2>','<h2>Case Converter</h2>'),
 ('全大写、全小写、首字母大写、驼峰、下划线等多种转换。','UPPERCASE, lowercase, Title Case, camelCase, snake_case.'),
 ('全大写','UPPER'),('全小写','lower'),('首字母大写','Title'),('驼峰','camelCase'),('下划线','snake_case'),
 ('<h2>文本去重 / 排序</h2>','<h2>Text Dedup & Sort</h2>'),
 ('按行去重、排序（升/降/长度）、去空行、添加行号、反转。','Dedupe lines, sort asc/desc/length, remove empty lines, add line numbers, reverse.'),
 ('每行一个条目','One item per line'),('去重','Dedup'),('升序','Sort A-Z'),('降序','Sort Z-A'),
 ('按长度','By Length'),('去空行','Remove Blanks'),('加行号','Number Lines'),('反转','Reverse'),
 ('<h2>CSV 转 JSON</h2>','<h2>CSV to JSON</h2>'),
 ('首行为表头，支持逗号/制表符/分号分隔，自动去引号。','First row is the header. Supports comma, tab and semicolon delimiters.'),
 ('转换为 JSON','Convert to JSON'),('逗号 ,','Comma ,'),('制表符 Tab','Tab'),('分号 ;','Semicolon ;'),
 ('<h2>UUID 生成器</h2>','<h2>UUID Generator</h2>'),
 ('使用浏览器加密随机源批量生成 UUID v4。','Batch-generate random UUID v4 with browser crypto.'),
 ('数量：','Count:'),('大写','Uppercase'),('生成 UUID','Generate UUIDs'),
 ('<h2>JWT 解码</h2>','<h2>JWT Decoder</h2>'),
 ('解码 JWT 的 Header 和 Payload（不验证签名，纯本地解码）。','Decode a JWT header and payload (no signature verification, fully local).'),
 ('粘贴 JWT，形如 eyJhbGciOi...','Paste a JWT like eyJhbGciOi...'),
 ('隐私说明','Privacy'),('所有工具均在您的浏览器本地运行，数据不会上传到任何服务器。','All tools run locally in your browser. No data is uploaded to any server.'),
 ('工具列表','All Tools'),
 ('© 2025 在线工具箱 · 纯前端本地运行 · 数据不上传','© 2025 ToolBox · Runs 100% client-side · No data uploaded'),
 ('广告位（728x90 / 响应式）— 此处稍后放置 AdSense 代码','Ad slot (728x90 / responsive) — AdSense code goes here'),
 ('广告位（300x250）<br>此处稍后放置 AdSense 代码','Ad slot (300x250)<br>AdSense code goes here'),
 ('广告位（300x600）','Ad slot (300x600)'),
 ('广告位（响应式横幅）— 此处稍后放置 AdSense 代码','Ad slot (responsive banner) — AdSense code goes here'),
 ('在此粘贴 JSON','Paste JSON here'),
 ('输入文本或 Base64 字符串','Enter text or Base64 string'),
 ('编码 →','Encode →'),('← 解码','← Decode'),('⇅ 交换','⇅ Swap'),
 ('输入文本或已编码的 URL','Enter text or an encoded URL'),
 ('输入网址或文本，如 https://example.com','Enter a URL or text, e.g. https://example.com'),
 ('生成二维码','Generate QR Code'),('下载 PNG','Download PNG'),
 ('生成密码','Generate Password'),('复制','Copy'),
 ('结果','Result'),
]
for k, v in sec_map:
    h = h.replace(k, v)

# sidebar list
h = h.replace('JSON 格式化/校验</a>','JSON Formatter</a>').replace('Base64 编解码</a>','Base64</a>')
h = h.replace('URL 编解码</a>','URL Encode</a>').replace('二维码生成</a>','QR Code</a>')
h = h.replace('密码生成器</a>','Password Gen</a>').replace('时间戳转换</a>','Timestamp</a>')
h = h.replace('颜色/配色</a>','Colors</a>').replace('Markdown 预览</a>','Markdown</a>')
h = h.replace('字数统计</a>','Word Count</a>').replace('MD5/SHA 哈希</a>','Hash</a>')
h = h.replace('IP 查询</a>','IP Lookup</a>').replace('进制转换</a>','Radix</a>')
h = h.replace('单位换算</a>','Units</a>').replace('大小写转换</a>','Case</a>')
h = h.replace('文本去重/排序</a>','Text Dedup</a>').replace('CSV 转 JSON</a>','CSV→JSON</a>')
h = h.replace('UUID 生成</a>','UUID</a>').replace('JWT 解码</a>','JWT</a>')
h = h.replace('欢迎','Welcome').replace('在线工具箱 - 免费在线小工具合集','Free Online Tools')

h = h.replace('https://maniu2475-glitch.github.io/online-toolbox/', 'https://maniu2475-glitch.github.io/tools-en/')

io.open('en-site/index.html', 'w', encoding='utf-8').write(h)

# ---- style.css: 换主题色为绿色系，仅变量替换 ----
css = css.replace('#4f6ef7', '#2563eb')
io.open('en-site/style.css', 'w', encoding='utf-8').write(css)

# ---- app.js: 保留全部逻辑，改输出文案为英文 ----
js = js.replace("'\\n归属地：'","'\\nLocation: '").replace("'\\n运营商/组织：'","'\\nOrg: '").replace("'\\n时区：'","'\\nTimezone: '")
js = js.replace("'您的 IP：'","'Your IP: '").replace("'查询中…'","'Looking up…'").replace("'❌ 查询失败，请稍后重试'","'❌ Lookup failed, try again later'")
js = js.replace("'❌ 输入不是有效的' + from + '进制数字'","'❌ Not a valid base-' + from + ' number'")
js = js.replace("'二进制 : '","'Binary : '").replace("'\\n八进制 : '","'\\nOctal  : '").replace("'\\n十进制 : '","'\\nDecimal: '").replace("'\\n十六进制: '","'\\nHex    : '")
js = js.replace("'过期时间：'","'Expires: '").replace("'（已过期 ⚠️）'","' (EXPIRED ⚠️)'").replace("'（有效 ✅）'","' (valid ✅)'")
js = js.replace("'❌ 不是有效的 JWT（需要 header.payload.signature 三段）'","'❌ Invalid JWT (expected header.payload.signature)'")
js = js.replace("'❌ 解码失败'","'❌ Decode failed'")
js = js.replace("'❌ 请输入 10 位（秒）或 13 位（毫秒）数字时间戳'","'❌ Enter a 10-digit (sec) or 13-digit (ms) timestamp'")
js = js.replace("'本地时间：'","'Local: '")
js = js.replace("'秒级：'","'Seconds: '").replace("'毫秒级：'","'Millis: '")
js = js.replace("'❌ 请选择日期时间'","'❌ Pick a date & time'")
js = js.replace("'请输入文本'","'Enter some text'")
js = js.replace("'❌ JSON 校验错误：'","'❌ JSON error: '")
js = js.replace("'✅ JSON 格式正确'","'✅ Valid JSON'")
js = js.replace("'已复制到剪贴板'","'Copied to clipboard'")
js = js.replace("'请至少选择一种字符类型'","'Select at least one character type'")
js = js.replace("'⚠️ 字符集过小，无法生成不重复的 ' + len + ' 位密码'","'⚠️ Charset too small for a unique ' + len + '-char password'")
js = js.replace("'强度评估：'","'Strength: '")
js = js.replace("'弱'","'Weak'").replace("'中等'","'Fair'").replace("'强'","'Strong'").replace("'极强'","'Very strong'")
js = js.replace("'位熵'","' bits of entropy'")
js = js.replace("'请输入内容后再生成'","'Enter content first'")
js = js.replace("'二维码库加载失败，请检查网络'","'QR library failed to load'")
js = js.replace("'请先生成二维码'","'Generate a QR code first'")
js = js.replace("'总字符数'","'Characters'").replace("'不含空格'","'No spaces'").replace("'中文字数'","'CJK chars'")
js = js.replace("'英文单词数'","'Words'").replace("'行数'","'Lines'").replace("'段落数'","'Paragraphs'").replace("'字节数'","'Bytes'")
js = js.replace("'❌ 解码失败：输入不是有效的 Base64'","'❌ Not valid Base64'")
js = js.replace("'❌ 解码失败：'","'❌ Decode failed: '")
js = js.replace("'需加载库'","'library not loaded'")
js = js.replace("'请输入 CSV 内容'","'Enter CSV content'")
js = js.replace("toLocaleString('zh-CN'","toLocaleString('en-US'")
io.open('en-site/app.js', 'w', encoding='utf-8').write(js)

# copy favicon
import shutil
shutil.copy('favicon.svg', 'en-site/favicon.svg')
print('en-site generated')
