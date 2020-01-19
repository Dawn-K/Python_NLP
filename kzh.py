import re, sys, os
import pynlpir
if __name__ == '__main__':
    # print(sys.argv)
    pynlpir.open()
    assert (len(sys.argv) == 3)
    lang = []
    tmp_file_c = open('cn_token', 'w', encoding='utf-8')  # tmp
    out_c2e = open('c2e', 'w', encoding='utf-8')  # out c2e
    print('start to creat cn token')
    with open(sys.argv[1], 'r', encoding='utf-8') as file:  #  cn
        for word in file:
            final_str = ' '.join(pynlpir.segment(word, pos_tagging=False))
            tmp_file_c.write(final_str + '\n')
    pynlpir.close()
    print('start to creat en token')
    en_token_cmd = r'perl ~/moses/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < ' + sys.argv[
        2] + r' > en_token'
    # os.system(en_token_cmd)
    # perl /root/moses/mosesdecoder/scripts/recaser/train-truecaser.perl --model truecase_model.en --corpus en_token
    # perl /root/moses/mosesdecoder/scripts/recaser/truecase.perl        --model truecase_model.en < en_token > en_true_token
    # en_true_token_cmd1 = r'perl /root/moses/mosesdecoder/scripts/recaser/train-truecaser.perl --model truecase_model.en --corpus en_token'
    # en_true_token_cmd2 = r'perl /root/moses/mosesdecoder/scripts/recaser/truecase.perl        --model truecase_model.en < en_token > en_true_token'
    # os.system(en_true_token_cmd1)
    # os.system(en_true_token_cmd2)
    print('start to creat parrel')
    with open('cn_token', 'r', encoding='utf-8') as f1:
        with open('en_token', 'r', encoding='utf-8') as f2:
            for lc, le in zip(f1.readlines(), f2.readlines()):
                lc = lc.rstrip('\n ')
                le = le.rstrip('\n ')
                word_c2e = lc + ' ||| ' + le + '\n'
                print(word_c2e)
                out_c2e.write(word_c2e)
    out_c2e.close()
    tmp_file_c.close()
    # print('start to fast_align')
    # fast_ali_cmd1 = r'/root/fast_align/fast_align-master/build/fast_align -i c2e -d -o -v > forward.align'
    # fast_ali_cmd2 = r'/root/fast_align/fast_align-master/build/fast_align -i c2e -d -o -v -r > reverse.align'
    # fast_ali_cmd3 = r'/root/fast_align/fast_align-master/build/atools -i forward.align -j reverse.align -c grow-diag-final-and > final.align'
    # os.system(fast_ali_cmd1)
    # os.system(fast_ali_cmd2)
    # os.system(fast_ali_cmd3)
    print('success')
    # print(cmd)
    # ~/moses/mosesdecoder/scripts/tokenizer
