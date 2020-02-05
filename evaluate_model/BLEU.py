r"""使用moses自带的 multi-blue.perl 测试BLEU值
"""
import pynlpir, os


# perl ~/moses/mosesdecoder/scripts/tokenizer/tokenizer.perl
# perl /root/moses/mosesdecoder/scripts/recaser/train-truecaser.perl
# perl /root/moses/mosesdecoder/scripts/recaser/truecase.perl
# perl /root/moses/mosesdecoder/scripts/generic/multi-bleu.perl
# perl /root/moses/mosesdecoder/scripts/generic/multi-bleu.perl

def process_cn(file_name: str, store_file: str):
    pynlpir.open()
    tmp_file_c = open('data/cn_true_token', 'w', encoding='utf-8')  # creat cn_token
    with open(file_name, 'r', encoding='utf-8') as file:  #  read cn
        for word in file:
            final_str = ' '.join(pynlpir.segment(word, pos_tagging=False))
            tmp_file_c.write(final_str + '\n')
    pynlpir.close()
    tmp_file_c.close()


def process_en(file_name: str, store_file: str):
    # 多测几个
    # todo: 此方法造出的数据会将标签拆开, <sub> 会拆成 &lt; sub &gt;
    en_token_cmd = r'perl tools/tokenizer.perl -l en < ' + file_name + r'  > data/en_token'
    os.system(en_token_cmd)
    en_true_token_cmd1 = r'perl tools/train-truecaser.perl --model data/truecase_model.en --corpus data/en_token'
    en_true_token_cmd2 = r'perl tools/truecase.perl        --model data/truecase_model.en < data/en_token > ' + store_file
    os.system(en_true_token_cmd1)
    os.system(en_true_token_cmd2)


def BLEU(file_name: str, ref_name: str, typ='en'):
    BLEU_cmd = ''
    data_path = os.getcwd() + '/data'
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if typ == 'cn':
        process_cn(file_name, 'data/cn_true_token')
        process_cn(ref_name, 'data/ref_true_token')
        BLEU_cmd = r'perl tools/multi-bleu.perl data/cn_true_token < data/ref_true_token'
    elif typ == 'en':
        process_en(file_name, 'data/en_true_token')
        process_en(ref_name, 'data/ref_true_token')
        BLEU_cmd = r'perl tools/multi-bleu.perl data/en_true_token < data/ref_true_token'
    else:
        print(r'err!! typ must be \'cn\' or \'en\' ')
    os.system(BLEU_cmd)
