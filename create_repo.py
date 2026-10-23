import subprocess, json, urllib.request
GIT = r'C:\Users\ADMIN\AppData\Local\OpenClaw\deps\portable-git\cmd\git.exe'
p = subprocess.run([GIT, 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n',
                   capture_output=True, text=True)
info = dict(l.split('=',1) for l in p.stdout.strip().split('\n') if '=' in l)
token = info['password']

def api(path, data=None, method=None):
    req = urllib.request.Request('https://api.github.com' + path)
    req.add_header('Authorization', 'token ' + token)
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('Content-Type', 'application/json')
    if data is not None:
        req.data = json.dumps(data).encode()
    if method:
        req.get_method = lambda: method
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read().decode() or '{}')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]

# 1. 创建 tools-en 仓库
print('create repo:', api('/user/repos', {'name': 'tools-en', 'public': True,
    'description': '18 free online tools, 100% browser-side: JSON formatter, Base64, QR code, MD5/SHA hash, UUID, JWT decoder and more.',
    'homepage': 'https://maniu2475-glitch.github.io/tools-en/'}))

# 2. 启用 Pages
print('pages:', api('/repos/maniu2475-glitch/tools-en/pages', {'source': {'branch': 'main', 'path': '/'}}))
