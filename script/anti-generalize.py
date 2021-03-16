r""" 利用json信息将标签反向复原
"""

import json, sys, re
record_file = None


def process_model2(line: str, info: str):
    dict = json.loads(info)
    arr = line.split(' ')
    lenth = len(arr)
    for i in range(lenth):
        if arr[i] in dict.keys():
            if arr[i] == '$lable':
                if len(dict['$lable']) > 0:
                    arr[i] = dict['$lable'][0]
                    del dict['$lable'][0]
                else:
                    arr[i] = ''
            else:
                arr[i] = dict[arr[i]]
        else:
            if re.match('\$lable_', arr[i]) is not None:
                arr[i] = ''
    return ' '.join(arr)


def anti_generalize(input_file: str, json_file: str, model: str):
    if model == "2" or model == "3":
        with open(input_file, 'r', encoding='utf-8') as i:
            with open(json_file, 'r', encoding='utf-8') as j:
                for raw, js in zip(i.readlines(), j.readlines()):
                    print(process_model2(raw.rstrip('\n'), js))
    elif model == "1":
        l_copy_tag = re.compile(r'\$copy<')
        r_copy_tag = re.compile(r'>\$copy')
        with open(input_file, 'r', encoding='utf-8') as i:
            for l in i.readlines():
                newlline = l_copy_tag.sub(r'<', l.rstrip('\n'))
                newlline = r_copy_tag.sub(r'>', newlline)
                print(newlline)
    else:
        with open(input_file, 'r', encoding='utf-8') as i:
            for l in i.readlines():
                print(l.rstrip('\n'))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(
            'ERROR! anti-generalize_file needs 3 parms\n such as "python anti-generalize_file.py input_file json_file model " '
        )
    input_file = sys.argv[1]
    json_file = sys.argv[2]
    model = sys.argv[3]
    anti_generalize(input_file, json_file, model)
