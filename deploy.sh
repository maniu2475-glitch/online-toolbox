#!/usr/bin/env bash
# ===== GitHub Pages 一键部署脚本 =====
# 用法: ./deploy.sh <github用户名> <仓库名> [github_token]
#   - 若提供 token（repo 权限），将自动创建远程仓库并通过 API 启用 Pages
#   - 若不提供 token，请先在网页上手动创建仓库，脚本只负责推送
set -e

USERNAME="${1:?用法: ./deploy.sh <github用户名> <仓库名> [token]}"
REPO="${2:?用法: ./deploy.sh <github用户名> <仓库名> [token]}"
TOKEN="${3:-}"

cd "$(dirname "$0")"

if [ ! -d .git ]; then
  git init -b main
fi
git add -A
git commit -m "Deploy: 在线工具箱 $(date +%Y-%m-%d)" || true

if [ -n "$TOKEN" ]; then
  # 通过 API 自动创建仓库（若已存在则忽略错误）
  echo ">>> 正在通过 API 创建仓库 ${USERNAME}/${REPO} ..."
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
    -H "Authorization: token ${TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    https://api.github.com/user/repos \
    -d "{\"name\":\"${REPO}\",\"public\":true}")
  echo "    创建仓库返回状态: ${HTTP_CODE} (201=新建成功, 422=已存在)"

  if [ -z "$(git remote | grep origin)" ]; then
    git remote add origin "https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/${REPO}.git"
  else
    git remote set-url origin "https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/${REPO}.git"
  fi
else
  if [ -z "$(git remote | grep origin)" ]; then
    git remote add origin "https://github.com/${USERNAME}/${REPO}.git"
  fi
fi

echo ">>> 推送到 GitHub ..."
git push -u origin main

# 启用 GitHub Pages（主分支根目录）
if [ -n "$TOKEN" ]; then
  echo ">>> 通过 API 启用 GitHub Pages ..."
  curl -s -X POST \
    -H "Authorization: token ${TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    https://api.github.com/repos/${USERNAME}/${REPO}/pages \
    -d '{"source":{"branch":"main","path":"/"}}'
  echo ""
  echo "✅ 部署完成！稍等 1-2 分钟后访问:"
  echo "   https://${USERNAME}.github.io/${REPO}/"
else
  echo "✅ 推送完成！请到仓库 Settings → Pages 手动启用 Pages（分支 main / 目录 /）"
  echo "   之后访问: https://${USERNAME}.github.io/${REPO}/"
fi
