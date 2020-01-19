import re
cnt = 100

# cn = open('cn', 'w', encoding='utf-8')
# en = open('en', 'w', encoding='utf-8')
small = open('raw_small', 'w', encoding='utf-8')
# `re.sub(pattern, repl, string, count=0, flags=0)`
remove_tail = r'\twmt2018[\s\S]+$'
sum_len = 0
with open('wmt2018.zh2en-Registry', 'r', encoding='utf-8') as file:
    for word in file:
        if cnt == 0:
            break
        cnt = cnt - 1
        new_word = re.sub(remove_tail,'',word)
        small.writelines(new_word+'\n')
small.close()