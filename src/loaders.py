import pandas as pd
import os

def load_stm_dat(file_path):
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return None

    try:
        # 第一步：先扫描文件，找到 [DATA] 标签所在的行号
        header_count = 0
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if "[DATA]" in line:
                    header_count = i + 1  # 数据从 [DATA] 的下一行开始
                    break
        
        if header_count == 0:
            print("错误：在文件中未找到 [DATA] 标签，请检查文件格式。")
            return None

        # 第二步：使用找到的行号来跳过文件头
        # 细节：Nanonis 的数据列通常以 Tab (\t) 分隔
        df = pd.read_csv(file_path, sep='\t', skiprows=header_count)
        
        # 清洗：去除全空的列
        df = df.dropna(axis=1, how='all')
        
        print(f"成功加载数据！跳过了 {header_count} 行文件头。")
        print(f"检测到的列名为: {list(df.columns)}")
        return df

    except Exception as e:
        print(f"读取过程中发生错误: {e}")
        return None