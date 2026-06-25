#!/bin/bash
# AI 喜讯汇公网部署脚本
# 使用 tunnelmole 创建临时公网访问（中国大陆可访问）

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
HTTP_PORT=8080

print_success() {
    echo ""
    echo "========================================"
    echo "  AI 喜讯汇 - 公网部署成功"
    echo "========================================"
    echo ""
    echo "  访问地址: $1"
    echo ""
    echo "  注意:"
    echo "  - 这是临时公网链接，重启后会变化"
    echo "  - 如需固定域名，建议使用 ngrok（需注册）"
    echo "  - 或部署到 GitHub Pages / Vercel"
    echo ""
}

echo "========================================"
echo "  AI 喜讯汇 - 公网部署"
echo "========================================"

# 1. 检查本地 HTTP 服务
echo "[步骤] 检查本地 HTTP 服务 (端口 $HTTP_PORT)..."
if ! curl -s http://localhost:$HTTP_PORT/ > /dev/null; then
    echo "[步骤] 启动本地 HTTP 服务..."
    cd "$PROJECT_DIR"
    nohup python3 -m http.server $HTTP_PORT > /tmp/http-server.log 2>&1 &
    sleep 2
fi

if curl -s http://localhost:$HTTP_PORT/ > /dev/null; then
    echo "[完成] 本地 HTTP 服务运行正常"
else
    echo "[错误] 本地 HTTP 服务启动失败"
    exit 1
fi

# 2. 检查是否已有 tunnelmole 在运行
echo "[步骤] 检查公网隧道..."
if pgrep -f "tunnelmole" > /dev/null; then
    echo "[完成] 公网隧道已在运行"
    # 尝试从日志中提取 URL
    if [ -f "$PROJECT_DIR/tunnel.log" ]; then
        URL=$(grep -oE 'https://[a-z0-9-]+\.tunnelmole\.net' "$PROJECT_DIR/tunnel.log" | tail -1)
        if [ -n "$URL" ]; then
            print_success "$URL"
            exit 0
        fi
    fi
fi

# 3. 启动 tunnelmole
echo "[步骤] 启动公网隧道 (tunnelmole)..."
pkill -f "tunnelmole" 2>/dev/null
sleep 1

cd "$PROJECT_DIR"
nohup script -q -c "npx --yes tunnelmole $HTTP_PORT" /dev/null > tunnel.log 2>&1 &

sleep 8
URL=$(grep -oE 'https://[a-z0-9-]+\.tunnelmole\.net' "$PROJECT_DIR/tunnel.log" | tail -1)

if [ -n "$URL" ]; then
    print_success "$URL"
else
    echo "[错误] 公网隧道启动失败"
    echo "[日志] ---"
    cat "$PROJECT_DIR/tunnel.log" 2>/dev/null | tail -20
    echo "[日志] ---"
    exit 1
fi
