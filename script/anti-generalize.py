r""" 利用json信息将标签反向复原
"""

import json, sys
record_file = None


def process(line: str, info: str):
    dict = json.loads(info)
    arr = line.split(' ')
    lenth = len(arr)
    for i in range(lenth):
        if arr[i] in dict.keys():
            if arr[i] == '$lable':
                arr[i] = dict['$lable'][0]
                del dict['$lable'][0]
            else:
                arr[i] = dict[arr[i]]
    return ' '.join(arr)


def anti_generalize(input_file: str, json_file: str):
    with open(input_file, 'r', encoding='utf-8') as i:
        with open(json_file, 'r', encoding='utf-8') as j:
            for raw, js in zip(i.readlines(), j.readlines()):
                print(process(raw.rstrip('\n'), js))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit(
            'ERROR! anti-generalize_file needs 2 parms\n such as "python anti-generalize_file.py input_file json_file " '
        )
    input_file = sys.argv[1]
    json_file = sys.argv[2]
    anti_generalize(input_file, json_file)
