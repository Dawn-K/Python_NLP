r"""中文分词,方便预处理脚本调用
"""

import pynlpir, os, sys
import jieba


def process(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as file:  #  read cn
        for word in file:
            word = word.rstrip('\n')
            final_str = ' '.join(jieba.cut(word))
            print(final_str)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(
            'ERROR! cn_tokenizer needs one parm\n such as "python cn_tokenizer.py cn_file " '
        )
    process(sys.argv[1])
