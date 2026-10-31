import os
 
def batch_output_files(directory, batch_size_mb=500):
    batch_size_bytes = batch_size_mb * 1024 * 1024  # 转换为字节
    current_batch_size = 0
    current_batch = []
 
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_size = os.path.getsize(file_path)
 
            if current_batch_size + file_size <= batch_size_bytes:
                current_batch.append(f'"{file_path}"')
                current_batch_size += file_size
            else:
                # 输出当前批次的文件
                print("\ngit add ", end=' ')
                for file in current_batch:
                    print(file, end=' ')
                print()  # 换行
                print("git commit -m 'add files'")
                print("git push -u origin main")
                # 清空当前批次，准备下一批
                current_batch = [f'"{file_path}"']
                current_batch_size = file_size
 
    # 输出最后一批文件（如果有的话）
    if current_batch:
        print("\ngit add ", end=' ')
        for file in current_batch:
            print(file, end=' ')
        print()  # 换行
        print("git commit -m 'add files'")
        print("git push -u origin main")
 
# 使用示例
batch_output_files('.')  # 遍历当前文件夹及其子文件夹

