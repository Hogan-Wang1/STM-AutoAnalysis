# STM-AutoAnalysis
A Python toolkit for automated STM data analysis (DAT formats).

这是一个专为扫描隧道谱 (STS) 数据设计的自动化分析与可视化工具。

🌟 核心功能

- 自动化瀑布图 (Waterfall Plot)**：支持多文件一键堆叠，自动处理 Y 轴偏移。
- 双层科学绘图 (Scientific Layering)**：
  - 底层 (Raw Data)：半透明显示原始实验数据，保持数据的真实性。
  - 顶层 (Guide to the Eye)：使用 Savitzky-Golay 滤波器生成的平滑曲线，清晰展现物理趋势（如相干峰和能隙特征）。
- 交互式标注：支持从文件名自动提取标注，并允许在 GUI 界面双击手动修改。
- 科研出版级输出：
  - 导出格式为 `.pdf` 矢量图。
  - 标签置于绘图区外侧，方便在 PowerPoint 或 Adobe Illustrator 中取消组合并进一步排版。
  - 符合 PRL/Nature 系列期刊的字体和刻度线规范。

🛠️ 安装与运行
-本项目基于 Python 3.10+，需要以下库：
 -pip install numpy matplotlib scipy pandas

 📂 项目结构
main.py: 主程序，包含 GUI 界面和绘图逻辑。
src/config.py: 集中管理所有的绘图参数（颜色、步长、字体、平滑系数）。
src/loaders.py: 数据读取模块，适配 Nanonis 导出的 .dat 文件。
data/: (已忽略) 用于存放原始实验数据。
figures/: 用于存放导出的矢量图。

🧪 物理参数说明 (UTe2 Case)
在 src/config.py 中，默认配置如下：
smooth_window: 11 (Savitzky-Golay 窗口长度)
offset_step: 2.0 (谱线纵向间距)
x_multiplier: 1000 (将 Bias Voltage V 转换为 mV)

⚖️ 学术诚信与数据处理说明
本工具在设计时充分考虑了实验数据的真实性要求。所有的平滑处理均作为“引导线”叠加在原始数据之上。在发表论文时，建议保留底层透明的原始数据点，以确保实验信噪比的透明度。
