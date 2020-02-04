import PRF, BLEU
PRF.normal('out_test.cn', 'out_test.en')
BLEU.BLEU('out_test.cn', 'out_test.en', 'out_test.en')
