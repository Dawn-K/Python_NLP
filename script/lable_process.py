import sys, re

# 0 不处理
# 1 在两端加$copy
# 2 完全泛化
ltag_com = re.compile(r'<')
rtag_com = re.compile(r'>')


def add_copy(line: str):
    newline = ''
    newline = ltag_com.sub(r' $copy<', line)
    newline = rtag_com.sub(r'>$copy ', newline)
    return newline


def generalized(language: str):
    #todo: path
    with open('../creat_data/data/out_generalization.' + language,
              'r',
              encoding='utf-8') as f:
        for l in f.readlines():
            print(l)


def pro_line(line: str, model: int, language: str):
    if model == '0':
        return line
    elif model == '1':
        return add_copy(line)
    else:
        print("pro_line err!!!")


def lable_process(model: str, file_name: str, language: str):
    assert (model in ['0', '1', '2'])
    if model != '2':
        with open(file_name, 'r', encoding='utf-8') as f:
            for l in f.readlines():
                print(pro_line(l, model, language),end='')
    else:
        generalized(language)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(
            'ERROR! lable_process needs 3 parms\n such as "python lable_process.py model file language " '
        )
    model = sys.argv[1]
    file_name = sys.argv[2]
    language = sys.argv[3]
    lable_process(model, file_name, language)
