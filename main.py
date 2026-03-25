import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
import numpy as np
import os
from itertools import cycle
from scipy.signal import savgol_filter # 必须安装 scipy: pip install scipy
from src.loaders import load_stm_dat
from src.config import PLOT_CONFIG, PHYSICS_CONFIG, WATERFALL_CONFIG

selected_files = []
file_labels = {}

def apply_style():
    plt.rcParams.update({
        "font.family": PLOT_CONFIG["font_family"],
        "font.size": PLOT_CONFIG["font_size"],
        "axes.linewidth": PLOT_CONFIG["axes_width"],
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": PLOT_CONFIG["tick_size"],
        "ytick.major.size": PLOT_CONFIG["tick_size"],
        "xtick.top": True,
        "ytick.right": True,
        "figure.dpi": PLOT_CONFIG["dpi"]
    })

def add_files():
    paths = filedialog.askopenfilenames(title="选择数据文件", initialdir="./data")
    for p in paths:
        if p not in selected_files:
            selected_files.append(p)
            file_labels[p] = os.path.splitext(os.path.basename(p))[0]
    refresh_listbox()

def refresh_listbox():
    listbox.delete(0, tk.END)
    for p in selected_files:
        listbox.insert(tk.END, f"🏷️ {file_labels[p]}  ({os.path.basename(p)})")

def on_item_double_click(event):
    selection = listbox.curselection()
    if not selection: return
    idx = selection[0]
    file_path = selected_files[idx]
    new_label = simpledialog.askstring("修改标注", "输入显示名称:", initialvalue=file_labels[file_path])
    if new_label is not None:
        file_labels[file_path] = new_label
        refresh_listbox()

def plot_waterfall():
    if not selected_files:
        messagebox.showwarning("提示", "请选择文件")
        return
        
    apply_style()
    fig_w, fig_h = PLOT_CONFIG["fig_size_waterfall"]
    fig, ax = plt.subplots(figsize=(fig_w + 1.5, fig_h), constrained_layout=True)
    
    if WATERFALL_CONFIG["use_colormap"]:
        colors = plt.get_cmap(WATERFALL_CONFIG["colormap_name"])(np.linspace(0, 0.85, len(selected_files)))
    else:
        color_pool = cycle(WATERFALL_CONFIG["color_cycle"])

    line_handles = []

    for i, path in enumerate(selected_files):
        df = load_stm_dat(path)
        if df is None: continue
        
        x = df.iloc[:, 0] * PHYSICS_CONFIG["x_multiplier"]
        y_raw = df.iloc[:, -1] * PHYSICS_CONFIG["y_multiplier"]
        y_offset = i * WATERFALL_CONFIG["offset_step"]
        
        current_color = colors[i] if WATERFALL_CONFIG["use_colormap"] else next(color_pool)
        
        # --- 绘制原始数据（淡色底层）---
        ax.plot(x, y_raw + y_offset, 
                color=current_color, 
                alpha=WATERFALL_CONFIG["raw_alpha"], 
                linewidth=WATERFALL_CONFIG["raw_line_width"])
        
        # --- 绘制平滑曲线（深色顶层）---
        y_plot = y_raw + y_offset
        if WATERFALL_CONFIG["enable_smoothing"]:
            try:
                # 使用 Savitzky-Golay 滤波器
                y_smooth = savgol_filter(y_raw, 
                                        window_length=WATERFALL_CONFIG["smooth_window"], 
                                        polyorder=WATERFALL_CONFIG["smooth_polyorder"])
                y_plot = y_smooth + y_offset
            except Exception as e:
                print(f"平滑失败: {e}，将使用原始数据")

        line, = ax.plot(x, y_plot, 
                        color=current_color, 
                        linewidth=PLOT_CONFIG["line_width"],
                        label=file_labels[path])
        line_handles.append(line)

    ax.set_xlabel(PHYSICS_CONFIG["x_label"])
    ax.set_ylabel(PHYSICS_CONFIG["y_label"])
    ax.get_yaxis().set_ticks([])
    ax.set_xlim(x.min(), x.max())
    
    if WATERFALL_CONFIG["show_label"]:
        ax.legend(handles=line_handles, loc='center left', bbox_to_anchor=(1.02, 0.5), frameon=False)

    plt.savefig("figures/Waterfall_Scientific.pdf")
    plt.show()

# --- GUI 保持不变 ---
root = tk.Tk()
root.title("UTe2 科学绘图终端 (原始数据+平滑对比)")
root.geometry("550x450")
root.attributes('-topmost', True)

ctrl_frame = tk.Frame(root); ctrl_frame.pack(pady=15)
tk.Button(ctrl_frame, text="添加数据", command=add_files, width=10).grid(row=0, column=0, padx=5)
tk.Button(ctrl_frame, text="清空", command=lambda: [selected_files.clear(), file_labels.clear(), listbox.delete(0, tk.END)], width=10).grid(row=0, column=1, padx=5)
tk.Button(ctrl_frame, text="生成瀑布图", command=plot_waterfall, width=15, bg="#9D0A12", fg="white").grid(row=0, column=2, padx=5)

listbox = tk.Listbox(root, width=65, height=15); listbox.pack(padx=20, pady=10)
listbox.bind('<Double-1>', on_item_double_click)

if __name__ == "__main__":
    root.mainloop()