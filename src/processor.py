import numpy as np

def auto_unit_scale(data_array):
    """根据偏置电压量级自动选择 V 或 mV"""
    max_val = np.max(np.abs(data_array))
    # 如果最大值小于 0.5，说明原始单位是 V，我们转为 mV 显示
    if max_val < 0.5: 
        return 1000.0, "mV"
    return 1.0, "V"

def process_spectral_data(df, index, offset_step=2.0):
    """
    仅处理原始数据的缩放和平移，不包含任何平滑算法。
    """
    # 1. X 轴动态缩放
    raw_x = df.iloc[:, 0].values
    x_scale, x_unit = auto_unit_scale(raw_x)
    x = raw_x * x_scale
    
    # 2. Y 轴：鲁棒性归一化 (使用 98% 分位数，无视那 2% 的超大噪声尖峰)
    raw_y = df.iloc[:, -1].values
    y_scale_factor = np.percentile(np.abs(raw_y), 98)
    if y_scale_factor == 0: y_scale_factor = 1.0
    
    # 归一化后的数据，振幅约在 0 到 1 之间
    y_norm = raw_y / y_scale_factor
    
    # 3. 施加瀑布图平移
    y_offset = index * offset_step
    y_final = y_norm + y_offset
    
    return x, y_final, x_unit