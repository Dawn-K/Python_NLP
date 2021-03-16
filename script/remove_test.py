import sys
if __name__ == '__main__':
    if len(sys.argv) != 7:
        sys.exit(
            'err! python3 remove_test.py RAWTEST.cn RAWTEST.en TEST.cn TEST.en RECORD MODEL'
        )
    RAWCN = sys.argv[1]
    RAWEN = sys.argv[2]
    CN = sys.argv[3]
    EN = sys.argv[4]
    RECORD = sys.argv[5]
    MODEL = sys.argv[6]
    w_rc = open('new_RC', 'w', encoding='utf-8')
    w_re = open('new_RE', 'w', encoding='utf-8')
    w_c = open('new_C', 'w', encoding='utf-8')
    w_e = open('new_E', 'w', encoding='utf-8')
    w_r = open('new_R', 'w', encoding='utf-8')
    if MODEL == '2' or MODEL == '3':
        with open(RAWCN, 'r', encoding='utf-8') as RC:
            with open(RAWEN, 'r', encoding='utf-8') as RE:
                with open(CN, 'r', encoding='utf-8') as C:
                    with open(EN, 'r', encoding='utf-8') as E:
                        with open(RECORD, 'r', encoding='utf-8') as R:
                            for rc, re, c, e, r in zip(RC.readlines(),
                                                       RE.readlines(),
                                                       C.readlines(),
                                                       E.readlines(),
                                                       R.readlines()):
                                if len(c) > 1000 or len(e) > 1000:
                                    continue
                                else:
                                    w_rc.write(rc)
                                    w_re.write(re)
                                    w_c.write(c)
                                    w_e.write(e)
                                    w_r.write(r)
    else:
        with open(RAWCN, 'r', encoding='utf-8') as RC:
            with open(RAWEN, 'r', encoding='utf-8') as RE:
                with open(CN, 'r', encoding='utf-8') as C:
                    with open(EN, 'r', encoding='utf-8') as E:
                        for rc, re, c, e in zip(RC.readlines(), RE.readlines(),
                                                C.readlines(), E.readlines()):
                            if len(c) > 1000 or len(e) > 1000:
                                continue
                            else:
                                w_rc.write(rc)
                                w_re.write(re)
                                w_c.write(c)
                                w_e.write(e)
    w_rc.close()
    w_re.close()
    w_c.close()
    w_e.close()
    w_r.close()
