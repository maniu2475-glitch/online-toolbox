# 在线工具箱（ToolBox）

一个纯前端的免费在线小工具集合网站，可部署到 **GitHub Pages**，挂载 Google AdSense 广告实现被动收入。

## ✨ 功能（18 个工具）

| 工具 | 说明 |
|------|------|
| JSON 格式化/校验 | 美化、压缩、错误定位 |
| Base64 编解码 | 支持中文（UTF-8） |
| URL 编解码 | encodeURIComponent / decode |
| 二维码生成 | qrcode.js，自定义尺寸，可下载 PNG |
| 密码生成器 | crypto 随机源，长度/字符集可调，熵强度评估 |
| 时间戳转换 | Unix 秒/毫秒 ↔ 日期，实时时钟 |
| 颜色转换/配色 | HEX/RGB/HSL 互转 + 互补/类似/三角配色方案 |
| Markdown 预览 | marked.js 实时渲染（GFM） |
| 字数统计 | 字符/中文/英文单词/行/段/字节 |
| MD5/SHA 哈希 | 多种哈希算法计算 |
| IP 归属地查询 | IP 地址信息查询 |
| 进制转换 | 二进制/八进制/十进制/十六进制互转 |
| 单位换算 | 长度/重量/温度等单位转换 |
| 大小写转换 | 英文大小写、驼峰、下划线转换 |
| 文本排序去重 | 文本行排序与去重 |
| CSV 转 JSON | CSV 格式转 JSON |
| UUID 生成器 | 批量生成 UUID v4 |
| JWT 解码 | 解析 JWT header/payload |

**特点：**
- 纯前端，零后端，数据不上传（隐私安全，利于 SEO 转化）
- 响应式设计，完美支持手机端
- SEO 友好：meta title/description/keywords、Open Graph、语义化标签
- 预留 4 处广告位（顶部 Banner、侧边栏 300x250、侧边栏 300x600、底部 Banner）

## 📁 目录结构

```
tool-site/
├── index.html    # 主页面（含全部工具与广告位）
├── style.css     # 样式（响应式）
├── app.js        # 工具逻辑
├── favicon.svg   # 图标
├── robots.txt    # SEO
├── sitemap.xml   # SEO
├── 404.html      # GitHub Pages 404 页
├── README.md     # 本文件
└── deploy.sh     # 一键部署脚本
```

## 🚀 方式一：一键部署（deploy.sh）

```bash
cd tool-site
./deploy.sh <你的GitHub用户名> <仓库名>
# 例如: ./deploy.sh myname tools
```

脚本会自动：初始化 git → 提交 → 创建 GitHub 仓库（需 gh CLI，或先手动在网页建仓）→ 推送 → 通过 GitHub API 启用 Pages。

### 手动部署（网页操作，无需命令行）

1. 登录 GitHub，点击 **New repository**，创建名为 `tools`（或任意名）的**公开**仓库
2. 上传本目录所有文件（网页端 Add file → Upload files，或 `git push`）
3. 进入仓库 **Settings → Pages**
4. Source 选择 **Deploy from a branch**，分支选 `main`，目录选 `/ (root)`，点 Save
5. 等待 1~2 分钟，访问 `https://<用户名>.github.io/tools/` 即可

### 方式二：用 deploy.py（Python，需要 GitHub Token）

```bash
python3 deploy.py
# 按提示输入 GitHub 用户名、Token（repo 权限）、仓库名
```

## 💰 挂载 AdSense 广告

1. 注册 [Google AdSense](https://adsense.google.com)，提交网站审核（网站需有真实内容，通常需运营几天到几周）
2. 审核通过后，在 `index.html` 的 `<head>` 中加入 AdSense 全局脚本：
   ```html
   <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-你的ID" crossorigin="anonymous"></script>
   ```
3. 将页面中 4 个广告占位 div 替换为 AdSense 广告单元代码，例如：
   ```html
   <!-- 顶部 banner，替换 <div class="ad-banner" id="ad-top"> 内容 -->
   <ins class="adsbygoogle" style="display:block"
        data-ad-client="ca-pub-你的ID"
        data-ad-slot="广告位ID"
        data-ad-format="auto"
        data-full-width-responsive="true"></ins>
   <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
   ```
4. 队列里 `ad-placeholder-text` 的占位文字删除即可。

## 🔍 SEO 说明

- `robots.txt` 与 `sitemap.xml` 已生成，记得将 sitemap 中的域名改为你的实际地址并提交到 [Google Search Console](https://search.google.com/search-console)
- 后续可扩展：每个工具单独页面 + 独立 URL，覆盖更多长尾关键词（如"json 在线格式化"、"base64 解码"）

## 📄 License

MIT

## 🌍 英文站（同步运营）

英文站 <https://maniu2475-glitch.github.io/tools-en/> 共 **43 个工具**（2026-10-24），包括：

- JSON/Base64/URL 编解码、二维码生成与扫描、密码生成与强度检查
- 时间戳、颜色转换与取色器、Markdown、字数统计、哈希、IP、进制、单位、大小写
- 文本排序/对比/转二进制、CSV→JSON、UUID、JWT、Base32
- Cron 解析与生成器、宽高比计算、随机字符串、Slug、HTML 实体、图片转 Base64、Lorem Ipsum、URL 解析
- 计算器类：百分比、BMI、年龄、贷款月供、复利、折扣、随机数
- 开发工具：chmod 权限计算、正则测试、温度换算
