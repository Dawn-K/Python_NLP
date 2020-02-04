import pynlpir,os


def process_cn(file_name: str):
    pynlpir.open()
    tmp_file_c = open('cn_true_token', 'w', encoding='utf-8')  # creat cn_token
    with open(file_name, 'r', encoding='utf-8') as file:  #  read cn
        for word in file:
            final_str = ' '.join(pynlpir.segment(word, pos_tagging=False))
            tmp_file_c.write(final_str + '\n')
    pynlpir.close()
    tmp_file_c.close()


def process_en(file_name: str,store_file:str):
    en_token_cmd = r'perl ~/moses/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < ' + file_name + r'  > en_token'
    os.system(en_token_cmd)
    en_true_token_cmd1 = r'perl /root/moses/mosesdecoder/scripts/recaser/train-truecaser.perl --model truecase_model.en --corpus en_token'
    en_true_token_cmd2 = r'perl /root/moses/mosesdecoder/scripts/recaser/truecase.perl        --model truecase_model.en < en_token > '+store_file
    os.system(en_true_token_cmd1)
    os.system(en_true_token_cmd2)


def BLEU(cn_file_name: str, en_file_name: str, en_ref_name: str):
    # process_cn(cn_file_name)
    process_en(en_file_name,'en_true_token')
    process_en(en_ref_name,'ref_true_token')
    BLEU_cmd = r'perl /root/moses/mosesdecoder/scripts/generic/multi-bleu.perl en_true_token < ref_true_token'
    os.system(BLEU_cmd)
