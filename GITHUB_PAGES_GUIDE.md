# GitHub Pages 部署指南

将 AI 喜讯汇部署到 GitHub Pages，获得免费、稳定的公网访问地址。

## 快速步骤（5 分钟）

### 1. 在 GitHub 创建仓库

- 访问 https://github.com/new
- 仓库名称填写：`ai-news-hub`
- 选择 **Public**（公开仓库才能免费使用 GitHub Pages）
- 不要勾选 "Add a README file"（我们已经有 README 了）
- 点击 **Create repository**

### 2. 推送代码

在项目目录下运行以下命令（将 `YOUR_USERNAME` 替换为你的 GitHub 用户名）：

```bash
cd /workspace/projects/workspace/tools/ai-news-hub

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/ai-news-hub.git

# 推送代码
git branch -M main
git push -u origin main
```

如果你配置了 GitHub SSH 密钥，也可以用：
```bash
git remote add origin git@github.com:YOUR_USERNAME/ai-news-hub.git
```

### 3. 启用 GitHub Pages

- 打开仓库页面：`https://github.com/YOUR_USERNAME/ai-news-hub`
- 点击 **Settings**（顶部标签栏）
- 左侧菜单选择 **Pages**
- **Source** 选择 **Deploy from a branch**
- **Branch** 选择 **main**，文件夹选 **/(root)**
- 点击 **Save**

### 4. 访问网站

等待约 1-2 分钟，访问：

```
https://YOUR_USERNAME.github.io/ai-news-hub/
```

## 自动更新数据（可选）

如果你想让网站自动采集最新 AI 资讯，可以配置 GitHub Actions：

1. 在仓库页面点击 **Actions** -> **New workflow** -> **set up a workflow yourself**
2. 粘贴 `.github/workflows/update-data.yml` 的内容（见下方）
3. 提交后，每天 UTC 00:00 会自动运行采集脚本并更新 data.json

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 前端主页面，GitHub Pages 会自动托管 |
| `data.json` | 演示数据，前端加载并渲染 Top 50 |
| `scraper.py` | 采集脚本，本地运行可更新 data.json |
| `README.md` | 项目说明 |
| `.gitignore` | 忽略不需要提交的文件 |

## 注意事项

- GitHub Pages 免费版有流量限制（每月 100GB），对于个人项目完全够用
- 首次部署可能需要 1-2 分钟生效
- 如果后续修改了代码，推送到 main 分支后会自动重新部署
- 如需绑定自定义域名，可在 Settings -> Pages -> Custom domain 中配置
