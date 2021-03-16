import CreatSmall as CS
import CreatCE as CCE
import CreatAlign as CA
import CreatLableData as CLD
import CreatTest as CT
import sys


def MainCreat(file_name: str, line_num: int, test_file: str, record_num: int,
              moses_path: str, fast_align_path: str):
    CS.wmt2018_to_rawsmall(file_name, line_num)
    CCE.creat_cn_en()
    CA.main_creat(moses_path, fast_align_path)
    CLD.CreatLableData(record_num)
    CT.splitce(test_file)


if __name__ == '__main__':
    if len(sys.argv) != 7:
        sys.exit(
            'Expect 6 parameters\n such as:   python main.py  CN2EN_SOURCE_FILE READ_FILE_NUM TEST_FILE RECORD_NUM MOSESPATH FASTPATH'
        )
    CN2EN_SOURCE_FILE = sys.argv[1]
    READ_FILE_NUM = int(sys.argv[2])
    TEST_FILE = sys.argv[3]
    RECORD_NUM = int(sys.argv[4])
    MOSESPATH = sys.argv[5]
    FASTPATH = sys.argv[6]
    MainCreat(CN2EN_SOURCE_FILE, READ_FILE_NUM, TEST_FILE, RECORD_NUM,
              MOSESPATH, FASTPATH)
