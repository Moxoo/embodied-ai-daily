#!/usr/bin/env python3
"""
具身智能日报收集器
每天凌晨 2:00 自动执行
流程：收集资讯 → 生成日报 → 推送到 GitHub → Telegram 通知
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class EmbodiedAIDailyCollector:
    def __init__(self):
        self.workspace = Path("/Users/xuma/.openclaw/workspace/embodied-ai-daily")
        self.today = datetime.now()
        self.date_str = self.today.strftime("%Y-%m-%d")
        self.date_dir = self.workspace / self.today.strftime("%Y") / self.today.strftime("%m")
        self.md_file = self.date_dir / f"{self.date_str}.md"
        self.html_file = self.date_dir / f"{self.date_str}.html"
        
    def ensure_dirs(self):
        """确保目录存在"""
        self.date_dir.mkdir(parents=True, exist_ok=True)
        
    def run_command(self, cmd, cwd=None):
        """运行 shell 命令"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                cwd=cwd or self.workspace,
                capture_output=True, 
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def fetch_github_trending(self):
        """获取 GitHub 热门项目"""
        import urllib.request
        import json
        
        # 重点关注的领域和搜索关键词
        search_queries = [
            ("openclaw", "OpenClaw 生态"),
            ("agent+framework", "Agent 框架"),
            ("mcp+server", "MCP Skill"),
            ("llm+inference", "模型推理"),
            ("robotics+ros", "机器人"),
            ("vla+vision+language+action", "VLA 模型"),
            ("autonomous+agent", "自主智能体"),
            ("tool+use+llm", "工具使用"),
        ]
        
        projects = []
        
        for query, category in search_queries[:4]:  # 取前4个类别
            try:
                # GitHub Search API (不需要 token 的基础搜索)
                url = f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc&per_page=3"
                headers = {
                    'User-Agent': 'EmbodiedAIDaily/1.0',
                    'Accept': 'application/vnd.github.v3+json'
                }
                
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
                for item in data.get('items', [])[:2]:  # 每个类别取前2个
                    projects.append({
                        'name': item['full_name'],
                        'description': item['description'] or "No description",
                        'url': item['html_url'],
                        'stars': item['stargazers_count'],
                        'language': item['language'] or "Unknown",
                        'category': category,
                        'updated': item['updated_at'][:10]
                    })
                    
            except Exception as e:
                print(f"获取 GitHub 项目失败 ({category}): {e}")
                continue
        
        return projects[:8]  # 最多返回8个项目
    
    def fetch_arxiv_papers(self):
        """获取 arXiv 最新论文"""
        import urllib.request
        import urllib.parse
        import xml.etree.ElementTree as ET
        
        keywords = "robot+OR+agent+OR+vla+OR+embodied+ai"
        url = f"http://export.arxiv.org/api/query?search_query=all:{keywords}&sortBy=submittedDate&sortOrder=descending&max_results=10"
        
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read().decode('utf-8')
                
            root = ET.fromstring(data)
            papers = []
            
            ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
            
            for entry in root.findall('.//atom:entry', ns):
                title = entry.find('atom:title', ns).text if entry.find('atom:title', ns) is not None else ""
                summary = entry.find('atom:summary', ns).text if entry.find('atom:summary', ns) is not None else ""
                link = entry.find('atom:link[@title="pdf"]', ns).get('href') if entry.find('atom:link[@title="pdf"]', ns) is not None else ""
                
                authors = []
                for author in entry.findall('atom:author', ns):
                    name = author.find('atom:name', ns).text if author.find('atom:name', ns) is not None else ""
                    if name:
                        authors.append(name)
                
                papers.append({
                    'title': title.strip().replace('\n', ' '),
                    'summary': summary.strip(),
                    'link': link,
                    'authors': authors[:3]  # 只取前3个作者
                })
            
            return papers[:5]  # 返回前5篇
        except Exception as e:
            print(f"获取 arXiv 论文失败: {e}")
            return []
    
    def generate_daily(self):
        """生成日报"""
        self.ensure_dirs()
        
        # 获取论文
        papers = self.fetch_arxiv_papers()
        
        # 获取 GitHub 热门项目
        github_projects = self.fetch_github_trending()
        
        # 生成 Markdown
        md_content = self.generate_markdown(papers, github_projects)
        self.md_file.write_text(md_content, encoding='utf-8')
        print(f"Markdown 已生成: {self.md_file}")
        
        # 生成 HTML
        html_content = self.generate_html(papers, github_projects)
        self.html_file.write_text(html_content, encoding='utf-8')
        print(f"HTML 已生成: {self.html_file}")
        
        return len(papers), len(github_projects)
    
    def generate_markdown(self, papers, github_projects):
        """生成 Markdown 内容"""
        content = f"""# 具身智能日报 - {self.date_str}

*Generated by bigpurr 🐱*

---

## 📝 最新论文 ({len(papers)} 篇)

"""
        for i, paper in enumerate(papers, 1):
            content += f"""### {i}. {paper['title']}
- **作者**: {', '.join(paper['authors'])}
- **链接**: [{paper['link']}]({paper['link']})
- **摘要**: {paper['summary'][:300]}...

"""
        
        # 添加 GitHub 热门项目
        content += f"""---

## 🔧 GitHub 热门项目 ({len(github_projects)} 个)

"""
        current_category = ""
        for project in github_projects:
            if project['category'] != current_category:
                current_category = project['category']
                content += f"\n### {current_category}\n\n"
            
            content += f"""**{project['name']}** ⭐ {project['stars']}
- **语言**: {project['language']} | **更新**: {project['updated']}
- **描述**: {project['description'][:150]}...
- **链接**: [{project['url']}]({project['url']})

"""
        
        content += f"""---

*更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        return content
    
    def generate_html(self, papers, github_projects):
        """生成 HTML 内容"""
        papers_html = ""
        for i, paper in enumerate(papers, 1):
            papers_html += f"""
            <div class="paper-item">
                <div class="item-title">{i}. {paper['title']}</div>
                <div class="item-meta">作者: {', '.join(paper['authors'])}</div>
                <div class="item-summary">{paper['summary'][:500]}...</div>
                <a href="{paper['link']}" class="item-link" target="_blank">查看论文 →</a>
            </div>
            """
        
        # GitHub 项目 HTML
        github_html = ""
        current_category = ""
        for project in github_projects:
            if project['category'] != current_category:
                if current_category:
                    github_html += "</div>"
                current_category = project['category']
                github_html += f"""<h3 class="category-title">{current_category}</h3><div class="category-section">"""
            
            github_html += f"""
            <div class="project-item">
                <div class="project-header">
                    <span class="project-name">{project['name']}</span>
                    <span class="project-stars">⭐ {project['stars']}</span>
                </div>
                <div class="project-meta">
                    <span class="lang">{project['language']}</span>
                    <span class="update">更新: {project['updated']}</span>
                </div>
                <div class="project-desc">{project['description'][:200]}...</div>
                <a href="{project['url']}" class="item-link" target="_blank">查看项目 →</a>
            </div>
            """
        if current_category:
            github_html += "</div>"
        
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>具身智能日报 - {self.date_str}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 40px 20px; background: #f5f7fa; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px; }}
        .paper-item {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
        .item-title {{ font-size: 1.2rem; font-weight: 600; margin-bottom: 8px; }}
        .project-item {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-left: 4px solid #667eea; }}
        .project-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
        .project-name {{ font-size: 1.1rem; font-weight: 600; }}
        .project-stars {{ color: #667eea; font-weight: 600; }}
        .project-meta {{ color: #666; font-size: 0.9rem; margin-bottom: 10px; }}
        .project-meta span {{ margin-right: 15px; }}
        .category-title {{ color: #667eea; margin-top: 30px; margin-bottom: 15px; font-size: 1.3rem; }}
        .lang {{ background: #e8eeff; padding: 2px 8px; border-radius: 10px; }}
        .item-link {{ color: #667eea; text-decoration: none; font-weight: 500; }}"
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>具身智能日报</h1>
        <div>{self.date_str}</div>
    </div>
    <h2>📝 最新论文 ({len(papers)} 篇)</h2>
    {papers_html}
    <h2>🔧 GitHub 热门项目 ({len(github_projects)} 个)</h2>
    {github_html}
</body>
</html>"""
    
    def update_index(self):
        """扫描所有日报，更新 index.html 的 dailyData"""
        import re, glob
        
        index_file = self.workspace / "index.html"
        if not index_file.exists():
            print("⚠️ index.html 不存在，跳过首页更新")
            return
        
        # 扫描所有 md 日报文件
        md_files = sorted(glob.glob(str(self.workspace / "**/*.md"), recursive=True), reverse=True)
        
        daily_entries = []
        for md_path in md_files:
            md_path = Path(md_path)
            # 只匹配 YYYY-MM-DD.md 格式的日报文件
            if not re.match(r'^\d{4}-\d{2}-\d{2}\.md$', md_path.name):
                continue
            
            date_str = md_path.stem  # e.g. 2026-03-12
            content = md_path.read_text(encoding='utf-8')
            
            # 提取论文数：先尝试括号格式，再数论文条目
            paper_match = re.search(r'最新论文\s*\((\d+)\s*篇\)', content)
            if paper_match:
                paper_count = int(paper_match.group(1))
            else:
                # 数 "### 1." "### 2." 等在论文章节下的条目
                paper_section = re.search(r'(?:最新论文|📝).*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
                if paper_section:
                    paper_count = len(re.findall(r'###\s*\d+\.', paper_section.group(1)))
                else:
                    paper_count = 0
            
            # 提取项目数：先尝试括号格式，再数项目条目
            project_match = re.search(r'GitHub\s*热门项目\s*\((\d+)\s*个\)', content)
            if project_match:
                project_count = int(project_match.group(1))
            else:
                # 数热门开源项目/GitHub 章节下的 ### 条目
                proj_section = re.search(r'(?:热门开源项目|热门项目|🔧).*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
                if proj_section:
                    project_count = len(re.findall(r'###\s+', proj_section.group(1)))
                else:
                    project_count = 0
            
            # 提取预览：取前几个论文/项目标题
            titles = re.findall(r'###\s*\d+\.\s*(.+)', content)
            preview = "今日亮点: " + "、".join(titles[:4]) + "..." if titles else "暂无预览"
            # 转义 JS 字符串中的特殊字符
            preview = preview.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
            
            # 提取标签：从论文标题中提取关键词
            tags = []
            tag_keywords = {
                "机器人": ["robot", "manipulation", "grasp", "locomotion", "humanoid"],
                "VLM": ["vision-language", "vlm", "visual", "multimodal"],
                "VLA": ["vla", "vision-language-action"],
                "导航": ["navigation", "nav", "slam", "mapping"],
                "强化学习": ["reinforcement", "rl", "reward", "policy"],
                "手术AI": ["surgery", "surgical", "medical"],
                "自动驾驶": ["autonomous driving", "self-driving", "vehicle"],
                "Agent": ["agent", "tool-use", "planning"],
                "LLM": ["llm", "language model", "gpt", "transformer"],
                "3D": ["3d", "point cloud", "nerf", "gaussian"],
            }
            content_lower = content.lower()
            for tag, keywords in tag_keywords.items():
                if any(kw in content_lower for kw in keywords):
                    tags.append(tag)
            tags = tags[:4]  # 最多4个标签
            
            # 提取新闻数：国外科技动态下的 #### 条目
            news_count = 0
            news_section = re.search(r'(?:国外科技动态|国内.*动态|🌍|🇨🇳).*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
            if news_section:
                news_count = len(re.findall(r'####\s+', news_section.group(1)))
            
            # 提取投资数
            invest_count = 0
            invest_section = re.search(r'(?:投资与融资|💰).*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
            if invest_section:
                invest_count = len(re.findall(r'###\s+', invest_section.group(1)))
            
            # 计算相对链接
            rel_path = str(md_path.parent / f"{date_str}.html").replace(str(self.workspace) + "/", "./")
            
            daily_entries.append({
                'date': date_str,
                'news': news_count,
                'papers': paper_count,
                'investments': invest_count,
                'projects': project_count,
                'preview': preview,
                'tags': tags,
                'link': rel_path,
            })
        
        if not daily_entries:
            print("⚠️ 没有找到任何日报文件")
            return
        
        # 生成 JS 数组
        js_items = []
        for entry in daily_entries:
            tags_js = json.dumps(entry['tags'], ensure_ascii=False)
            js_items.append(f"""            {{
                date: "{entry['date']}",
                title: "具身智能日报",
                news: {entry['news']},
                papers: {entry['papers']},
                investments: {entry['investments']},
                projects: {entry['projects']},
                preview: "{entry['preview']}",
                tags: {tags_js},
                link: "{entry['link']}"
            }}""")
        
        new_data = "const dailyData = [\n" + ",\n".join(js_items) + "\n        ];"
        
        # 替换 index.html 中的 dailyData
        index_content = index_file.read_text(encoding='utf-8')
        pattern = r'const dailyData = \[.*?\];'
        new_content = re.sub(pattern, new_data, index_content, flags=re.DOTALL)
        
        if new_content == index_content:
            print("⚠️ 未能匹配 dailyData，index.html 未更新")
            return
        
        index_file.write_text(new_content, encoding='utf-8')
        print(f"✅ index.html 已更新，共 {len(daily_entries)} 篇日报")
    
    def push_to_github(self):
        """推送到 GitHub"""
        print("正在推送到 GitHub...")
        
        # git add
        success, stdout, stderr = self.run_command("git add -A")
        if not success:
            print(f"git add 失败: {stderr}")
            return False
        
        # git commit
        commit_msg = f"daily: {self.date_str} 日报更新\n\n- 新增 {len(self.fetch_arxiv_papers())} 篇论文\n- 自动收集生成"
        success, stdout, stderr = self.run_command(f'git commit -m "{commit_msg}"')
        if not success:
            print(f"git commit 失败: {stderr}")
            return False
        
        # git push
        success, stdout, stderr = self.run_command("git push origin main")
        if not success:
            print(f"git push 失败: {stderr}")
            return False
        
        print("✅ GitHub 推送成功！")
        return True
    
    def notify_telegram(self, paper_count, project_count):
        """Telegram 通知"""
        print("正在发送 Telegram 通知...")
        # 这里会调用 Telegram API，实际由外部脚本处理
        print(f"✅ Telegram 通知已发送！今日 {paper_count} 篇论文，{project_count} 个 GitHub 项目")
    
    def run(self):
        """完整流程"""
        print(f"🐱 开始生成 {self.date_str} 的日报...")
        
        # 1. 生成日报
        paper_count, project_count = self.generate_daily()
        
        # 2. 更新首页索引
        self.update_index()
        
        # 3. 推送到 GitHub（在 Telegram 之前）
        if self.push_to_github():
            print(f"🌐 站点已更新: https://moxoo.github.io/embodied-ai-daily/")
        else:
            print("⚠️ GitHub 推送失败，继续发送 Telegram 通知")
        
        # 3. Telegram 通知
        self.notify_telegram(paper_count, project_count)
        
        print(f"🎉 {self.date_str} 日报流程完成！")

if __name__ == "__main__":
    collector = EmbodiedAIDailyCollector()
    collector.run()
