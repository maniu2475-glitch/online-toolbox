import subprocess, shutil, os
GIT = r'C:\Users\ADMIN\AppData\Local\OpenClaw\deps\portable-git\cmd\git.exe'
if not os.path.exists(GIT):
    GIT = shutil.which('git')
print('using git:', GIT)

# portable git 可能没有 credential manager；先测试 push 是否能走（凭据可能存在 .git-credentials 或 GCM）
p = subprocess.run([GIT, 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n',
                   capture_output=True, text=True)
print('stdout keys:', [l.split('=')[0] for l in p.stdout.strip().split('\n') if '=' in l])
print('stderr:', p.stderr[:200])
info = dict(l.split('=',1) for l in p.stdout.strip().split('\n') if '=' in l)
print('username:', info.get('username'), '| token present:', bool(info.get('password')))
