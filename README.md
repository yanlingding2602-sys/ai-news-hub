# AI 喜讯汇 | Top 50 Intelligence Hub

一个自动聚合全网 AI 领域热讯的前端系统，支持实时采集、热度排序、分类筛选，搭配高级质感深色 UI。

## 功能特性

- **Top 50 排行榜**：多源聚合，按热度分排序
- **分类筛选**：模型 / 产品 / 研究 / 投资 / 政策
- **实时搜索**：标题关键词即时过滤
- **高级 UI**：深色主题 + 玻璃拟态 + 霓虹渐变 + 悬停动效
- **自动采集**：Python 脚本采集 HackerNews / Reddit / GitHub
- **响应式布局**：适配桌面端与移动端

## 项目结构

```
ai-news-hub/
├── index.html      # 前端主页面（纯 HTML/CSS/JS，零依赖）
├── scraper.py      # Python 采集脚本（异步多源采集）
├── data.json       # 演示数据 / 采集输出文件
└── README.md       # 项目说明
```

## 快速启动

### 方式一：直接打开（使用演示数据）

用浏览器直接打开 `index.html` 即可查看效果，无需任何服务器。

### 方式二：启动本地服务（推荐）

```bash
cd ai-news-hub

# Python
python -m http.server 8080

# 或 Node.js
npx serve .

# 或 VS Code Live Server
```

访问 `http://localhost:8080`

### 方式三：采集真实数据

```bash
# 安装依赖（仅需 aiohttp）
pip install aiohttp

# 运行采集脚本
python scraper.py

# 采集完成后刷新页面即可看到真实数据
```

## 采集脚本说明

`scraper.py` 支持以下数据源：

| 数据源 | API 类型 | 是否需要 Key |
|--------|---------|-------------|
| HackerNews | 官方公开 API | 否 |
| Reddit | 公开 RSS/JSON | 否 |
| GitHub | Search API | 否（有速率限制） |

### 自定义扩展

在 `scraper.py` 中：

1. **修改关键词**：编辑 `AI_KEYWORDS` 列表
2. **新增数据源**：仿照 `fetch_xxx()` 函数添加新的采集逻辑
3. **调整热度算法**：修改 `score` 计算公式
4. **定时更新**：结合 `cron` 或 `systemd timer` 定时执行

```bash
# 每 30 分钟自动更新（Linux/macOS）
*/30 * * * * cd /path/to/ai-news-hub && python scraper.py
```

## 技术栈

- **前端**：原生 HTML5 + CSS3 + Vanilla JS（零框架依赖）
- **样式**：CSS 变量 + Flexbox + 玻璃拟态（backdrop-filter）
- **字体**：Inter + Noto Sans SC（Google Fonts CDN）
- **采集**：Python 3.8+ + asyncio + aiohttp

## UI 设计亮点

- 动态呼吸背景光效（CSS 动画）
- 前三名金银铜徽章渐变
- 热度分渐变文字
- 卡片悬浮抬升 + 微光扫过
- 实时脉冲更新指示器
- 平滑的筛选切换过渡

## License

MIT
