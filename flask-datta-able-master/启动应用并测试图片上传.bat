@echo off
chcp 65001 >nul
echo ========================================
echo   商品图片上传功能 - 快速启动脚本
echo ========================================
echo.

:: 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

:: 进入项目目录
cd /d "%~dp0"

:: 检查虚拟环境
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 激活虚拟环境...
    call .venv\Scripts\activate.bat
) else (
    echo ℹ️  未找到虚拟环境，使用系统Python
)

:: 检查依赖
echo 📦 检查依赖...
python -c "import flask, requests" 2>nul
if errorlevel 1 (
    echo ⚠️  缺少依赖，正在安装...
    pip install flask requests
)

echo.
echo ========================================
echo   启动Flask应用
echo ========================================
echo.
echo 💡 提示：
echo    1. 应用启动后访问: http://127.0.0.1:5000
echo    2. 登录后台: http://127.0.0.1:5000/login
echo    3. 商品管理: http://127.0.0.1:5000/admin/sp/product
echo.
echo    测试账号: admin / admin123
echo.
echo 按 Ctrl+C 停止应用
echo ========================================
echo.

:: 启动Flask
python run.py
