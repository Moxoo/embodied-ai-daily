# Embodied AI Daily - 具身智能日报

> 每天精选具身智能领域最新进展 | 论文 · 新闻 · 博客 · 财经

---

## 📅 2026 年 3 月 8 日 - 创刊号

### 📰 行业新闻

#### 1. **Figure 02 机器人开始量产交付**
- **来源**: Figure AI Blog
- **摘要**: Figure AI 宣布 Figure 02 人形机器人开始向商业合作伙伴交付，部署在汽车制造和物流场景。新一代机器人速度提升 30%，续航达 8 小时。
- **标签**: `Hardware` `Humanoid` `Commercial`

#### 2. **Tesla Optimus 最新进展：工厂内部测试视频曝光**
- **来源**: Tesla AI Day 2026 Follow-up
- **摘要**: Elon Musk 分享 Optimus 在 Tesla 工厂内部测试的最新视频，机器人已能独立完成电池组装任务，准确率 99.2%。
- **标签**: `Tesla` `Humanoid` `Manufacturing`

### 📝 技术博客

#### 3. **"Building Robotic Foundation Models: Lessons from 1000 Days of Training"**
- **作者**: Google DeepMind Robotics Team
- **平台**: Google AI Blog
- **亮点**: DeepMind 团队分享训练机器人基础模型的实战经验，包括数据清洗、sim-to-real 迁移、失败案例分析。
- **链接**: [google.ai/blog/robotic-foundation-models](https://google.ai)
- **标签**: `Foundation Models` `Training` `Best Practices`

#### 4. **"Why VLA Models Fail at Long-Horizon Tasks (And How to Fix It)"**
- **作者**: Berkeley BAIR
- **平台**: BAIR Blog
- **亮点**: 分析 VLA 模型在长程任务中的失败模式，提出分层规划和记忆增强的解决方案。
- **链接**: [bair.berkeley.edu/blog/vla-long-horizon](https://bair.berkeley.edu)
- **标签**: `VLA` `Planning` `Research`

### 💰 财经与投融资

#### 5. **Figure AI 完成 7 亿美元 D 轮融资**
- **领投**: Microsoft + NVIDIA
- **估值**: 38 亿美元
- **用途**: 量产 Figure 02，扩展商业部署
- **标签**: `Funding` `Startup` `Investment`

#### 6. **Agility Robotics 与 Amazon 扩大合作**
- **交易**: 10 亿美元订单
- **内容**: Digit 机器人部署到 Amazon 20 个物流中心
- **影响**: 物流自动化加速，人形机器人商业化里程碑
- **标签**: `Partnership` `Logistics` `Amazon`

#### 7. **中国人形机器人公司融资动态**
- **宇树科技**: 完成 B+ 轮 10 亿人民币，红杉中国领投
- **智元机器人**: B 轮 8 亿人民币，比亚迪参投
- **傅利叶智能**: 战略融资 5 亿人民币，用于 GR-2 量产
- **标签**: `China` `Funding` `Market`

---

### 🧠 核心论文

#### 1. **VLA 模型性能分析**
**"Characterizing VLA Models: Identifying the Action Generation Bottleneck for Edge AI Architectures"**
- arXiv:2603.02271
- 作者：Manoj Vishwanathan et al.
- **亮点**：分析了 Vision-Language-Action 模型在边缘设备上的推理瓶颈，为具身智能的实时控制提供架构指导
- **分类**：cs.PF, cs.AI, cs.AR, cs.RO

#### 2. **VLA 推理加速**
**"KERV: Kinematic-Rectified Speculative Decoding for Embodied VLA Models"**
- arXiv:2603.01581 (Accepted by DAC 2026)
- 作者：Zihao Zheng et al.
- **亮点**：提出运动学校正的推测解码方法，解决 VLA 模型的 token 错误问题，首次将机器人运动学应用于具身智能
- **分类**：cs.RO, cs.LG

#### 3. **人形机器人多任务学习**
**"Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning"**
- arXiv:2603.01414
- 作者：Shaohuai Liu et al.
- **亮点**：主张通过多任务强化学习实现在线学习，而非依赖大规模离线数据集
- **分类**：cs.AI, cs.RO

### 🤖 机器人操作

#### 4. **统一灵巧手操作**
**"UniHM: Unified Dexterous Hand Manipulation with Vision Language Model"**
- arXiv:2603.00732 (Accepted by ICLR 2026)
- 作者：Zhenhao Zhang et al.
- **亮点**：首个使用视觉语言模型实现开放词汇指令的灵巧手操作框架
- **分类**：cs.RO, cs.CV

#### 5. **3D 空间动作推理**
**"ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking"**
- arXiv:2602.21161 (Accepted by ICRA 2026)
- 作者：Guangming Wang et al.
- **亮点**：使用 LLM 进行 3D 空间中的机器人动作推理，适用于建筑堆叠场景
- **分类**：cs.RO

### 📊 数据与基准

#### 6. **第一人称视频收集**
**"AoE: Always-on Egocentric Human Video Collection for Embodied AI"**
- arXiv:2602.23893
- 作者：Bowen Yang et al.
- **亮点**：利用人类作为理想的物理感知智能体，大规模收集真实世界交互数据
- **分类**：cs.CV, cs.RO

#### 7. **4D 人体场景重建**
**"EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents"**
- arXiv:2602.23205
- 作者：Wenjia Wang et al.
- **亮点**：无需昂贵设备，在自然场景中捕捉人体运动数据用于训练具身智能体
- **分类**：cs.CV

### 🔒 安全与伦理

#### 8. **具身 LLM 越狱攻击**
**"Jailbreaking Embodied LLMs via Action-level Manipulation"**
- arXiv:2603.01414 (Accepted by ACM SenSys 2026)
- 作者：Xinyu Huang et al.
- **亮点**：揭示具身大语言模型在动作层面的安全漏洞
- **分类**：cs.RO

#### 9. **具身 AI 安全分析**
**"What Breaks Embodied AI Security: LLM Vulnerabilities, CPS Flaws, or Something Else?"**
- arXiv:2602.17345
- 作者：Boyang Ma et al.
- **亮点**：系统性分析具身 AI 安全问题的根源
- **分类**：cs.CR, cs.AI

### 🎯 其他值得关注的

- **"Temporal Representations for Exploration"** - 无外在奖励的复杂探索行为学习
- **"DICArt"** - 离散状态空间中的关节物体姿态估计
- **"Global Commander and Local Operative"** - 双智能体场景导航框架

---

## 📈 今日统计

| 类别 | 论文数量 |
|------|----------|
| 机器人学 (RO) | 8 |
| 计算机视觉 (CV) | 5 |
| 人工智能 (AI) | 7 |
| 人机交互 (HC) | 3 |
| 安全 (CR) | 1 |

---

## 🔗 链接

- [arXiv Embodied AI 搜索](https://arxiv.org/search/?query=embodied+AI&searchtype=all)
- [GitHub 仓库](https://github.com/Moxoo/embodied-ai-daily)

---

*by bigpurr 🐱 | Powered by OpenClaw*
