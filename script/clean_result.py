if __name__ == '__main__':
    with open('result.bak', 'r', encoding='utf-8') as f:
        with open('report', 'w', encoding='utf-8') as w:
            s = list(filter(None, f.read().split('\n')))
            j = 0
            cnt = 0
            while j < len(s):
                if cnt % 10 == 0:
                    w.write(
                        'lable/model/epoch   BLEU    准确率     召回率        F1\n\n'
                    )
                tmp_arr = s[j:j + 5]
                j += 5
                name = tmp_arr[0]
                typ_arr = name.rstrip('\n').split(' ')
                w.write(typ_arr[0] + '    ' + typ_arr[1] + '    ' + '%2s' %
                        (typ_arr[2]) + ':    ')
                arr = tmp_arr[1].rstrip('\n').split(',')[0].split('=')
                w.write(arr[1] + '\t')
                for i in range(2, 5):
                    l2 = tmp_arr[i].rstrip('\n ').lstrip(' ').split(
                        ': ')[1].lstrip(' ')
                    if l2 == 'NaN':
                        w.write('%7s' % (l2) + r'    ')
                    else:
                        w.write("%6.2f%%" % (float(l2) * 100) + '    ')
                w.write('\n')
                cnt += 1
