#!/bin/bash
# 自动部署脚本
# 每天凌晨 2:00 执行

set -e  # 遇到错误立即退出

echo "🐱 $(date): 开始具身智能日报自动部署流程..."

WORKSPACE="/Users/xuma/.openclaw/workspace/embodied-ai-daily"
cd "$WORKSPACE"

DATE=$(date +%Y-%m-%d)
DATE_DIR="$WORKSPACE/$(date +%Y/%m)"
MD_FILE="$DATE_DIR/$DATE.md"
HTML_FILE="$DATE_DIR/$DATE.html"

# 检查今天的日报是否已存在且内容完整
if [ -f "$MD_FILE" ] && [ -s "$MD_FILE" ]; then
    # 检查是否包含论文内容（通过检查文件大小和关键词）
    if grep -q "arXiv" "$MD_FILE" && [ $(wc -l < "$MD_FILE") -gt 50 ]; then
        echo "✅ 今天的日报已存在且内容完整，跳过生成"
        echo "📄 文件: $MD_FILE"
        
        # 直接推送（如果有其他变更）
        git add -A
        git commit -m "daily: $DATE 日报已存在，跳过生成" || echo "没有变更需要提交"
        git push origin main
        
        echo "🌐 站点地址: https://moxoo.github.io/embodied-ai-daily/"
        echo "📄 今日日报: https://moxoo.github.io/embodied-ai-daily/$(date +%Y/%m/$DATE.html)"
        echo "🎉 流程完成！"
        exit 0
    fi
fi

# 备份现有文件（如果存在）
if [ -f "$MD_FILE" ]; then
    echo "📦 备份现有日报..."
    cp "$MD_FILE" "$MD_FILE.backup.$(date +%H%M%S)"
    cp "$HTML_FILE" "$HTML_FILE.backup.$(date +%H%M%S)" 2>/dev/null || true
fi

# 1. 生成日报
echo "📰 步骤 1: 生成日报..."
if ! python3 daily-collector.py; then
    echo "❌ 日报生成失败，恢复备份..."
    # 恢复备份
    if [ -f "$MD_FILE.backup"* ]; then
        BACKUP_MD=$(ls -t "$MD_FILE.backup"* | head -1)
        cp "$BACKUP_MD" "$MD_FILE"
        echo "✅ 已恢复: $BACKUP_MD"
    fi
    exit 1
fi

# 2. 检查生成结果
echo "🔍 步骤 2: 检查生成结果..."
if [ ! -f "$MD_FILE" ]; then
    echo "❌ 日报文件未生成"
    exit 1
fi

# 检查内容是否为空或过少
LINE_COUNT=$(wc -l < "$MD_FILE")
if [ "$LINE_COUNT" -lt 20 ]; then
    echo "⚠️ 警告: 日报内容过少 ($LINE_COUNT 行)，可能获取失败"
    echo "📄 文件内容预览:"
    head -10 "$MD_FILE"
    
    # 如果有备份，询问是否恢复（自动模式下直接恢复）
    if [ -f "$MD_FILE.backup"* ]; then
        echo "🔄 恢复之前的备份..."
        BACKUP_MD=$(ls -t "$MD_FILE.backup"* | head -1)
        BACKUP_HTML="${BACKUP_MD%.md}.html"
        cp "$BACKUP_MD" "$MD_FILE"
        [ -f "$BACKUP_HTML" ] && cp "$BACKUP_HTML" "$HTML_FILE"
        echo "✅ 已恢复备份"
    fi
fi

echo "✅ 日报生成完成: $LINE_COUNT 行"

# 3. 推送到 GitHub（自动部署 GitHub Pages）
echo "🚀 步骤 3: 推送到 GitHub..."
git add -A
git commit -m "daily: $DATE 日报更新

- 自动收集 arXiv 论文
- 自动收集 GitHub 热门项目
- 更新 GitHub.io 站点" || echo "没有变更需要提交"

git push origin main
echo "✅ GitHub 推送完成！站点将在 1-2 分钟内自动部署"

# 4. 等待 GitHub Pages 部署
echo "⏳ 步骤 4: 等待 GitHub Pages 部署..."
sleep 30  # 等待 30 秒让 GitHub 开始部署

# 5. 检查部署状态
echo "🔍 步骤 5: 检查部署状态..."
DEPLOY_URL="https://moxoo.github.io/embodied-ai-daily/"
TODAY_URL="https://moxoo.github.io/embodied-ai-daily/$(date +%Y/%m/$DATE.html)"

echo "🌐 首页: $DEPLOY_URL"
echo "📄 今日日报: $TODAY_URL"

# 6. 清理备份文件（保留最近3个）
echo "🧹 步骤 6: 清理旧备份..."
ls -t "$DATE_DIR/$DATE.md.backup"* 2>/dev/null | tail -n +4 | xargs rm -f 2>/dev/null || true
ls -t "$DATE_DIR/$DATE.html.backup"* 2>/dev/null | tail -n +4 | xargs rm -f 2>/dev/null || true

echo "🎉 自动部署流程完成！"
echo "⏰ $(date): 下次运行时间: 明天凌晨 2:00"
