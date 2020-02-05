import re


def trans(file_name: str, converted_file_name: str):
    left_tag_com = re.compile(r'&lt;')
    right_tag_com = re.compile(r'&gt;')
    tag_com = re.compile(r'<[\s\S]*?(\s)[\s\S]*?>')
    with open(file_name, 'r', encoding='utf-8') as f:
        with open(converted_file_name, 'w', encoding='utf-8') as f_convered:
            for line in f:
                normal_line = left_tag_com.sub(r'<', line)
                normal_line = right_tag_com.sub(r'>', normal_line)
                length = normal_line.__len__()
                flag = False
                final_arr = []
                for i in range(length):
                    if normal_line[i] == '<':
                        flag = True
                    elif normal_line[i] == '>':
                        flag = False
                    if not flag or normal_line[i] != ' ':
                        final_arr.append(normal_line[i])
                f_convered.write(''.join(final_arr))


if __name__ == '__main__':
    trans('data/en_true_token', 'data/tmp_file')
