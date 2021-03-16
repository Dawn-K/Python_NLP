r""" 将被修改的标签(如'&lt;  u  &gt;') 恢复原状
"""
import re, sys


def trans(lable_type: str, model_type: str, file_name: str):
    r"""
        lable_type          : 标签保留类型
        model_type          : 标签泛化类型
        file_name           : 待转换文件路径 
    """
    if lable_type == "no":  # 不保留就不需要操作了,也不用在乎是什么模型
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                print(line, end='')
        return
    remove_sig = [' ']
    if lable_type == "bpe":
        remove_sig.append('@')
    if model_type != "2" and model_type != "3":
        left_tag = None
        right_tag = None
        left_tag_to = None
        right_tag_to = None
        if model_type == "0":
            left_tag = r'&lt;'
            right_tag = r'&gt;'
            left_tag_to = r'<'
            right_tag_to = r'>'
        if model_type == "1":  # $copy
            left_tag = r'\$ copy &lt;'
            left_tag_to = r'$copy<'
            right_tag = r'&gt; \$ copy'
            right_tag_to = r'>$copy'
        left_tag_com = re.compile(left_tag)
        right_tag_com = re.compile(right_tag)
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                normal_line = left_tag_com.sub(left_tag_to, line)
                normal_line = right_tag_com.sub(right_tag_to, normal_line)
                length = normal_line.__len__()
                flag = False
                final_arr = []
                # 去除尖括号中的无用元素
                for i in range(length):
                    if normal_line[i] == '<':
                        flag = True
                    elif normal_line[i] == '>':
                        flag = False
                    if not flag or normal_line[i] not in remove_sig:
                        final_arr.append(normal_line[i])
                print(''.join(final_arr), end='')
    else:  #  $ lable _ l1  or  $ lable   or  $ lable _ l
        gen_tag = r'\$ lable'
        gen_tag_line = r'\$lable _ '
        gen_tag_com = re.compile(gen_tag)
        gen_tag_line_com = re.compile(gen_tag_line)
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                normal_line = gen_tag_com.sub(r'$lable', line)
                normal_line = gen_tag_line_com.sub(r'$lable_', normal_line)
                print(normal_line, end='')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(
            'ERROR! lable_process needs 1 parm\n such as "python restore_token.py lable_type model_type file  "\n'
            + 'lable type must be "no" or "tok" or "bpe" '  # 保留类型
            + 'model type must be 0 or 1 or 2'  # 泛化类型
        )
    lable_type = sys.argv[1]
    model_type = sys.argv[2]
    file_name = sys.argv[3]
    trans(lable_type, model_type, file_name)