# 科普类短视频制作系统 - 使用文档

## 项目简介

本项目为GLCC项目，是一个AI驱动的科普类短视频制作系统，旨在自动生成高质量的科普教学内容，支持数学动画、科学插画、教学演示等多种科普内容形式。

## 核心特性

### 主要功能
- **AI 驱动的动画生成**：使用大语言模型自动生成 Manim 动画代码
- **科普插画制作**：智能生成科学图表、示意图和教学插画
- **多模态制作模式**：支持自动化、人工控制等两种模式
- **智能质量控制**：内置多层质量检测和优化系统
- **音频集成**：支持 TTS 语音合成和音频同步
- **背景图生成**：智能背景图片生成和管理
- **空间约束系统**：防止元素重叠和越界的智能布局

### 技术特色
- **增强提示词系统**：优化的 AI 提示词模板，专门针对科普内容优化
- **代码质量检测**：自动检测和修复常见代码问题
- **视觉质量评估**：智能评估动画效果和布局合理性
- **任务管理系统**：支持复杂动画项目的分解和管理

## 系统架构

```
科普类短视频制作系统
├── 核心工作流 (workflow.py)
├── 人工动画工作室 (human_animation_studio.py) - 包含交互式功能
├── 质量控制系统
│   ├── 增强质量系统 (enhanced_quality_system.py)
│   ├── Manim质量控制器 (manim_quality_controller.py)
│   └── 优化提示词系统 (optimized_manim_prompts.py)
├── 增强功能模块
│   ├── 背景图生成器 (background_image.py)
│   ├── 平衡空间系统 (balanced_spatial_system.py)
│   ├── 动画制作模式 (animation_production_modes.py)
│   └── 增强提示词 (enhanced_manim_prompts.py)
└── 资源文件夹 (asset/)
    ├── 音频文件
    └── 字体文件
```

## 安装配置

### 环境要求
- Python 3.8+
- Windows/Linux/macOS
- FFmpeg（用于视频渲染）

### 安装步骤

1. **克隆项目**
```bash
git clone [项目地址]
cd [项目目录]
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
# 设置模型API密钥（可选，有默认值）
$env:MODELSCOPE_API_KEY = "你的token"
```

4. **验证安装**
```python
python -c "import manim; print(manim.__version__)"
```

## 快速开始

### 自动模式

```python
python workflow.py "视频主题" 目录地址 auto
```

### 人工模式

```python
python workflow.py "视频主题" 目录地址 human
python human_animation_studio.py "视频目录地址"    #启动人工动画工作室模式
```

