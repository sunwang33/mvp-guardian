# MVP Guardian（MVP 守门员）

> **先完成 MVP，再完美。先跑 MVP，别想一步到位。**

一个用于 vibe coding 的 AI Agent Skill：在你和 AI 结对开发时，**辅助并监督你遵循 MVP 思路**——适用于从零做新产品，也适用于给已有产品加拓展功能。

---

## 它解决什么问题

vibe coding 最大的风险不是「写不出来」，而是**写多了**：

- AI 会在你还没想清楚核心闭环时就开始写代码
- 写着写着冒出「顺便做个登录」「顺便上数据库」「顺便打磨下 UI」
- 报错后不回退，在错误代码上继续叠加修改，错上加错
- 第一版就追求一步到位，结果核心闭环永远跑不通

这个 skill 把「MVP 思路」从一句口号变成**可执行的流程约束**：在关键节点设门禁，没过不许往下走，并对偏离信号当场叫停。

## 核心机制：阶段门禁链

```mermaid
flowchart TD
    A["三问<br/>最核心一件事 / 最少功能 / 痛点推迟"] --> B["mvp-plan.md 落盘确认<br/>核心闭环 + 砍掉清单 + 完成标准"]
    B --> C["PRD 确认<br/>必含技术架构三件套"]
    C --> D["UI 结构确认<br/>5 项精简清单"]
    D --> E["写码前检查清单<br/>6 项自报"]
    E --> F["开发中监督<br/>偏离信号当场叫停"]
    F --> G["验收<br/>完成标准逐条核对"]
```

**任何一道门禁未通过，禁止创建或修改生产代码。** 门禁未过时只允许修改文档稿（mvp-plan.md、PRD）和标注过的 UI 原型稿。

| 阶段 | 门禁 | 关键动作 |
|------|------|---------|
| 一 · 想清楚 | 三问没过不写代码 | 最核心的一件事（必须一句话）→ 最少功能清单（每项经得起「第一版真的需要吗」）→ 痛点推迟清单 |
| 二 · 划边界 | 用户确认范围 | 落盘 `mvp-plan.md`：核心闭环、最少功能、**砍掉清单**、扩展候选池、完成标准、技术约定 |
| 三 · PRD | **默认必经**，非可选 | 功能范围锁死在 mvp-plan 内；必含技术架构（数据流 / 选型理由 / 职责边界）；提醒用户自己先审一遍 |
| 四 · UI 结构 | 有界面的产品必经 | 只要求 5 项：页面清单、核心流程、四种状态、布局方向、按钮文案。**不做视觉打磨 ≠ 不做结构设计** |
| 五 · 开发 | 写码前 6 项自报 | 每次写代码前先输出核对结果，让抢跑在发生前可见；4 类偏离信号（越界加功能 / 过度设计 / 跳阶段 / 一步到位）当场叫停 |
| 六 · 验收 | 标准没过不算完成 | 对照完成标准逐条给「通过 + 证据」，含糊不得 |

**阶段状态机**记录在 `mvp-plan.md` 的「状态」字段，跨会话可追溯：

```
计划中 → PRD 审查中 → UI 审查中 → 开发中 → 已验收
                              ↘ 已暂停（任意阶段可进入）
```

## 下载与安装

### 方式一：下载现成安装包（推荐给不熟悉命令行的用户）

到 [**Releases 页面**](https://github.com/sunwang33/mvp-guardian/releases/latest)，按你用的工具下载对应压缩包：

| 安装包 | 适用工具 | 装到哪里 |
|--------|---------|---------|
| `mvp-guardian.zip` | WorkBuddy | 解压出的 `mvp-guardian` 整个文件夹 → `~/.workbuddy/skills/` |
| `mvp-guardian-codex-share.zip` | Codex | 里面的 `mvp-guardian/` 文件夹 → `~/.codex/skills/`；`prompts-mvp.md` 重命名为 `mvp.md` → `~/.codex/prompts/` |

> Windows 上 `~` 就是 `C:\Users\你的用户名`。`~/.workbuddy/skills/` 即 `C:\Users\你的用户名\.workbuddy\skills\`。

### 方式二：网页下载源码（不需要命令行）

打开 [仓库首页](https://github.com/sunwang33/mvp-guardian) → 绿色 **Code** 按钮 → **Download ZIP**，解压后按下面的对应关系取文件。

### 方式三：git clone（开发者推荐）

直接克隆到技能目录，之后 `git pull` 就能更新，不用重复下载：

```bash
# macOS / Linux / Git Bash
git clone https://github.com/sunwang33/mvp-guardian.git ~/.workbuddy/skills/mvp-guardian
```

```powershell
# Windows PowerShell
git clone https://github.com/sunwang33/mvp-guardian.git "$env:USERPROFILE\.workbuddy\skills\mvp-guardian"
```

克隆到别处也可以，装的时候把对应文件夹拷进技能目录即可（见下表）。以后更新只需在该仓库目录执行 `git pull`。

> 本仓库根目录本身就是 WorkBuddy 技能目录结构（`SKILL.md` 在根），所以可以直接克隆到 `skills/` 下使用。

### 装哪几个文件？

仓库里同时放了两个平台的适配版，按你用的工具取：

| 你用的工具 | 需要的内容 | 目标位置 |
|-----------|-----------|---------|
| **WorkBuddy** | 仓库根目录的 `SKILL.md` + `references/` | `~/.workbuddy/skills/mvp-guardian/` |
| **Codex** | `codex/SKILL.md` + `references/` + `codex/agents/`；以及 `codex/prompts/mvp.md` | `~/.codex/skills/mvp-guardian/` 和 `~/.codex/prompts/mvp.md` |

小提示：WorkBuddy 只要文件夹里有 `SKILL.md` 就能识别，把仓库根目录整个文件夹拷进 `~/.workbuddy/skills/` 也可以，多出来的 README、`codex/` 等不影响运行。

Codex 的详细步骤（含 Windows PowerShell 写法）见 [`codex/安装说明.md`](codex/安装说明.md)。

### 一键部署（本仓库贡献者用）

```bash
bash scripts/deploy.sh          # 从本仓库部署到本机 WorkBuddy + Codex
bash scripts/deploy.sh --dry    # 只看会做什么，不实际写入
```

## 使用

**触发方式**（双通道）：

1. **自动**：对话中出现开发意图（「我要做一个 XX 网站」「给 XX 加一个功能」），守门员会先问一句是否启用，确认后进入流程
2. **手动**：说「mvp」「启动mvp」「mvp检查」「新功能」「开始开发」；Codex 里可直接敲 `/mvp`

**需求模糊时**：三问答不清核心那一件事，自动进入 grill 式追问模式——一次只问一个问题、每轮复述确认、5 轮上限，收敛出一句话核心闭环后回到三问。

**产出物**：项目根目录的 `mvp-plan.md`。它是你和 AI 之间的合同，监督和验收都对照它。

## 项目结构

```
.
├── SKILL.md                     # 技能本体（WorkBuddy 版，根目录直接可装）
├── references/
│   └── mvp-principles.md        # 实践原则详版（附出处与修订记录）
├── codex/                       # Codex 适配
│   ├── SKILL.md                 # frontmatter 按 Codex 规范
│   ├── prompts/mvp.md           # /mvp 命令
│   ├── AGENTS.md                # 项目级强制注入（可选）
│   ├── agents/openai.yaml       # 界面显示元数据
│   └── 安装说明.md
└── scripts/deploy.sh            # 一键部署到本机
```

## 设计哲学与诚实边界

**为什么是「门禁」而不是「提醒」**：软提醒在真实会话里会被忽略——实测中 AI 会绕过模糊表述直接写代码。所以本 skill 的选择是：门禁条款写具体、写码前强制自报核对结果。它的作用不是物理阻止抢跑，而是**让抢跑可见**。

**诚实边界**：本 skill 是提示词级约束，不存在运行时强制。**最后一道门禁永远是使用者自己的确认动作**——任何「AI 说过了门禁」都不等于「你确认过了」。

**与其他技能协同**：UI 结构阶段若环境中有 `design-taste-frontend` 或 `frontend-design` 等设计类技能，会自动调用以避免页面模板化；没有也不影响，内置 5 项清单兜底。本 skill 自包含，不依赖任何其他技能。

## 版本历史

见 [CHANGELOG.md](CHANGELOG.md)。当前 **v2.0**。

v2 的修订来自一次真实实测评估：初版在 Codex 实测中被判定为「6/10，是 MVP 提醒器而非守门员」——代理在 PRD 未确认时直接开始写页面。据此补齐了阶段门禁链、状态机、UI 门禁、写码前检查清单和报错安全回退。

## 贡献与反馈

欢迎提 issue 和 PR。特别欢迎这类反馈：

- **AI 没有遵守某条规则**——请附上具体现象（当时说了什么、AI 做了什么），用于加强对应措辞
- **门禁太严或太松**——比如某道门禁在你的场景里纯属浪费
- **新的偏离信号**——你踩过但清单里没写的坑

## 致谢

- 内容源自作者在 AI 编程实战营的亲身实践笔记，非理论推演
- 设计阶段协同参考了 [taste-skill](https://github.com/Leonxlnx/taste-skill) 的反模板化思路

## License

[MIT](LICENSE) © 2026 孙旺 (sunwang33)
