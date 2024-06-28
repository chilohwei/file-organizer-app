# FileOrganizerApp
File Organizer App 是一个用于整理文件的工具，能够根据文件类型、日期等条件自动将文件分类整理。

![File Organizer Preview](https://github.com/chilohwei/File_Organizer/assets/51521054/8b356be4-2040-4241-933f-84100060651e)


## 功能

- 根据文件类型分类整理
- 根据文件日期分类整理
- 自定义分类规则
- 支持多种文件格式

## 安装

### 克隆仓库

首先，克隆此仓库到本地：

```bash
git clone https://github.com/yourusername/file_organizer.git 
cd file_organizer
```

### 安装依赖

确保你已经安装了 Python 3.6 及以上版本，并安装所需的依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

运行以下命令启动文件整理器：

```bash
python file_organizer.py
```

你可以通过修改配置文件来自定义整理规则和目标目录。

## 打包应用

你可以使用 PyInstaller 将该项目打包为一个独立的应用程序。以下是打包步骤：

### 打包

```bash
pyinstaller file_organizer.spec
```

打包完成后，你可以在 `dist` 目录下找到生成的应用程序。PS：如果需要更改logo，请在打包前，用自己的`logo.icns`替换项目代码中的同名文件。

## 贡献

如果你有任何改进建议或发现了 bug，欢迎提交 issue 或 pull request。

## 许可证

此项目基于 [MIT 许可证](LICENSE)。

## 联系

如有任何问题，请联系 [chilohwei@gmail.com](mailto:chilohwei@gmail.com)。
