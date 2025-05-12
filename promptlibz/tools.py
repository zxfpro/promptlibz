import re
import pandas as pd
import io


def extract_python_code(text: str)->str:
    """从文本中提取python代码

    Args:
        text (str): 输入的文本。

    Returns:
        str: 提取出的python文本
    """
    pattern = r'```python([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches[0].replace('\n','')

def extract_type_code(text: str)->str:
    """从文本中提取python代码

    Args:
        text (str): 输入的文本。

    Returns:
        str: 提取出的python文本
    """
    pattern = r'```type([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches[0].replace('\n','')


def dataframe_to_lm_string(df: pd.DataFrame, num_samples: int = 5, max_col_width: int = 50) -> str:
    """
    将 Pandas DataFrame 转换为一个对大模型友好的字符串表示。

    这个字符串包含数据描述、数据类型、前几行数据样本，
    旨在让大模型充分理解数据的结构和内容，以便执行后续操作。

    Args:
        df (pd.DataFrame): 需要转换的 Pandas DataFrame。
        num_samples (int): 要显示的数据样本行数。默认为 5。
        max_col_width (int): 显示数据样本时，每列的最大宽度，
                             超过部分将被截断并显示省略号。默认为 50。

    Returns:
        str: 包含数据描述和样本的字符串，适合作为大模型的输入。
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("输入必须是一个 Pandas DataFrame。")

    output_string = io.StringIO()

    # 1. 添加数据描述和总览
    output_string.write("# 数据集概览\n\n")
    output_string.write(f"这是一个包含 {len(df)} 行， {len(df.columns)} 列的数据集。\n")
    output_string.write("下面是关于数据集列的描述：\n\n")

    # 2. 添加列信息（列名、数据类型、非空数量）
    output_string.write("## 列信息\n\n")
    output_string.write("| 列名 | 数据类型 | 非空数量 |\n")
    output_string.write("|---|---|---|\n")
    for col in df.columns:
        dtype = df[col].dtype
        non_null_count = df[col].count()
        output_string.write(f"| {col} | {dtype} | {non_null_count} |\n")
    output_string.write("\n")

    # 3. 添加数据样本
    output_string.write(f"## 数据样本 (前 {num_samples} 行)\n\n")
    if len(df) > 0:
        # 使用 to_csv 转换为 CSV 格式字符串，方便模型解析
        # 同时处理列宽，避免过长影响可读性
        sample_df = df.head(num_samples).copy()
        for col in sample_df.columns:
            # 将非字符串类型转换为字符串，方便截断
            sample_df[col] = sample_df[col].astype(str).str.slice(0, max_col_width) + sample_df[col].astype(str).apply(lambda x: '...' if len(x) > max_col_width else '')

        sample_csv = sample_df.to_csv(index=False)
        output_string.write("```csv\n") # 使用CSV代码块，明确格式
        output_string.write(sample_csv)
        output_string.write("```\n")
    else:
        output_string.write("数据集为空，无法显示样本。\n")

    return output_string.getvalue()
