#!/usr/bin/env python3
# ===== GitHub Pages 一键部署脚本（Python 版，需 requests）=====
# 用法: python3 deploy.py
# 交互式输入 GitHub 用户名、Token（需 repo 权限）、仓库名
import os
import sys
import json
import subprocess
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def sh(cmd, cwd=HERE):
    print(">>>", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def api(url, token, data=None, method=None):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    if data is not None:
        req.data = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    if method:
        req.get_method = lambda: method
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def main():
    username = input("GitHub 用户名: ").strip()
    token = input("GitHub Token (repo 权限): ").strip()
    repo = input("仓库名 (默认 tools): ").strip() or "tools"

    # 1. git init / commit
    if not os.path.exists(os.path.join(HERE, ".git")):
        sh(["git", "init", "-b", "main"])
    sh(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", "Deploy: 在线工具箱"],
                   cwd=HERE, check=False)

    # 2. 创建远程仓库（已存在则忽略 422）
    code, resp = api("https://api.github.com/user/repos", token,
                     {"name": repo, "public": True})
    print(f"创建仓库: HTTP {code}", "（已存在，继续）" if code == 422 else "")

    # 3. 推送
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo}.git"
    proc = subprocess.run(["git", "remote"], cwd=HERE, capture_output=True, text=True)
    if "origin" in proc.stdout:
        sh(["git", "remote", "set-url", "origin", remote_url])
    else:
        sh(["git", "remote", "add", "origin", remote_url])
    sh(["git", "push", "-u", "origin", "main"])

    # 4. 启用 Pages
    code, resp = api(f"https://api.github.com/repos/{username}/{repo}/pages",
                     token, {"source": {"branch": "main", "path": "/"}})
    print(f"启用 Pages: HTTP {code}（201=成功，409=已启用）")

    print(f"\n✅ 部署完成！1-2 分钟后访问:\n   https://{username}.github.io/{repo}/")


if __name__ == "__main__":
    main()
