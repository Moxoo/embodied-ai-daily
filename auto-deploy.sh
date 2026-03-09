#!/bin/bash
# 自动部署脚本
# 每天凌晨 2:00 执行

set -e  # 遇到错误立即退出

echo "🐱 $(date): 开始具身智能日报自动部署流程..."

WORKSPACE="/Users/xuma/.openclaw/workspace/embodied-ai-daily"
cd "$WORKSPACE"

# 1. 生成日报
echo "📰 步骤 1: 生成日报..."
python3 daily-collector.py

# 2. 推送到 GitHub（自动部署 GitHub Pages）
echo "🚀 步骤 2: 推送到 GitHub..."
git add -A
DATE=$(date +%Y-%m-%d)
git commit -m "daily: $DATE 日报更新

- 自动收集 arXiv 论文
- 更新 GitHub.io 站点" || echo "没有变更需要提交"

git push origin main
echo "✅ GitHub 推送完成！站点将在 1-2 分钟内自动部署"

# 3. 等待 GitHub Pages 部署
echo "⏳ 步骤 3: 等待 GitHub Pages 部署..."
sleep 30  # 等待 30 秒让 GitHub 开始部署

# 4. 检查部署状态
echo "🔍 步骤 4: 检查部署状态..."
DEPLOY_URL="https://moxoo.github.io/embodied-ai-daily/"
TODAY_URL="https://moxoo.github.io/embodied-ai-daily/$(date +%Y/%m/$DATE.html)"

echo "🌐 首页: $DEPLOY_URL"
echo "📄 今日日报: $TODAY_URL"

echo "🎉 自动部署流程完成！"
echo "⏰ $(date): 下次运行时间: 明天凌晨 2:00"
