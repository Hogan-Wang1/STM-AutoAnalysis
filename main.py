import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
import os
from itertools import cycle
from src.loaders import load_stm_dat
from src.config import PLOT_CONFIG, WATERFALL_CONFIG
from src.processor import process_spectral_data

selected_files = []
file_labels = {}

def apply_style():
    plt.rcParams.update({
        "font.family": PLOT_CONFIG.get("font_family", "Arial"),
        "font.size": PLOT_CONFIG.get("font_size", 10),
        "axes.linewidth": 1.2,
        "xtick.direction": "in", "ytick.direction": "in",
        "xtick.top": True, "ytick.right": True,
        "figure.dpi": 300
    })

def add_files():
    global selected_files
    paths = filedialog.askopenfilenames(title="选择数据文件", initialdir="./data")
    for p in paths:
        if p not in selected_files:
            selected_files.append(p)
            file_labels[p] = os.path.splitext(os.path.basename(p))[0]
    refresh_listbox()

def refresh_listbox():
    listbox.delete(0, tk.END)
    for p in selected_files:
        listbox.insert(tk.END, f"📊 {file_labels[p]}")

def plot_waterfall():
    global selected_files
    if not selected_files:
        messagebox.showwarning("提示", "请先添加数据文件")
        return
        
    apply_style()
    # 设定一个宽大比例的画布，防止挤压
    fig, ax = plt.subplots(figsize=(8, 10))
    
    color_pool = cycle(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'])
    last_x_unit = "V"
    offset_step = WATERFALL_CONFIG.get("offset_step", 2.0)

    for i, path in enumerate(selected_files):
        # 兼容性读取：处理可能返回的元组格式
        result = load_stm_dat(path)
        df = result[0] if isinstance(result, tuple) else result
        if df is None: continue
        
        # 调用处理器获取原始数据缩放后的结果
        x, y, x_unit = process_spectral_data(df, i, offset_step)
        last_x_unit = x_unit
        
        # 绘制原始数据：加粗线宽至 1.5 确保清晰
        ax.plot(x, y, color=next(color_pool), linewidth=1.5, label=file_labels[path])

    # 设置坐标轴标签
    ax.set_xlabel(f'Bias Voltage ({last_x_unit})', fontsize=12, fontweight='bold')
    ax.set_ylabel('dI/dV (Normalized & Offset)', fontsize=12, fontweight='bold')
    
    # 自动调整 X 轴范围
    ax.set_xlim(x.min(), x.max())
    
    # 智能设置 Y 轴范围：底部预留一点，顶部根据文件数动态增加
    ax.set_ylim(-0.5, (len(selected_files)) * offset_step + 1.0)
    
    # 移除 Y 轴刻度数字（因为瀑布图的绝对数值已无意义）
    ax.set_yticks([])

    # 图例放在右侧外部
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), frameon=False, fontsize=9)

    # 关键布局调整：rect=[左, 下, 右, 上]，给右侧留出 20% 空间放图例
    plt.tight_layout(rect=[0, 0, 0.8, 1])
    
    # 导出并显示
    os.makedirs("figures", exist_ok=True)
    plt.savefig("figures/Raw_Waterfall.pdf", bbox_inches='tight')
    plt.show()

# --- GUI 界面 ---
root = tk.Tk()
root.title("STS 原始数据自动化分析仪")
root.geometry("500x500")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="导入数据", command=add_files, width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="清空", command=lambda: [selected_files.clear(), refresh_listbox()], width=12).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="生成瀑布图", command=plot_waterfall, width=15, bg="#9D0A12", fg="white").grid(row=0, column=2, padx=5)

listbox = tk.Listbox(root, width=60, height=20)
listbox.pack(padx=20, pady=10)

if __name__ == "__main__":
    root.mainloop()