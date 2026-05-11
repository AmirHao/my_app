# 在Mac上打包Mac应用

## 打包Mac版本

如果您想在Mac上使用，可以打包成Mac应用：

### 1. 安装PyInstaller

```bash
pip3 install pyinstaller
```

### 2. 打包程序

```bash
pyinstaller --onefile --windowed --name="账本管理系统" main.py
```

### 3. 查找生成的应用

打包完成后，应用位于：
```
dist/账本管理系统.app
```

### 4. 运行应用

双击 `账本管理系统.app` 即可运行。

### 5. 移动到应用程序文件夹（可选）

```bash
mv dist/账本管理系统.app /Applications/
```

## 注意事项

1. Mac版本只能在Mac上运行
2. 如果遇到"无法打开，因为它来自身份不明的开发者"：
   - 右键点击应用
   - 选择"打开"
   - 点击"打开"确认

3. 或者在系统偏好设置中允许：
   ```bash
   sudo spctl --master-disable
   ```
   使用后记得重新启用：
   ```bash
   sudo spctl --master-enable
   ```

## 直接运行Python脚本（推荐开发时使用）

```bash
python3 main.py
```

这样可以直接测试功能，无需每次都打包。
