import pandas as pd
import os

def load_stm_dat(file_path):
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return None, {}

    metadata = {}
    try:
        header_count = 0
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if "[DATA]" in line:
                    header_count = i + 1  # 数据从 [DATA] 的下一行开始
                    break
                
                # 智能提取 Nanonis Header (格式通常是 Key \t Value)
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    metadata[key] = value
        
        if header_count == 0:
            print("错误：在文件中未找到 [DATA] 标签，请检查文件格式。")
            return None, {}

        # 读取核心数据
        df = pd.read_csv(file_path, sep='\t', skiprows=header_count)
        df = df.dropna(axis=1, how='all')
        
        return df, metadata

    except Exception as e:
        print(f"读取过程中发生错误: {e}")
        return None, {}