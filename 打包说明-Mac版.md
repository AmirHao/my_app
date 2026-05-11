# 账本管理系统 - Mac环境打包Windows程序说明

## 当前情况

您在Mac上开发，但需要生成Windows的exe文件。PyInstaller只能在目标平台上打包，即：
- 在Mac上打包 → 生成Mac应用（.app）
- 在Windows上打包 → 生成Windows程序（.exe）
- 在Linux上打包 → 生成Linux程序

## 推荐方案

### 方案1：使用GitHub Actions（最简单）

1. 将代码推送到GitHub仓库
2. GitHub Actions会自动在Windows环境中打包
3. 从Actions页面下载生成的exe文件

**步骤：**
```bash
# 初始化git仓库（如果还没有）
git init
git add .
git commit -m "Initial commit"

# 推送到GitHub
git remote add origin <你的GitHub仓库地址>
git push -u origin main
```

然后：
- 访问GitHub仓库的Actions标签页
- 点击最新的workflow运行
- 下载生成的exe文件

### 方案2：使用虚拟机或云服务

**选项A：使用免费的Windows虚拟机**
- 下载VirtualBox或Parallels Desktop
- 安装Windows 10/11（可以使用90天试用版）
- 在虚拟机中安装Python和PyInstaller
- 打包程序

**选项B：使用云服务**
- AWS EC2 Windows实例（有免费额度）
- Azure Windows虚拟机（有免费额度）
- 在云服务器上打包后下载

### 方案3：借用Windows电脑

如果有朋友或同事有Windows电脑：
1. 将代码复制到U盘或通过网盘分享
2. 在Windows电脑上安装Python
3. 运行打包命令
4. 将生成的exe文件拷贝回来

## Mac上的本地打包

如果您想在Mac上打包Mac版本的应用：

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包Mac应用
pyinstaller --onefile --windowed --name="账本管理系统" main.py

# 生成的应用在 dist/账本管理系统.app
```

## 使用Wine（不推荐）

Wine可以在Mac上运行Windows程序，理论上可以用来打包，但：
- 配置复杂
- 可能有兼容性问题
- 生成的exe可能无法在真实Windows上运行

**如果仍想尝试：**
```bash
# 安装Wine
brew install wine-stable

# 下载Windows版Python
# 使用Wine运行Python和PyInstaller
# （具体步骤复杂且不稳定，不建议使用）
```

## 测试程序功能

在Mac上，您可以直接运行Python程序来测试功能：

```bash
python main.py
```

所有功能都可以正常测试，只是界面样式可能与Windows略有不同。

## 建议的工作流程

1. **开发阶段**：在Mac上使用 `python main.py` 测试
2. **打包阶段**：使用GitHub Actions或虚拟机生成Windows exe
3. **测试阶段**：在Windows环境中测试exe文件

## 快速验证（推荐）

最简单的方法是使用GitHub Actions：

1. 创建GitHub仓库
2. 推送代码（已包含.github/workflows/build-windows.yml）
3. 等待几分钟自动打包完成
4. 下载exe文件

这样您无需安装任何额外软件，也不需要Windows环境！
