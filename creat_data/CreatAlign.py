r""" creat cn_token , c2e , en_token

"""
import re, sys, os
import pynlpir
import jieba


def creat_cn_token():
    tmp_file_c = open('data/cn_token', 'w', encoding='utf-8')  # creat cn_token
    with open('data/cn', 'r', encoding='utf-8') as file:  #  read cn
        for word in file:
            final_str = ' '.join(jieba.cut(word))
            #print('final str:',final_str)
            #final_str1 = ' '.join(pynlpir.segment(word,pos_tagging=False))
            #print(final_str == final_str1)
            tmp_file_c.write(final_str)
    pynlpir.close()
    tmp_file_c.close()


# ~/moses/mosesdecoder/scripts
def creat_en_token(moses_path: str):
    en_token_cmd = r'perl ' + moses_path + r'/tokenizer/tokenizer.perl  -threads 8 -l en < data/en  > data/en_token'
    os.system(en_token_cmd)
    en_true_token_cmd1 = r'perl ' + moses_path + r'/recaser/train-truecaser.perl --model data/truecase_model.en --corpus data/en_token'
    en_true_token_cmd2 = r'perl ' + moses_path + r'/recaser/truecase.perl        --model data/truecase_model.en < data/en_token > data/en_true_token'
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


#/root/fast_align/fast_align-master/build
def creat_fast_align(fast_align_path: str):
    fast_ali_cmd1 = fast_align_path + r'/fast_align -i data/c2e -d -o -v > data/forward.align'
    fast_ali_cmd2 = fast_align_path + r'/fast_align -i data/c2e -d -o -v -r > data/reverse.align'
    fast_ali_cmd3 = fast_align_path + r'/atools -i data/forward.align -j data/reverse.align -c grow-diag-final-and > data/final.align'
    os.system(fast_ali_cmd1)
    os.system(fast_ali_cmd2)
    os.system(fast_ali_cmd3)


def main_creat(moses_path: str, fast_align_path: str):
    pynlpir.open()
    # assert (len(sys.argv) == 3)
    print('start to creat cn token')
    creat_cn_token()

    print('start to creat en token')
    creat_en_token(moses_path)

    print('start to creat parrel')
    creat_parrel()

    print('start to fast_align')
    creat_fast_align(fast_align_path)

    print('success')
