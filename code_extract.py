import os
import re

# -------- 配置你的目录和输出文件 --------
input_dir = '/Users/louisliu/dev/frontend_projects/gdweb/src'  # 修改成你的目录
output_file = 'code.txt'

# 支持的文件后缀
file_extensions = ['.vue']

# -------- 工具函数 --------
def remove_comments(code):
    """
    删除 JavaScript/Vue 文件中的注释，包括单行和多行注释
    """
    # 去除单行注释
    code = re.sub(r'//.*', '', code)
    # 去除多行注释
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

all_code = []

# 遍历文件夹
for root, dirs, files in os.walk(input_dir):
    # 过滤掉不需要的目录：node_modules 和 dist
    if root.find('largeModel') > 0:
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                        code_no_comments = remove_comments(code)
                        all_code.append(code_no_comments)
                except Exception as e:
                    print(f"读取 {file_path} 出错: {e}")

# 把所有清理过的代码写入到输出文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_code))

print(f"完成！所有代码已写入 {output_file}")
