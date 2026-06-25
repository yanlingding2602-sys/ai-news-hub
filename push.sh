#!/usr/bin/env bash
# AI 喜讯汇 - GitHub 一键推送脚本
# 用法: ./push.sh YOUR_GITHUB_USERNAME

set -e

USERNAME="$1"

if [ -z "$USERNAME" ]; then
  echo "用法: ./push.sh YOUR_GITHUB_USERNAME"
  echo "示例: ./push.sh johndoe"
  exit 1
fi

echo "========================================"
echo "  AI 喜讯汇 - GitHub Pages 推送"
echo "========================================"
echo ""
echo "目标仓库: https://github.com/$USERNAME/ai-news-hub"
echo ""

# 检查远程仓库是否已配置
if git remote | grep -q origin; then
  echo "[步骤] 更新远程仓库地址..."
  git remote set-url origin "https://github.com/$USERNAME/ai-news-hub.git"
else
  echo "[步骤] 添加远程仓库..."
  git remote add origin "https://github.com/$USERNAME/ai-news-hub.git"
fi

echo "[步骤] 推送到 GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "========================================"
echo "  推送完成！"
echo "========================================"
echo ""
echo "接下来："
echo "1. 访问 https://github.com/$USERNAME/ai-news-hub"
echo "2. 点击 Settings -> Pages"
echo "3. Source 选择 Deploy from a branch -> main -> /(root)"
echo "4. 点击 Save"
echo ""
echo "等待 1-2 分钟后访问："
echo "  https://$USERNAME.github.io/ai-news-hub/"
echo ""
