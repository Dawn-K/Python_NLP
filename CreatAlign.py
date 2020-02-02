r""" creat cn_token , c2e , en_token

"""
import re, sys, os
import pynlpir


def creat_cn_token():
    tmp_file_c = open('data/cn_token', 'w', encoding='utf-8')  # creat cn_token
    with open('data/cn', 'r', encoding='utf-8') as file:  #  read cn
        for word in file:
            final_str = ' '.join(pynlpir.segment(word, pos_tagging=False))
            tmp_file_c.write(final_str + '\n')
    pynlpir.close()
    tmp_file_c.close()


def creat_en_token():
    en_token_cmd = r'perl ~/moses/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < data/en  > data/en_token'
    os.system(en_token_cmd)
    en_true_token_cmd1 = r'perl /root/moses/mosesdecoder/scripts/recaser/train-truecaser.perl --model data/truecase_model.en --corpus data/en_token'
    en_true_token_cmd2 = r'perl /root/moses/mosesdecoder/scripts/recaser/truecase.perl        --model data/truecase_model.en < data/en_token > data/en_true_token'
    os.system(en_true_token_cmd1)
    os.system(en_true_token_cmd2)


def creat_parrel():
    out_c2e = open('data/c2e', 'w', encoding='utf-8')  # creat c2e
    with open('data/cn_token', 'r', encoding='utf-8') as f1:
        with open('data/en_true_token', 'r', encoding='utf-8') as f2:
            for lc, le in zip(f1.readlines(), f2.readlines()):
                lc = lc.rstrip('\n ')
                le = le.rstrip('\n ')
                word_c2e = lc + ' ||| ' + le + '\n'
                out_c2e.write(word_c2e)
    out_c2e.close()


def creat_fast_align():
    fast_ali_cmd1 = r'/root/fast_align/fast_align-master/build/fast_align -i data/c2e -d -o -v > data/forward.align'
    fast_ali_cmd2 = r'/root/fast_align/fast_align-master/build/fast_align -i data/c2e -d -o -v -r > data/reverse.align'
    fast_ali_cmd3 = r'/root/fast_align/fast_align-master/build/atools -i data/forward.align -j data/reverse.align -c grow-diag-final-and > data/final.align'
    os.system(fast_ali_cmd1)
    os.system(fast_ali_cmd2)
    os.system(fast_ali_cmd3)


def main_creat():
    pynlpir.open()
    # assert (len(sys.argv) == 3)
    print('start to creat cn token')
    creat_cn_token()

    print('start to creat en token')
    creat_en_token()

    print('start to creat parrel')
    creat_parrel()

    print('start to fast_align')
    creat_fast_align()

    print('success')


if __name__ == '__main__':
    main_creat()
