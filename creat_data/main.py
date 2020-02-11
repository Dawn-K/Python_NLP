import CreatSmall as CS
import CreatCE as CCE
import CreatAlign as CA
import CreatLableData as CLD
import sys


def MainCreat(file_name: str, line_num: int, record_num: int):
    CS.wmt2018_to_rawsmall(file_name, line_num)
    CCE.creat_cn_en()
    CA.main_creat()
    CLD.CreatLableData(record_num)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(
            'Expect three parameters\n such as:   python main.py  CN2EN_SOURCE_FILE READ_FILE_NUM RECORD_NUM'
        )
    CN2EN_SOURCE_FILE = sys.argv[1]
    READ_FILE_NUM = sys.argv[2]
    RECORD_NUM = sys.argv[3]
    MainCreat(CN2EN_SOURCE_FILE, READ_FILE_NUM, RECORD_NUM)
