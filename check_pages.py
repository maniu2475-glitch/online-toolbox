import subprocess, json, urllib.request, time
GIT = r'C:\Users\ADMIN\AppData\Local\OpenClaw\deps\portable-git\cmd\git.exe'
p = subprocess.run([GIT, 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n',
                   capture_output=True, text=True)
token = dict(l.split('=',1) for l in p.stdout.strip().split('\n') if '=' in l)['password']

def get(path):
    req = urllib.request.Request('https://api.github.com' + path)
    req.add_header('Authorization', 'token ' + token)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

for i in range(10):
    d = get('/repos/maniu2475-glitch/tools-en/pages')
    print('attempt', i, 'status:', d.get('status'))
    if d.get('status') == 'built':
        break
    time.sleep(20)

# 再测 HTTP
import urllib.error
try:
    with urllib.request.urlopen('https://maniu2475-glitch.github.io/tools-en/') as r:
        print('site HTTP:', r.status)
except urllib.error.HTTPError as e:
    print('site HTTP:', e.code)
