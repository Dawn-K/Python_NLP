r"""分数评估的主文件,可计算准确率,召回率,F1值,BLEU值
"""
import PRF, BLEU, sys


def evaluate(cn_file, en_file, en_ref_file):
    PRF.calculate_F1(cn_file, en_file)
    BLEU.BLEU(en_file, en_ref_file)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(
            'Expect three parameters\n such as:   python evaluate.py  CN_SOURCE_FILE EN_SOURCE_FILE EN_REF_FILE'
        )
    CN_file = sys.argv[1]
    EN_file = sys.argv[2]
    EN_ref_file = sys.argv[3]
    evaluate(CN_file, EN_file, EN_ref_file)
